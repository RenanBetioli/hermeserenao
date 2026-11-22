"""Diagrama da arquitetura adaptada, gerado como SVG sem dependências."""

NODES = [
    ("user", "Você", ["operador"], 24, 238, 140, 58, "person"),
    ("access", "Acesso local", ["CLI / TUI", "navegador", "gateway"], 216, 214, 176, 106, "access"),
    ("models", "Modelos de IA", ["opcional", "sem chave"], 216, 62, 176, 72, "external"),
    ("core", "hermeserenao", ["núcleo do agente"], 458, 214, 188, 88, "core"),
    ("context", "Contexto", ["memória", "base versionada", "skills"], 724, 70, 206, 112, "context"),
    ("execution", "Execução", ["terminal", "arquivos", "código"], 724, 212, 206, 112, "execution"),
    ("integration", "Integrações", ["adaptadores stub"], 724, 356, 206, 82, "execution"),
    ("central", "Central de Operações", ["painel + API"], 458, 372, 188, 82, "operations"),
    ("local", "Localhost", ["127.0.0.1:8765", "sem domínio"], 216, 372, 176, 82, "access"),
]

EDGES = [
    ("user", "access"), ("access", "core"), ("models", "core"),
    ("core", "context"), ("core", "execution"), ("core", "integration"),
    ("core", "central"), ("local", "central"),
]

STYLE = """
  text { font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif; fill: #e6e9ec; }
  .title { font-size: 19px; font-weight: 650; letter-spacing: .2px; }
  .sub { font-size: 12px; fill: #8b949e; }
  .label { font-size: 14px; font-weight: 600; }
  .line { font-size: 12px; fill: #a4aeb7; }
  .edge { stroke: #4c5661; stroke-width: 1.6; fill: none; marker-end: url(#arrow); }
  .person rect { fill: #2d2417; stroke: #d99a4a; }
  .access rect { fill: #1b2127; stroke: #4c5661; }
  .external rect { fill: #1b2127; stroke: #4c5661; stroke-dasharray: 5 4; }
  .core rect { fill: #2b2114; stroke: #e0a458; stroke-width: 2; }
  .context rect { fill: #211d2b; stroke: #8d7bb8; }
  .execution rect { fill: #17251e; stroke: #4e8f68; }
  .operations rect { fill: #2a2416; stroke: #d99a4a; stroke-width: 1.6; }
"""


def svg() -> str:
    by_id = {n[0]: n for n in NODES}
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 470" role="img" '
        'aria-label="Arquitetura adaptada do hermeserenao">',
        '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="3" '
        'orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#4c5661"/>'
        '</marker></defs>',
        f'<style>{STYLE}</style>',
        '<text class="title" x="24" y="32">Arquitetura local · hermeserenao</text>',
        '<text class="sub" x="24" y="50">Versão adaptada: sem VPS, domínio ou serviços pagos</text>',
    ]
    for a, b in EDGES:
        _, _, _, x1, y1, w1, h1, _ = by_id[a]
        _, _, _, x2, y2, w2, h2, _ = by_id[b]
        sx, sy = x1 + w1, y1 + h1 / 2
        ex, ey = x2, y2 + h2 / 2
        if b == "central" and a == "core":
            sx, sy = x1 + w1 / 2, y1 + h1
            ex, ey = x2 + w2 / 2, y2
        out.append(f'<path class="edge" d="M{sx},{sy} C{(sx+ex)/2},{sy} {(sx+ex)/2},{ey} {ex},{ey}"/>')
    for key, label, lines, x, y, w, h, kind in NODES:
        out.append(f'<g class="{kind}">')
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>')
        cy = y + 23 if len(lines) > 1 else y + h / 2 + 5
        out.append(f'<text class="label" x="{x + w/2}" y="{cy}" text-anchor="middle">{label}</text>')
        for i, line in enumerate(lines):
            out.append(f'<text class="line" x="{x + w/2}" y="{cy + 17 + i*14}" text-anchor="middle">{line}</text>')
        out.append('</g>')
    out.append('<text class="sub" x="24" y="458">Componentes tracejados são opcionais / futuros</text>')
    out.append('</svg>')
    return "".join(out)
