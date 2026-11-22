"""API HTTP e serviços do hermeserenao (somente stdlib)."""
import json
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .architecture import svg as architecture_svg

ROOT = Path(__file__).resolve().parent.parent
CONTEXT = ROOT / "context"
SKILLS = ROOT / "skills"
INTEGRATIONS = ROOT / "integrations"
EVENTS = ROOT / "state" / "events.jsonl"
STATIC = ROOT / "app" / "static"
STOPWORDS = {"de", "da", "do", "e", "em", "um", "uma", "para", "com", "como", "o", "a", "os", "as", "no", "na"}


def _md_files():
    return sorted(CONTEXT.rglob("*.md"))


def _rel(path):
    return str(path.relative_to(ROOT)).replace("\\", "/")


def status_payload():
    ctx = _md_files()
    registry = SKILLS / "registry.json"
    skills = json.loads(registry.read_text(encoding="utf-8")) if registry.exists() else []
    adapters = sorted(p.stem for p in INTEGRATIONS.glob("*.py") if not p.name.startswith("__"))
    jobs = ROOT / "state" / "jobs.json"
    enabled = 0
    if jobs.exists():
        enabled = sum(1 for j in json.loads(jobs.read_text(encoding="utf-8")) if j.get("enabled"))
    comps = [
        {"id": "api", "label": "API local", "state": "ok", "detail": "Python stdlib · 127.0.0.1"},
        {"id": "agent", "label": "Núcleo do agente", "state": "demo", "detail": "sem chamada a modelo"},
        {"id": "gateway", "label": "Gateway", "state": "demo", "detail": "eventos em state/events.jsonl"},
        {"id": "context", "label": "Base de contexto", "state": "ok" if ctx else "off", "detail": f"{len(ctx)} documentos"},
        {"id": "skills", "label": "Skills", "state": "ok" if skills else "off", "detail": f"{len(skills)} registrada{'s' if len(skills) != 1 else ''}"},
        {"id": "scheduler", "label": "Agendador", "state": "demo", "detail": f"{enabled} rotina{'s' if enabled != 1 else ''} habilitada{'s' if enabled != 1 else ''}"},
        {"id": "integration", "label": "Integrações", "state": "demo", "detail": f"{len(adapters)} adaptador{'es' if len(adapters) != 1 else ''} stub"},
        {"id": "central", "label": "Central de Operações", "state": "ok", "detail": "painel + API"},
    ]
    return {"components": comps, "host": "local", "generated_at": int(time.time())}


def list_context():
    out = []
    for p in _md_files():
        lines = p.read_text(encoding="utf-8").splitlines()
        title = next((l.lstrip("# ").strip() for l in lines if l.startswith("#")), p.stem)
        out.append({"path": _rel(p), "title": title, "lines": len(lines)})
    return out


def list_skills():
    registry = SKILLS / "registry.json"
    return json.loads(registry.read_text(encoding="utf-8")) if registry.exists() else []


def list_jobs():
    jobs = ROOT / "state" / "jobs.json"
    return json.loads(jobs.read_text(encoding="utf-8")) if jobs.exists() else []


def recent_events(limit=12):
    if not EVENTS.exists():
        return []
    rows = []
    for line in EVENTS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return list(reversed(rows[-limit:]))


def append_event(kind, detail):
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "kind": kind, "detail": detail}
    with EVENTS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def ask_payload(question):
    tokens = {t for t in re.findall(r"[\wÀ-ÿ]{3,}", question.lower()) if t not in STOPWORDS}
    hits = []
    for p in _md_files():
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            text = line.strip()
            if len(text) < 24 or text.startswith("#"):
                continue
            low = text.lower()
            score = sum(1 for t in tokens if t in low)
            if score:
                hits.append({"source": _rel(p), "line": n, "text": text[:260], "score": score})
    hits.sort(key=lambda h: (-h["score"], h["source"], h["line"]))
    append_event("ask", question[:120])
    return {"question": question, "answers": hits[:5], "mode": "busca determinística (sem LLM)"}


class Handler(BaseHTTPRequestHandler):
    server_version = "hermeserenao/0.1"

    def log_message(self, *_):
        pass

    def _send(self, code, body, ctype):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, data, code=200):
        self._send(code, json.dumps(data, ensure_ascii=False, indent=2), "application/json; charset=utf-8")

    def do_GET(self):
        path = urlparse(self.path).path
        routes = {
            "/api/status": lambda: self._json(status_payload()),
            "/api/context": lambda: self._json(list_context()),
            "/api/skills": lambda: self._json(list_skills()),
            "/api/events": lambda: self._json(recent_events()),
            "/api/jobs": lambda: self._json(list_jobs()),
            "/api/architecture.svg": lambda: self._send(200, architecture_svg(), "image/svg+xml; charset=utf-8"),
        }
        if path in routes:
            return routes[path]()
        if path in ("/", "/index.html"):
            path = "/static/index.html"
        if path.startswith("/static/"):
            target = (STATIC / path[len("/static/"):]).resolve()
            if STATIC.resolve() in target.parents and target.is_file():
                ctype = "text/html; charset=utf-8" if target.suffix == ".html" else "text/plain; charset=utf-8"
                return self._send(200, target.read_bytes(), ctype)
        self._json({"error": "not found"}, 404)

    def do_POST(self):
        if urlparse(self.path).path != "/api/ask":
            return self._json({"error": "not found"}, 404)
        try:
            size = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(size) or b"{}")
            question = str(body.get("question", "")).strip()
        except (ValueError, json.JSONDecodeError):
            return self._json({"error": "JSON inválido"}, 400)
        if not question:
            return self._json({"error": "question vazia"}, 400)
        self._json(ask_payload(question))


def run_server(port=8765, host="127.0.0.1"):
    append_event("server_started", f"container:{port}" if host == "0.0.0.0" else f"{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
