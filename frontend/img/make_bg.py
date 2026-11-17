"""Sinh bg-light.svg và bg-dark.svg (nền dashboard). Sửa màu/bố cục ở đây rồi chạy: py make_bg.py
Ý tưởng từ bg-logistics.svg: mạng tuyến vận chuyển + hub đỏ + kiện hàng, thêm máy chia chọn vòng, cổng quét BCR,
kiện hàng chạy trên tuyến. Giữa màn hình làm mờ (mask) để không lấn nội dung."""
from pathlib import Path

THEMES = {
    "dark": dict(base="#0f1115", dot="#ffffff", dot_o=.08, line="#8e9bb5", link_o=.28, trace_o=.36, red="#ee1c3f",
                 route_o=.62, glow_red=.30, blue="#3b5b9a", glow_blue=.26, face=("#252b38", "#1c212b", "#303746"),
                 edge="#aab5ca", edge_o=.55, node_o=.70, belt_o=.40, beam_o=.75),
    "light": dict(base="#f4f5f7", dot="#1d2433", dot_o=.12, line="#4b5263", link_o=.28, trace_o=.34, red="#ee0033",
                  route_o=.50, glow_red=.12, blue="#2a78d6", glow_blue=.10, face=("#ffffff", "#dde1e8", "#eef0f4"),
                  edge="#5b6478", edge_o=.70, node_o=.70, belt_o=.38, beam_o=.50),
}

HUBS = [(150, 230), (110, 700), (1160, 180), (1600, 520), (1050, 640)]
NODES = [(420, 120), (330, 470), (470, 860), (760, 300), (1500, 110), (1790, 250), (1830, 740), (1420, 880), (700, 700)]
EDGES = [  # (từ, đến, độ cong link, độ cong route hoặc None)
    ((150, 230), (420, 120), (272, 143), (305, 224)), ((150, 230), (330, 470), (269, 328), None),
    ((330, 470), (110, 700), (248, 611), (179, 545)), ((110, 700), (470, 860), (309, 737), None),
    ((420, 120), (760, 300), (612, 169), (558, 271)), ((330, 470), (760, 300), (525, 333), None),
    ((760, 300), (1160, 180), (946, 192), (982, 312)), ((1160, 180), (1500, 110), (1322, 104), None),
    ((1500, 110), (1790, 250), (1662, 145), (1620, 232)), ((1790, 250), (1600, 520), (1727, 408), None),
    ((1600, 520), (1830, 740), (1741, 602), (1675, 671)), ((1830, 740), (1420, 880), (1642, 859), None),
    ((1600, 520), (1160, 180), (1339, 403), (1441, 271)), ((1420, 880), (1050, 640), (1206, 804), None),
    ((1050, 640), (700, 700), (882, 712), (864, 607)), ((700, 700), (470, 860), (604, 808), None),
    ((330, 470), (700, 700), (543, 541), (474, 652)), ((1050, 640), (1600, 520), (1311, 514), None),
]
# (x, y, cỡ, độ đậm, có băng keo đỏ)
BOXES = [(30, 330, 34, .95, True), (75, 353, 22, .75, False), (1660, 390, 30, .95, True), (1700, 412, 20, .75, False),
         (60, 560, 18, .6, False), (1820, 560, 16, .6, False), (1700, 760, 26, .85, True), (1728, 774, 18, .7, False),
         (1712, 738, 18, .7, False), (190, 860, 24, .8, True), (560, 175, 16, .45, False), (1350, 300, 14, .45, False)]


def box(x, y, s, op, tape, t):
    h = s * .62
    f1, f2, f3 = t["face"]
    tape_line = (f'<path d="M{x + s / 2},{y - s / 4} l{s},{s / 2}" stroke="{t["red"]}" stroke-opacity=".55" stroke-width="1.6"/>'
                 if tape else "")
    return (f'<g class="box" opacity="{op}">'
            f'<path d="M{x},{y} l{s},{s / 2} l0,{h} l{-s},{-s / 2} z" fill="{f1}"/>'
            f'<path d="M{x + s},{y + s / 2} l{s},{-s / 2} l0,{h} l{-s},{s / 2} z" fill="{f2}"/>'
            f'<path d="M{x},{y} l{s},{-s / 2} l{s},{s / 2} l{-s},{s / 2} z" fill="{f3}"/>{tape_line}</g>')


def svg(t):
    o = []
    a = o.append
    a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">')
    a(f'''<defs>
<radialGradient id="gRed" cx="86%" cy="6%" r="58%"><stop offset="0" stop-color="{t["red"]}" stop-opacity="{t["glow_red"]}"/><stop offset="1" stop-color="{t["red"]}" stop-opacity="0"/></radialGradient>
<radialGradient id="gBlue" cx="6%" cy="96%" r="52%"><stop offset="0" stop-color="{t["blue"]}" stop-opacity="{t["glow_blue"]}"/><stop offset="1" stop-color="{t["blue"]}" stop-opacity="0"/></radialGradient>
<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{t["dot"]}" fill-opacity="{t["dot_o"]}"/></pattern>
<linearGradient id="fadeX" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset=".2" stop-color="#fff" stop-opacity=".9"/><stop offset=".36" stop-color="#fff" stop-opacity=".3"/><stop offset=".64" stop-color="#fff" stop-opacity=".3"/><stop offset=".8" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="sides"><rect width="1920" height="1080" fill="url(#fadeX)"/></mask>
<linearGradient id="fadeSoft" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="#fff" stop-opacity=".85"/><stop offset=".5" stop-color="#fff" stop-opacity=".5"/><stop offset=".7" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="soft"><rect width="1920" height="1080" fill="url(#fadeSoft)"/></mask>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["red"]}" stop-opacity="{t["beam_o"]}"/><stop offset="1" stop-color="{t["red"]}" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
</defs>''')
    a(f'''<style>
.link{{fill:none;stroke:{t["line"]};stroke-opacity:{t["link_o"]};stroke-width:1}}
.route{{fill:none;stroke:{t["red"]};stroke-opacity:{t["route_o"]};stroke-width:1.6;stroke-dasharray:6 12;animation:flow 6s linear infinite}}
.route.slow{{animation-duration:10s;stroke-opacity:{t["route_o"] * .7:.2f}}}
.trace{{fill:none;stroke:{t["line"]};stroke-opacity:{t["trace_o"]};stroke-width:1.2}}
.stream{{fill:none;stroke:{t["line"]};stroke-opacity:{t["trace_o"]};stroke-width:1;stroke-dasharray:2 10;animation:flow 4s linear infinite}}
.box path{{stroke:{t["edge"]};stroke-opacity:{t["edge_o"]};stroke-width:1.1;stroke-linejoin:round}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 3.2s ease-out infinite}}
.ring{{fill:none;stroke:{t["line"]};stroke-opacity:{t["link_o"] * 1.4:.2f};transform-box:fill-box;transform-origin:center;animation:spin 60s linear infinite}}
.ring.rev{{animation-direction:reverse;animation-duration:90s}}
.parcel{{animation:move 9s linear infinite;offset-rotate:0deg}}
.carrier{{offset-path:path('M140,945 H1780 A45,45 0 0 1 1780,1035 H140 A45,45 0 0 1 140,945 Z');offset-rotate:auto;animation:move 80s linear infinite}}
.laser{{animation:blink 2.4s ease-in-out infinite}}
@keyframes flow{{to{{stroke-dashoffset:-72}}}}
@keyframes pulse{{0%{{transform:scale(.6);opacity:.55}}100%{{transform:scale(2.4);opacity:0}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes move{{from{{offset-distance:0%}}to{{offset-distance:100%}}}}
@keyframes blink{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>''')
    a(f'<rect width="1920" height="1080" fill="{t["base"]}"/><rect width="1920" height="1080" fill="url(#dots)"/>')
    a('<rect width="1920" height="1080" fill="url(#gRed)"/><rect width="1920" height="1080" fill="url(#gBlue)"/>')
    a('<g mask="url(#sides)">')

    # vòng radar quanh 2 hub chính
    for (cx, cy) in [(1600, 520), (150, 230)]:
        a(f'<circle class="ring" cx="{cx}" cy="{cy}" r="70" stroke-dasharray="3 9"/>')
        a(f'<circle class="ring rev" cx="{cx}" cy="{cy}" r="120" stroke-dasharray="40 14 4 14"/>')
        a(f'<circle class="ring" cx="{cx}" cy="{cy}" r="175" stroke-dasharray="1 7" style="animation-duration:120s"/>')

    # mạng tuyến + kiện hàng chạy trên tuyến đỏ
    for i, ((x1, y1), (x2, y2), (lx, ly), r) in enumerate(EDGES):
        a(f'<path class="link" d="M{x1},{y1} Q{lx},{ly} {x2},{y2}"/>')
        if r:
            d = f"M{x1},{y1} Q{r[0]},{r[1]} {x2},{y2}"
            a(f'<path class="route{" slow" if i % 2 else ""}" d="{d}"/>')
            a(f'<rect class="parcel" x="-4" y="-3" width="8" height="6" rx="1.5" fill="{t["red"]}" fill-opacity=".75" '
              f'style="offset-path:path(\'{d}\');animation-delay:-{i * 1.7 % 9:.1f}s;animation-duration:{8 + i % 4 * 2}s"/>')

    for (x, y) in HUBS:
        a(f'<circle class="pulse" cx="{x}" cy="{y}" r="9" fill="none" stroke="{t["red"]}" stroke-width="1.5" '
          f'style="animation-delay:{HUBS.index((x, y)) * 1.2:.1f}s"/>')
        a(f'<circle cx="{x}" cy="{y}" r="7" fill="{t["red"]}" fill-opacity=".35" filter="url(#glow)"/>')
        a(f'<circle cx="{x}" cy="{y}" r="8" fill="none" stroke="{t["red"]}" stroke-opacity=".6" stroke-width="1.3"/>')
        a(f'<circle cx="{x}" cy="{y}" r="3" fill="{t["red"]}" fill-opacity=".9"/>')
    for (x, y) in NODES:
        a(f'<circle cx="{x}" cy="{y}" r="5" fill="{t["base"]}" stroke="{t["line"]}" stroke-opacity="{t["node_o"]}" stroke-width="1.3"/>')
        a(f'<circle cx="{x}" cy="{y}" r="2" fill="{t["line"]}" fill-opacity="{t["node_o"] + .1}"/>')

    for b in BOXES:
        a(box(*b, t))

    # mạch điện ở các góc + luồng dữ liệu dọc 2 bên
    for d, (ex, ey) in [("M0,60 L90,60 L120,90 L260,90", (260, 90)), ("M0,90 L60,90 L90,120 L90,170", (90, 170)),
                        ("M1920,40 L1860,40 L1830,70 L1830,140", (1830, 140)), ("M1920,70 L1890,70 L1890,190", (1890, 190)),
                        ("M0,880 L40,880 L70,850 L170,850", (170, 850)), ("M1920,860 L1870,860 L1840,830 L1760,830", (1760, 830))]:
        a(f'<path class="trace" d="{d}"/><circle cx="{ex}" cy="{ey}" r="3" fill="{t["base"]}" stroke="{t["line"]}" stroke-opacity=".4"/>')
    for x in (36, 60, 1860, 1884):
        a(f'<path class="stream" d="M{x},250 V800" style="animation-duration:{3 + x % 5}s"/>')
    a('</g>')

    # máy chia chọn vòng ở đáy: đường ray, xe chở hàng, máng (chute), cổng quét BCR
    a(f'<g opacity="{t["belt_o"] * 2.4:.2f}" mask="url(#soft)">')
    a(f'<path d="M140,945 H1780 A45,45 0 0 1 1780,1035 H140 A45,45 0 0 1 140,945 Z" fill="none" stroke="{t["line"]}" '
      f'stroke-opacity=".55" stroke-width="10" stroke-linejoin="round"/>')
    a(f'<path d="M140,945 H1780 A45,45 0 0 1 1780,1035 H140 A45,45 0 0 1 140,945 Z" fill="none" stroke="{t["base"]}" stroke-width="6"/>')
    for x in range(220, 1720, 90):
        a(f'<path d="M{x},1040 l-14,40 M{x + 26},1040 l14,40" stroke="{t["line"]}" stroke-opacity=".35" stroke-width="1.2"/>')
    for k in range(40):
        red = k % 5 == 0
        a(f'<rect class="carrier" x="-10" y="-6" width="20" height="12" rx="2" fill="{t["face"][2]}" '
          f'stroke="{t["red"] if red else t["edge"]}" stroke-opacity="{.8 if red else .5}" style="animation-delay:-{k * 2}s"/>')
    for gx in (520, 1400):
        a(f'<path d="M{gx - 34},1050 V905 H{gx + 34} V1050" fill="none" stroke="{t["line"]}" stroke-opacity=".7" stroke-width="3"/>')
        a(f'<rect x="{gx - 14}" y="899" width="28" height="12" rx="2" fill="{t["face"][1]}" stroke="{t["line"]}" stroke-opacity=".7"/>')
        a(f'<path class="laser" d="M{gx},911 L{gx - 26},1040 H{gx + 26} Z" fill="url(#beam)"/>')
        a(f'<line class="laser" x1="{gx - 26}" y1="990" x2="{gx + 26}" y2="990" stroke="{t["red"]}" stroke-opacity=".9" stroke-width="1.5"/>')
    a('</g>')
    a('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    here = Path(__file__).parent
    for name, t in THEMES.items():
        (here / f"bg-{name}.svg").write_text(svg(t), encoding="utf-8")
        print(name, (here / f"bg-{name}.svg").stat().st_size, "bytes")
