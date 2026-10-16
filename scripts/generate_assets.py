"""Generate the animated SVGs used by the profile README.

Run from the repo root:  python scripts/generate_assets.py
Every SVG is self-contained (CSS + SMIL animations, system fonts only),
so GitHub renders it without any external service.
"""

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

BG = "#0D1117"
PANEL = "#0F151D"
BORDER = "#30363D"
TEXT = "#E6EDF3"
MUTED = "#8B949E"
GREEN = "#7EE787"
BLUE = "#79C0FF"
CYAN = "#39D0D8"
AMBER = "#F2CC60"
PURPLE = "#D2A8FF"

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Code', 'SF Mono', Consolas, Menlo, monospace"

REDUCED_MOTION = """
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; opacity: 1 !important; transform: none !important; }
}"""


def x(s):
    return escape(s, quote=True)


def svg(w, h, body, style="", title=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="{x(title)}">
<title>{x(title)}</title>
<style>
.sans {{ font-family: {SANS}; }}
.mono {{ font-family: {MONO}; }}
@keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
@keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
@keyframes pulse {{ 0% {{ opacity: .9; transform: scale(1); }} 100% {{ opacity: 0; transform: scale(2.6); }} }}
.fade-up {{ opacity: 0; animation: fadeUp .8s cubic-bezier(.2,.7,.2,1) forwards; }}
.fade-in {{ opacity: 0; animation: fadeIn .8s ease forwards; }}
{style}
{REDUCED_MOTION}
</style>
{body}
</svg>
"""


def typed_clip(cid, x0, y0, chars, char_w, h, begin, dur):
    """clipPath that reveals monospace text one character at a time."""
    values = ";".join(str(round(i * char_w, 1)) for i in range(chars + 1))
    return (
        f'<clipPath id="{cid}"><rect x="{x0}" y="{y0}" height="{h}" width="0">'
        f'<animate attributeName="width" values="{values}" begin="{begin}s" dur="{dur}s" '
        f'calcMode="discrete" fill="freeze"/></rect></clipPath>'
    )


# ---------------------------------------------------------------- header
def header():
    W, H = 1200, 400
    prompt = "camilo@la-paz:~$ "
    cmd = "whoami"
    cw = 9.6  # 16px monospace advance
    roles = [
        ("real-time systems", CYAN),
        ("secure code sandboxes", GREEN),
        ("RAG assistants with LLMs", AMBER),
        ("clean, well-tested backends", BLUE),
    ]
    cycle = 12
    slot = cycle / len(roles)
    role_css, role_svg = [], []
    for i, (role, color) in enumerate(roles):
        start = i * slot / cycle * 100
        end = (i + 1) * slot / cycle * 100
        role_css.append(
            f"@keyframes role{i} {{ 0% {{ opacity: 0; transform: translateY(8px); }} "
            f"{max(start, 0.01):.2f}% {{ opacity: 0; transform: translateY(8px); }} "
            f"{start + 2:.2f}% {{ opacity: 1; transform: translateY(0); }} "
            f"{end - 2:.2f}% {{ opacity: 1; transform: translateY(0); }} "
            f"{end:.2f}% {{ opacity: 0; transform: translateY(-8px); }} 100% {{ opacity: 0; }} }}\n"
            f".role{i} {{ opacity: 0; animation: role{i} {cycle}s linear 2.6s infinite; }}"
        )
        role_svg.append(f'<text class="mono role{i}" x="186" y="296" font-size="17" fill="{color}">{x(role)}</text>')

    chips = [("La Paz, Bolivia", GREEN), ("Open to remote", BLUE), ("UPB · GPA 96/100", AMBER)]
    chip_svg, cx = [], 60
    for i, (label, color) in enumerate(chips):
        w = int(len(label) * 7.4) + 38
        chip_svg.append(
            f'<g class="fade-up" style="animation-delay:{2.2 + i * .15:.2f}s">'
            f'<rect x="{cx}" y="324" width="{w}" height="30" rx="15" fill="{color}" fill-opacity=".08" stroke="{color}" stroke-opacity=".35"/>'
            f'<circle cx="{cx + 16}" cy="339" r="4" fill="{color}"/>'
            f'<text class="sans" x="{cx + 28}" y="344" font-size="13" fill="{TEXT}">{x(label)}</text></g>'
        )
        cx += w + 10

    # live system map (right panel)
    nodes = {
        "api": (885, 118, "api · gRPC"),
        "queue": (1075, 118, "redis streams"),
        "worker": (1075, 218, "sandbox ×3"),
        "db": (885, 218, "postgres"),
        "rag": (980, 300, "rag · pgvector"),
    }
    node_svg = []
    for i, (key, (nx, ny, label)) in enumerate(nodes.items()):
        node_svg.append(
            f'<g class="fade-in" style="animation-delay:{1.4 + i * .15:.2f}s">'
            f'<rect x="{nx - 68}" y="{ny - 17}" width="136" height="34" rx="8" fill="{BG}" stroke="{BORDER}"/>'
            f'<circle cx="{nx - 54}" cy="{ny}" r="3.5" fill="{GREEN}"/>'
            f'<text class="mono" x="{nx - 44}" y="{ny + 4.5}" font-size="12.5" fill="{TEXT}">{x(label)}</text></g>'
        )
    loop = "M953 118 H1007 M1075 135 V201 M1007 218 H953"
    edges = [
        ("M953 118 L1007 118", CYAN, 0),
        ("M1075 135 L1075 201", GREEN, .7),
        ("M1007 218 L953 218", BLUE, 1.4),
        ("M885 235 L960 283", AMBER, 2.1),
        ("M1075 235 L1000 283", PURPLE, 2.8),
        ("M885 135 L885 201", MUTED, 3.5),
    ]
    edge_svg = [f'<path d="{loop}" stroke="{BORDER}" stroke-width="1.5"/>']
    for d, color, delay in edges:
        edge_svg.append(f'<path d="{d}" stroke="{BORDER}" stroke-width="1.5" stroke-dasharray="4 4"/>')
        edge_svg.append(
            f'<circle r="3.5" fill="{color}" opacity="0"><animateMotion dur="1.6s" begin="{delay + 2}s;p{int(delay*10)}.end+2.6s" '
            f'id="p{int(delay*10)}" path="{d}"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.85;1" dur="1.6s" begin="{delay + 2}s;p{int(delay*10)}.end+2.6s"/></circle>'
        )

    body = f"""
<defs>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" stroke="#161B22" stroke-width="1"/>
  </pattern>
  <radialGradient id="glowA" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(260 120) scale(420 300)">
    <stop stop-color="{GREEN}" stop-opacity=".16"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowB" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(980 260) scale(380 260)">
    <stop stop-color="{BLUE}" stop-opacity=".14"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="nameGrad" x1="0" y1="0" x2="600" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="reflect">
    <stop stop-color="{GREEN}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{BLUE}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="0 0;600 0;0 0" dur="10s" repeatCount="indefinite"/>
  </linearGradient>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  {typed_clip("typeCmd", 60 + len(prompt) * cw, 60, len(cmd), cw, 26, .5, .9)}
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <rect width="{W}" height="{H}" fill="url(#glowA)">
    <animate attributeName="opacity" values="1;.55;1" dur="8s" repeatCount="indefinite"/>
  </rect>
  <rect width="{W}" height="{H}" fill="url(#glowB)">
    <animate attributeName="opacity" values=".6;1;.6" dur="8s" repeatCount="indefinite"/>
  </rect>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" stroke="{BORDER}"/>

<text class="mono" x="60" y="80" font-size="16"><tspan fill="{GREEN}">camilo@la-paz</tspan><tspan fill="{MUTED}">:</tspan><tspan fill="{BLUE}">~</tspan><tspan fill="{MUTED}">$ </tspan></text>
<text class="mono" x="{60 + len(prompt) * cw}" y="80" font-size="16" fill="{TEXT}" clip-path="url(#typeCmd)">{cmd}</text>
<rect x="{60 + (len(prompt) + len(cmd)) * cw + 2}" y="66" width="9" height="18" fill="{GREEN}" style="animation: blink 1s step-end infinite;"/>

<text class="sans fade-up" style="animation-delay:1.3s" x="58" y="152" font-size="58" font-weight="700" fill="{TEXT}" letter-spacing="-1.2">Camilo Raphael</text>
<text class="sans fade-up" style="animation-delay:1.5s" x="58" y="214" font-size="58" font-weight="700" fill="url(#nameGrad)" letter-spacing="-1.2">Zuleta Wolff</text>
<text class="sans fade-up" style="animation-delay:1.8s" x="60" y="254" font-size="20" fill="{MUTED}">Software Engineer  ·  Backend (Java, Node.js, Go)  ·  Applied AI</text>
<text class="mono fade-in" style="animation-delay:2.4s" x="60" y="296" font-size="17" fill="{MUTED}">&gt; building</text>
{''.join(role_svg)}
{''.join(chip_svg)}

<g class="fade-in" style="animation-delay:1.1s">
  <rect x="790" y="48" width="372" height="300" rx="14" fill="{PANEL}" fill-opacity=".85" stroke="#21262D"/>
  <circle cx="814" cy="72" r="5" fill="#FF7B72"/><circle cx="832" cy="72" r="5" fill="{AMBER}"/><circle cx="850" cy="72" r="5" fill="{GREEN}"/>
  <text class="mono" x="1144" y="76" font-size="11.5" fill="{MUTED}" text-anchor="end">system.map — live</text>
  <g transform="translate(984 72)">
    <circle r="3.5" fill="{GREEN}"/>
    <circle r="3.5" fill="{GREEN}" style="transform-box: fill-box; transform-origin: center; animation: pulse 1.8s ease-out infinite;"/>
  </g>
  <path d="M790 92 H1162" stroke="#21262D"/>
</g>
{''.join(edge_svg)}
{''.join(node_svg)}
"""
    return svg(W, H, body, "\n".join(role_css), "Camilo Raphael Zuleta Wolff — Software Engineer, Backend and Applied AI")


# ---------------------------------------------------------------- metrics
def metrics():
    W, H = 1200, 150
    tiles = [
        ("300+", "Cypress E2E tests", "critical API &amp; user flows", GREEN),
        ("10k", "requests / minute", "k6 load-tested Express service", CYAN),
        ("Top 8", "ICPC Bolivia 2025", "regional competitor 2024 · 2025", AMBER),
        ("1st", "Hackathon winner", "GAM La Paz · July 2026", PURPLE),
    ]
    tw, gap = 285, 20
    out = []
    for i, (big, label, sub, color) in enumerate(tiles):
        tx = i * (tw + gap)
        d = .2 + i * .18
        out.append(f"""
<g class="fade-up" style="animation-delay:{d:.2f}s">
  <rect x="{tx + .5}" y=".5" width="{tw - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{BORDER}"/>
  <rect x="{tx + 24}" y="{H - 22}" width="0" height="3" rx="1.5" fill="{color}">
    <animate attributeName="width" from="0" to="{tw - 48}" begin="{d + .5:.2f}s" dur="1.2s" fill="freeze" calcMode="spline" keySplines=".2 .7 .2 1"/>
  </rect>
  <rect x="{tx + 24}" y="{H - 22}" width="{tw - 48}" height="3" rx="1.5" fill="{color}" fill-opacity=".12"/>
  <text class="sans" x="{tx + 24}" y="62" font-size="42" font-weight="700" fill="{color}" letter-spacing="-1">{big}</text>
  <text class="sans" x="{tx + 24}" y="90" font-size="15" font-weight="600" fill="{TEXT}">{label}</text>
  <text class="sans" x="{tx + 24}" y="111" font-size="12.5" fill="{MUTED}">{sub}</text>
</g>""")
    return svg(W, H, "".join(out), title="Highlights: 300+ E2E tests, 10k requests per minute, ICPC Top 8 Bolivia, hackathon winner")


# ---------------------------------------------------------------- timeline
def timeline():
    W, H = 1200, 290
    y = 145
    events = [
        ("2023", "Started at UPB", "Systems Engineering · TA", BLUE),
        ("2024", "ICPC Regionals", "first regional contest", AMBER),
        ("2025", "ICPC Top 8 Bolivia", "IEEE Student Branch Treasurer", AMBER),
        ("FEB 2026", "Waveware Solutions", "Full-Stack Intern · remote US", CYAN),
        ("JUL 2026", "Hackathon winner", "superAMI · GAM La Paz", PURPLE),
        ("SEP 2026", "Full-Stack Developer", "Web3 products · now", GREEN),
    ]
    x0, step = 110, 196
    line_len = step * (len(events) - 1) + 60
    out = [
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="{BG}" stroke="{BORDER}"/>',
        f'<path d="M80 {y} H{x0 + step * (len(events) - 1) + 30}" stroke="#21262D" stroke-width="2"/>',
        f'<defs><linearGradient id="tl" x1="80" x2="1120" y1="0" y2="0" gradientUnits="userSpaceOnUse">'
        f'<stop stop-color="{BLUE}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{GREEN}"/></linearGradient></defs>',
        f'<path d="M80 {y} H{x0 + step * (len(events) - 1) + 30}" stroke="url(#tl)" stroke-width="2.5" stroke-linecap="round" '
        f'stroke-dasharray="{line_len}" stroke-dashoffset="{line_len}">'
        f'<animate attributeName="stroke-dashoffset" from="{line_len}" to="0" begin=".2s" dur="2.4s" fill="freeze" calcMode="spline" keySplines=".4 0 .2 1"/></path>',
    ]
    for i, (date, title, sub, color) in enumerate(events):
        ex = x0 + i * step
        d = .3 + i * .38
        up = i % 2 == 0
        ty = y - 76 if up else y + 46
        stem = (y - 34, y - 12) if up else (y + 12, y + 30)
        last = i == len(events) - 1
        pulse = (
            f'<circle cx="{ex}" cy="{y}" r="7" fill="{color}" style="transform-box: fill-box; transform-origin: center; '
            f'animation: pulse 2s ease-out {d + .6:.2f}s infinite; opacity: 0;"/>'
            if last else ""
        )
        out.append(f"""
<g class="fade-up" style="animation-delay:{d:.2f}s">
  {pulse}
  <circle cx="{ex}" cy="{y}" r="9" fill="{BG}" stroke="{color}" stroke-width="2.5"/>
  <circle cx="{ex}" cy="{y}" r="3.5" fill="{color}"/>
  <path d="M{ex} {stem[0]} V{stem[1]}" stroke="{color}" stroke-opacity=".4" stroke-dasharray="2 3"/>
  <text class="mono" x="{ex}" y="{ty}" font-size="12" font-weight="700" fill="{color}" text-anchor="middle" letter-spacing="1">{x(date)}</text>
  <text class="sans" x="{ex}" y="{ty + 22}" font-size="15" font-weight="600" fill="{TEXT}" text-anchor="middle">{x(title)}</text>
  <text class="sans" x="{ex}" y="{ty + 41}" font-size="12" fill="{MUTED}" text-anchor="middle">{x(sub)}</text>
</g>""")
    return svg(W, H, "".join(out), title="Timeline from UPB in 2023 to Full-Stack Developer at Waveware Solutions in 2026")


# ---------------------------------------------------------------- project cards
PROJECTS = [
    {
        "slug": "aetherjudge", "name": "AetherJudge", "accent": CYAN, "glyph": "{ }",
        "tagline": "Real-time competitive programming platform",
        "badge": "Go · distributed",
        "bullets": [
            "Runs untrusted C++ / Python / Go in isolated Docker sandboxes",
            "Redis Streams queue with worker recovery: no lost submissions",
            "Live verdicts &amp; leaderboards over WebSockets · Helm + Grafana",
        ],
        "stack": ["Go", "gRPC", "Redis Streams", "PostgreSQL", "Next.js", "Kubernetes"],
    },
    {
        "slug": "superami", "name": "superAMI", "accent": AMBER, "glyph": "AI",
        "tagline": "AI assistant for municipal procedures on WhatsApp",
        "badge": "★ Hackathon winner",
        "bullets": [
            "RAG pipeline: pgvector search with metadata filters",
            "Clarification flows over Bolivian public procedures data",
            "WhatsApp Cloud API webhooks · Docker deploy on AWS EC2",
        ],
        "stack": ["Python", "FastAPI", "pgvector", "WhatsApp API", "AWS EC2"],
    },
    {
        "slug": "nexuscommerce", "name": "NexusCommerce", "accent": BLUE, "glyph": "$",
        "tagline": "Multi-tenant commerce platform",
        "badge": "Java · Spring",
        "bullets": [
            "Storefront + admin dashboard with JWT auth and RBAC",
            "PostgreSQL for orders, MongoDB for catalogs, linked by UUID",
            "Transactional orders with inventory reservation · OpenAPI",
        ],
        "stack": ["Java", "Spring Boot 3", "Next.js", "PostgreSQL", "MongoDB"],
    },
    {
        "slug": "plantini", "name": "Plantini", "accent": GREEN, "glyph": "+1",
        "tagline": "University volunteering app with an AI assistant",
        "badge": "NestJS · mobile",
        "bullets": [
            "NestJS proxy to Gemini that verifies Supabase JWTs",
            "Per-IP rate limiting (20 req/min) and streamed responses",
            "App-level chat ownership where service keys bypass RLS",
        ],
        "stack": ["NestJS", "TypeScript", "React Native", "Supabase", "Gemini", "Jest"],
    },
    {
        "slug": "ajedrez", "name": "Ajedrez Relámpago", "accent": PURPLE, "glyph": "e4",
        "tagline": "Lightning chess with energy and missions",
        "badge": "▶ Live demo",
        "bullets": [
            "Chess variant with energy and mission mechanics",
            "Authoritative game logic on the server",
            "E2E suites running in CI with Cypress and Playwright",
        ],
        "stack": ["React", "Express", "Cypress", "Playwright"],
    },
]


def card(p):
    W, H = 580, 240
    a = p["accent"]
    perim = 2 * (W + H - 4)
    pills, px = [], 28
    for s in p["stack"]:
        w = int(len(s) * 6.9) + 22
        pills.append(
            f'<rect x="{px}" y="190" width="{w}" height="24" rx="12" fill="{a}" fill-opacity=".08" stroke="{a}" stroke-opacity=".3"/>'
            f'<text class="mono" x="{px + w / 2}" y="206" font-size="11.5" fill="{TEXT}" text-anchor="middle">{x(s)}</text>'
        )
        px += w + 8
    bullets = "".join(
        f'<g class="fade-up" style="animation-delay:{.45 + i * .12:.2f}s">'
        f'<path d="M30 {104 + i * 26} l5 4 -5 4" stroke="{a}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<text class="sans" x="46" y="{113 + i * 26}" font-size="13.5" fill="#C9D1D9">{b}</text></g>'
        for i, b in enumerate(p["bullets"])
    )
    bw = int(len(p["badge"]) * 7.2) + 24
    body = f"""
<defs>
  <radialGradient id="g" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(560 0) scale(320 220)">
    <stop stop-color="{a}" stop-opacity=".18"/><stop offset="1" stop-color="{a}" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{BG}"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#g)">
  <animate attributeName="opacity" values="1;.5;1" dur="6s" repeatCount="indefinite"/>
</rect>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" stroke="{BORDER}"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" stroke="{a}" stroke-width="1.6" stroke-linecap="round"
      stroke-dasharray="140 {perim - 140}" stroke-opacity=".9">
  <animate attributeName="stroke-dashoffset" from="0" to="-{perim}" dur="7s" repeatCount="indefinite"/>
</rect>
<g class="fade-up" style="animation-delay:.1s">
  <rect x="28" y="26" width="44" height="44" rx="11" fill="{a}" fill-opacity=".12" stroke="{a}" stroke-opacity=".45"/>
  <text class="mono" x="50" y="54" font-size="17" font-weight="700" fill="{a}" text-anchor="middle">{x(p["glyph"])}</text>
  <text class="sans" x="86" y="47" font-size="22" font-weight="700" fill="{TEXT}" letter-spacing="-.3">{x(p["name"])}</text>
  <text class="sans" x="86" y="67" font-size="13.5" fill="{MUTED}">{x(p["tagline"])}</text>
  <rect x="{W - 28 - bw}" y="26" width="{bw}" height="24" rx="12" fill="{a}" fill-opacity=".14"/>
  <text class="sans" x="{W - 28 - bw / 2}" y="42" font-size="12" font-weight="600" fill="{a}" text-anchor="middle">{x(p["badge"])}</text>
</g>
{bullets}
<g class="fade-in" style="animation-delay:.9s">{''.join(pills)}</g>
"""
    return svg(W, H, body, title=f'{p["name"]} — {p["tagline"]}')


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1200, 110
    msg = 'echo "Thanks for stopping by. Let\'s build something."'
    cw = 9.6
    start = 60 + 2 * cw
    body = f"""
<defs>{typed_clip("t", start, 30, len(msg), cw, 30, .4, 2.6)}</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="{BG}" stroke="{BORDER}"/>
<text class="mono" x="60" y="52" font-size="16" fill="{GREEN}">$</text>
<text class="mono" x="{start}" y="52" font-size="16" fill="{TEXT}" clip-path="url(#t)">{x(msg)}</text>
<rect x="{start + len(msg) * cw + 4}" y="38" width="9" height="18" fill="{GREEN}" style="animation: blink 1s step-end infinite;"/>
<text class="mono fade-in" style="animation-delay:3.2s" x="60" y="82" font-size="14" fill="{MUTED}">→ camiloraphaelzuletawolff@gmail.com  ·  linkedin.com/in/camilo-raphael-zuleta-wolff</text>
"""
    return svg(W, H, body, title="Thanks for stopping by")


def main():
    OUT.mkdir(exist_ok=True)
    files = {"header.svg": header(), "metrics.svg": metrics(), "timeline.svg": timeline(), "footer.svg": footer()}
    for p in PROJECTS:
        files[f'card-{p["slug"]}.svg'] = card(p)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
