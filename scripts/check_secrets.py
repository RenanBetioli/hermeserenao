#!/usr/bin/env python3.13
"""Verifica padrões de segredo nos arquivos versionados."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "__pycache__", "scripts", "tests", ".venv", "venv"}
SUFFIXES = {".py", ".md", ".json", ".yml", ".yaml", ".html", ".toml", ".env", ".txt"}
PATTERNS = [
    ("token de API", re.compile(r"sk-" + r"[A-Za-z0-9]{20,}")),
    ("token do GitHub", re.compile(r"gh[pousr]_" + r"[A-Za-z0-9]{20,}")),
    ("chave AWS", re.compile(r"AKIA" + r"[A-Z0-9]{16}")),
    ("senha literal", re.compile(r"(?i)password\s*[:=]\s*['\"][^'\"]{6,}")),
    ("bearer JWT", re.compile(r"Bearer\s+ey[A-Za-z0-9_-]{10,}")),
]


def main():
    findings = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for name, pattern in PATTERNS:
                if pattern.search(line):
                    findings.append(f"{path.relative_to(ROOT)}:{n} — {name}")
    if findings:
        print("Possíveis segredos encontrados:")
        print("\n".join(findings))
        return 1
    print("OK — nenhum padrão de segredo encontrado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
