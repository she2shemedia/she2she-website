"""She2She Media social graphics library (1080 x 1350).

Matches the She2She blog-graphic style: magenta field, torn white paper,
single white wavy line, lilac waves, black hatch, Gloock headlines, Poppins body,
round wordmark badge. Used by build.py; see README.md.
"""
import base64, pathlib, random

HERE = pathlib.Path(__file__).resolve().parent
F = HERE / "fonts"; A = HERE / "assets"
def b64(p): return base64.b64encode(p.read_bytes()).decode()
def uri(p, mime): return f"data:{mime};base64,{b64(p)}"
LOGO = uri(A / "badge.svg", "image/svg+xml")

MAG, LILAC, TEAL = "#CA328D", "#D6AACD", "#000000"
W, H = 1080, 1350

CSS = "".join(f"@font-face{{font-family:'Poppins';font-weight:{w};src:url({uri(F/f'poppins-latin-{w}-normal.woff2','font/woff2')}) format('woff2')}}" for w in (400, 600, 700)) + f"@font-face{{font-family:'Gloock';font-weight:400;src:url({uri(F/'gloock-latin-400-normal.woff2','font/woff2')}) format('woff2')}}" + f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px}}
body{{font-family:'Poppins',Arial,sans-serif;color:#000;background:{MAG};position:relative;overflow:hidden}}
svg.bg{{position:absolute;inset:0}}
.abs{{position:absolute}}
.h{{font-family:'Gloock',Georgia,serif;font-weight:400;letter-spacing:0}}
.url{{font-size:30px;font-weight:600;color:#000}}
.n{{font-size:26px;font-weight:600;color:#000;background:#fff;border:2px solid {MAG};border-radius:999px;padding:2px 18px}}
.logo{{width:200px;height:200px;border-radius:50%;background:#fff}}
"""

def rnd(seed): r = random.Random(seed); return r

def torn_h(x0, x1, y, amp, r, step=(6, 16), slope=0.0):
    pts, x = [], x0
    while x < x1:
        pts.append((x, y + slope * (x - x0) + r.uniform(-amp, amp))); x += r.uniform(*step)
    pts.append((x1, y + slope * (x1 - x0)))
    return pts

def torn_rect(x, y, w, h, amp, r):
    top = torn_h(x, x + w, y, amp, r)
    right = [(x + w + r.uniform(-amp, amp), yy) for yy in range(int(y), int(y + h), 14)]
    bot = [(px, py) for px, py in torn_h(x, x + w, y + h, amp * 1.6, r)][::-1]
    left = [(x + r.uniform(-amp, amp), yy) for yy in range(int(y + h), int(y), -14)]
    return top + right + bot + left

def poly(pts): return " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)

DEFS = """<defs>
<filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="4"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.35 -0.12"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<filter id="shadow"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-opacity=".18"/></filter>
</defs>"""

def scribbles(x, y, s=1.0, color="#fff", op=.85):
    # single flowing line, matched to the blog graphics (Oct 2026)
    paths = ["M40,-40 C20,20 110,50 95,110 C82,165 150,195 215,168 C285,140 300,215 365,222 C415,228 425,268 465,300"]
    return f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{color}" stroke-width="{3/s:.1f}" opacity="{op}" stroke-linecap="round">' + "".join(f'<path d="{d}"/>' for d in paths) + "</g>"

def waves(x, y, n=5, color=LILAC, sw=11, gap=34, length=430):
    out = []
    for i in range(n):
        ox = x + i * gap
        out.append(f'<path d="M{ox},{y} c-40,{length*.22} 50,{length*.3} 10,{length*.52} s-50,{length*.28} -10,{length*.5}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
    return "".join(out)

def hatch(x, y, n=9, color=TEAL):
    return "".join(f'<line x1="{x+i*26}" y1="{y+56}" x2="{x+i*26+40}" y2="{y}" stroke="{color}" stroke-width="5" stroke-linecap="round"/>' for i in range(n))

def brush(x, y, w):
    return f'<path d="M{x},{y+6} C{x+w*.3},{y-4} {x+w*.7},{y-2} {x+w},{y-8}" fill="none" stroke="{MAG}" stroke-width="9" stroke-linecap="round"/><path d="M{x+20},{y+12} C{x+w*.35},{y+4} {x+w*.6},{y+5} {x+w-60},{y}" fill="none" stroke="{MAG}" stroke-width="4" stroke-linecap="round" opacity=".7"/>'

def paper_poly(y, r, slope=0.03):
    edge = torn_h(-10, W + 10, y, 9, r, slope=slope)
    return poly(edge + [(W + 10, H + 10), (-10, H + 10)])

def doc(svg, html, seed=1):
    return f'<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body><svg class="bg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}{svg}</svg>{html}</body></html>'

def footer(n=None, logo=True, url=True):
    h = ""
    if url: h += f'<div class="abs url" style="left:64px;bottom:96px">she2shemedia.com</div>'
    if n: h += f'<div class="abs n" style="right:64px;bottom:56px">{n}</div>'
    if logo: h += f'<img class="abs logo" style="right:150px;bottom:40px" src="{LOGO}">' if not n else ""
    return h

def cover(photo, title, n, seed, sub=None, lines=2):
    """Photo cover: magenta field, torn photo top-left, torn paper bottom, Poppins headline."""
    r = rnd(seed)
    ph = uri(A / photo, "image/jpeg")
    rect = torn_rect(80, 64, 700, 600, 5, r)
    border = torn_rect(66, 50, 728, 628, 8, rnd(seed + 9))
    paper_y = 760
    svg = (scribbles(720, 30, 1.0) +
           f'<polygon points="{poly(border)}" fill="#fff"/>' +
           f'<clipPath id="ph"><polygon points="{poly(rect)}"/></clipPath>' +
           f'<image href="{ph}" x="80" y="64" width="700" height="600" preserveAspectRatio="xMidYMid slice" clip-path="url(#ph)"/>' +
           f'<polygon points="{paper_poly(paper_y, r)}" fill="#fff"/>' +
           f'<polygon points="{paper_poly(paper_y, rnd(seed))}" fill="#fff" filter="url(#paper)" opacity=".5"/>' +
           waves(880, 1010, n=4) + hatch(40, 1282))
    bsvg = f'<svg width="470" height="24" style="display:block;margin:6px 0 0 auto;overflow:visible"><g transform="translate(0,12)">{brush(0, 0, 470)}</g></svg>'
    html = (f'<div class="abs" style="left:48px;width:800px;top:830px;display:flex;flex-direction:column;align-items:center;gap:14px">'
            f'<div class="h" style="font-size:62px;line-height:72px;text-align:center">{title}</div>{bsvg}'
            f'<div class="url" style="margin-top:6px">she2shemedia.com</div></div>' +
            f'<img class="abs logo" style="right:150px;bottom:44px" src="{LOGO}">' +
            (f'<div class="abs n" style="left:64px;bottom:96px">{n}</div>' if n else ""))
    return doc(svg, html)

def text_cover(label, title, sub, seed, logo=True, strike=False):
    """No-photo single: big white headline on magenta, torn paper with the subline."""
    r = rnd(seed)
    svg = (scribbles(640, 20, 1.1) + f'<polygon points="{paper_poly(820, r, -0.02)}" fill="#fff"/>' +
           f'<polygon points="{paper_poly(820, rnd(seed))}" fill="#fff" filter="url(#paper)" opacity=".5"/>' +
           waves(860, 940) + hatch(40, 1282))
    deco = "text-decoration:line-through;text-decoration-thickness:6px;text-decoration-color:#000;" if strike else ""
    html = (f'<div class="abs" style="left:80px;top:150px;background:#fff;color:{MAG};font-weight:700;font-size:30px;letter-spacing:.1em;text-transform:uppercase;border-radius:999px;padding:10px 30px">{label}</div>' +
            f'<div class="abs h" style="left:80px;right:120px;top:250px;font-size:{100 if len(title)<40 else 80}px;line-height:{112 if len(title)<40 else 92}px;color:#fff;{deco}">{title}</div>' +
            f'<div class="abs" style="left:80px;right:300px;top:930px;font-size:46px;line-height:62px;font-weight:600">{sub}</div>' +
            f'<img class="abs logo" style="right:150px;bottom:44px" src="{LOGO}">' +
            f'<div class="abs url" style="left:80px;bottom:96px">she2shemedia.com</div>')
    return doc(svg, html)

def inner(num, title, body, n, seed, ex=None):
    """Inner slide: textured paper, torn magenta band on top, number + title + body."""
    r = rnd(seed)
    band = torn_h(-10, W + 10, 150, 9, r, slope=0.015)
    svg = (f'<rect width="{W}" height="{H}" fill="#fff"/><rect width="{W}" height="{H}" fill="#fff" filter="url(#paper)" opacity=".5"/>' +
           f'<polygon points="{poly([(-10,-10),(W+10,-10)] + band[::-1])}" fill="{MAG}"/>' + scribbles(760, -40, .7) +
           waves(930, 1010, n=3, sw=9, gap=30, length=330) + hatch(40, 1282, n=6))
    exh = (f'<div style="border:3px solid {MAG};border-radius:24px;padding:28px 36px;font-size:36px;line-height:50px;background:#fff">'
           f'<div style="font-weight:700;color:{MAG};font-size:26px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px">{ex[0]}</div>{ex[1]}</div>') if ex else ""
    html = (f'<div class="abs" style="left:80px;right:120px;top:200px;bottom:170px;display:flex;flex-direction:column;justify-content:center;gap:34px">'
            f'<div class="h" style="font-size:150px;line-height:140px;color:{MAG}">{num}</div>'
            f'<div class="h" style="font-size:76px;line-height:88px">{title}</div>'
            f'<div style="width:220px;height:8px;border-radius:4px;background:{MAG};margin-top:-12px"></div>'
            f'<div style="font-size:44px;line-height:62px">{body}</div>{exh}</div>' + footer(n))
    return doc(svg, html)

def recap(title, items, cta, n, seed):
    r = rnd(seed)
    svg = (f'<polygon points="{paper_poly(330, r, 0.01)}" fill="#fff"/>' + f'<polygon points="{paper_poly(330, rnd(seed))}" fill="#fff" filter="url(#paper)" opacity=".5"/>' +
           scribbles(700, 0, .8) + waves(900, 960, n=4) + hatch(40, 1282, n=6))
    lis = "".join(f'<div style="display:flex;gap:24px;align-items:center;font-size:46px;line-height:58px;font-weight:600"><span style="flex:none;width:56px;height:56px;border-radius:50%;background:{MAG};color:#fff;font-size:30px;display:flex;align-items:center;justify-content:center">✓</span>{t}</div>' for t in items)
    html = (f'<div class="abs h" style="left:80px;right:80px;top:130px;font-size:78px;line-height:90px;color:#fff">{title}</div>' +
            f'<div class="abs" style="left:80px;right:300px;top:420px;display:flex;flex-direction:column;gap:30px">{lis}</div>' +
            f'<div class="abs" style="left:80px;top:1010px;background:{MAG};color:#fff;border-radius:999px;padding:20px 42px;font-size:34px;font-weight:700">{cta}</div>' +
            f'<img class="abs logo" style="right:150px;bottom:44px" src="{LOGO}">' + f'<div class="abs url" style="left:80px;bottom:96px">she2shemedia.com</div>' +
            f'<div class="abs n" style="left:440px;bottom:92px">{n}</div>')
    return doc(svg, html)

def closer(title_html, body, n, seed):
    r = rnd(seed)
    svg = (f'<rect width="{W}" height="{H}" fill="#fff"/><rect width="{W}" height="{H}" fill="#fff" filter="url(#paper)" opacity=".5"/>' +
           f'<polygon points="{poly([(-10,-10),(W+10,-10)] + torn_h(-10, W+10, 150, 9, r, slope=0.015)[::-1])}" fill="{MAG}"/>' + scribbles(760, -40, .7) +
           waves(880, 900) + hatch(40, 1282))
    html = (f'<div class="abs" style="left:80px;right:140px;top:200px;bottom:300px;display:flex;flex-direction:column;justify-content:center;gap:44px">'
            f'<div class="h" style="font-size:96px;line-height:110px">{title_html}</div>'
            f'<div style="font-size:46px;line-height:64px;padding-right:120px">{body}</div></div>' +
            f'<img class="abs logo" style="right:150px;bottom:44px" src="{LOGO}">' + f'<div class="abs url" style="left:80px;bottom:96px">she2shemedia.com</div>' +
            f'<div class="abs n" style="left:440px;bottom:92px">{n}</div>')
    return doc(svg, html)

M = lambda t: f"<span style='color:{MAG}'>{t}</span>"

def tcover(label, title, sub, n, seed):
    """Text cover with a slide-number pill, for carousels."""
    h = text_cover(label, title, sub, seed)
    return h.replace("</body>", f'<div class="abs n" style="left:440px;bottom:92px">{n}</div></body>')

def paper_page(seed):
    r = rnd(seed)
    band = torn_h(-10, W + 10, 150, 9, r, slope=0.015)
    return (f'<rect width="{W}" height="{H}" fill="#fff"/><rect width="{W}" height="{H}" fill="#fff" filter="url(#paper)" opacity=".5"/>' +
            f'<polygon points="{poly([(-10,-10),(W+10,-10)] + band[::-1])}" fill="{MAG}"/>' + scribbles(760, -40, .7) +
            waves(930, 1010, n=3, sw=9, gap=30, length=330) + hatch(40, 1282, n=6))

def headline_card(tag, quote, note, n, seed, after=False, button=None):
    box = (f"background:{MAG};color:#fff;" if after else "background:#fff;color:rgba(0,0,0,.62);border:4px dashed rgba(0,0,0,.35);")
    btn = (f'<div style="margin-top:34px"><span style="display:inline-block;background:#fff;color:{MAG};border-radius:999px;padding:14px 34px;font-size:32px;font-weight:700">{button}</span></div>' if button else "")
    tagc = f"background:{MAG};color:#fff" if after else "background:#000;color:#fff"
    html = (f'<div class="abs" style="left:80px;right:120px;top:210px;bottom:180px;display:flex;flex-direction:column;justify-content:center;gap:40px">'
            f'<div><span style="display:inline-block;{tagc};font-weight:700;font-size:30px;letter-spacing:.1em;text-transform:uppercase;border-radius:999px;padding:10px 30px">{tag}</span></div>'
            f'<div style="{box}border-radius:24px;padding:56px 52px"><div class="h" style="font-size:66px;line-height:80px">{quote}</div>{btn}</div>'
            f'<div style="font-size:42px;line-height:58px">{note}</div></div>' + footer(n))
    return doc(paper_page(seed), html)

def missing(title, items, body, n, seed):
    lis = "".join(f'<div style="display:flex;gap:26px;align-items:center;font-size:52px;line-height:64px;font-weight:600"><span style="flex:none;width:72px;height:72px;border-radius:50%;border:4px solid {MAG};color:{MAG};font-size:40px;font-weight:700;display:flex;align-items:center;justify-content:center">?</span>{t}</div>' for t in items)
    html = (f'<div class="abs" style="left:80px;right:120px;top:210px;bottom:180px;display:flex;flex-direction:column;justify-content:center;gap:44px">'
            f'<div class="h" style="font-size:76px;line-height:88px">{title}</div>'
            f'<div style="width:220px;height:8px;border-radius:4px;background:{MAG};margin-top:-20px"></div>'
            f'<div style="display:flex;flex-direction:column;gap:30px">{lis}</div>'
            f'<div style="font-size:42px;line-height:58px">{body}</div></div>' + footer(n))
    return doc(paper_page(seed), html)

def poll(label, title, opts, sub, seed):
    r = rnd(seed)
    svg = (scribbles(640, 20, 1.1) + f'<polygon points="{paper_poly(610, r, -0.02)}" fill="#fff"/>' +
           f'<polygon points="{paper_poly(610, rnd(seed))}" fill="#fff" filter="url(#paper)" opacity=".5"/>' +
           waves(880, 1000, n=4) + hatch(40, 1282))
    pills = "".join(f'<div style="display:flex;gap:22px;align-items:center;border:4px solid {MAG};border-radius:999px;padding:10px 32px 10px 12px;font-size:38px;font-weight:600;background:#fff"><span style="flex:none;width:58px;height:58px;border-radius:50%;background:{MAG};color:#fff;font-size:30px;font-weight:700;display:flex;align-items:center;justify-content:center">{i}</span>{o}</div>' for i, o in enumerate(opts, 1))
    html = (f'<div class="abs" style="left:80px;top:130px;background:#fff;color:{MAG};font-weight:700;font-size:30px;letter-spacing:.1em;text-transform:uppercase;border-radius:999px;padding:10px 30px">{label}</div>' +
            f'<div class="abs h" style="left:80px;right:120px;top:215px;font-size:80px;line-height:92px;color:#fff">{title}</div>' +
            f'<div class="abs" style="left:80px;right:330px;top:660px;display:flex;flex-direction:column;gap:16px;align-items:flex-start">{pills}</div>' +
            f'<div class="abs" style="left:80px;right:330px;top:1100px;font-size:34px;line-height:46px;font-weight:600">{sub}</div>' +
            f'<img class="abs logo" style="right:150px;bottom:44px" src="{LOGO}">' +
            f'<div class="abs url" style="left:80px;bottom:96px">she2shemedia.com</div>')
    return doc(svg, html)

GBLUE = "#1A0DAB"
def serp(label, title, sub, n, seed):
    """Mock Google result: before/after page titles."""
    svg = paper_page(seed)
    def card(tag, ttl, before):
        st = ("border:3px dashed rgba(0,0,0,.3);opacity:.75;" if before else f"border:3px solid {MAG};box-shadow:0 10px 30px rgba(0,0,0,.10);")
        tc = "color:#5f6368;text-decoration:line-through;text-decoration-thickness:3px;" if before else f"color:{GBLUE};"
        tagc = "background:#000;color:#fff" if before else f"background:{MAG};color:#fff"
        return (f'<div style="position:relative;background:#fff;border-radius:24px;padding:30px 36px;{st}">'
                f'<span style="position:absolute;top:-22px;left:28px;{tagc};font-weight:700;font-size:24px;letter-spacing:.1em;text-transform:uppercase;border-radius:999px;padding:6px 20px">{tag}</span>'
                f'<div style="display:flex;align-items:center;gap:16px;margin-top:6px"><span style="width:44px;height:44px;border-radius:50%;background:#f1f3f4;display:flex;align-items:center;justify-content:center;font-size:22px;color:#5f6368;font-weight:600">B</span>'
                f'<div style="font-size:26px;line-height:32px;color:#202124">Bloom &amp; Co.<br><span style="color:#5f6368;font-size:22px">https://www.bloomandco.com</span></div></div>'
                f'<div style="font-family:Arial,sans-serif;font-size:44px;line-height:54px;margin-top:14px;{tc}">{ttl}</div>'
                f'<div style="font-family:Arial,sans-serif;font-size:24px;line-height:34px;color:#4d5156;margin-top:6px">Wedding and event flowers, designed around your day...</div></div>')
    html = (f'<div class="abs" style="left:80px;right:110px;top:200px;bottom:250px;display:flex;flex-direction:column;justify-content:center;gap:46px">'
            f'<div><span style="display:inline-block;background:{MAG};color:#fff;font-weight:700;font-size:28px;letter-spacing:.1em;text-transform:uppercase;border-radius:999px;padding:8px 26px">{label}</span></div>'
            f'<div class="h" style="font-size:80px;line-height:88px;margin-top:-20px">{title}</div>'
            + card("Before", "Home", True) + card("After", "Wedding Florist in Raleigh | Bloom &amp; Co.", False) +
            f'<div style="font-size:38px;line-height:52px;font-weight:600">{sub}</div></div>'
            f'<img class="abs logo" style="right:150px;bottom:44px" src="{LOGO}">'
            f'<div class="abs url" style="left:80px;bottom:96px">she2shemedia.com</div>')
    return doc(svg, html)


WM = uri(A / "wordmark.svg", "image/svg+xml")
def slide(num, title, inner_html, n, seed):
    html = (f'<div class="abs" style="left:80px;right:110px;top:200px;bottom:180px;display:flex;flex-direction:column;justify-content:center;gap:34px">'
            f'<div class="h" style="font-size:120px;line-height:110px;color:{MAG}">{num}</div>'
            f'<div class="h" style="font-size:76px;line-height:86px">{title}</div>'
            f'<div style="width:220px;height:8px;border-radius:4px;background:{MAG};margin-top:-12px"></div>{inner_html}</div>' + footer(n))
    return doc(paper_page(seed), html)

def rules_list(items):
    return '<div style="display:flex;flex-direction:column;gap:26px">' + "".join(f'<div style="display:flex;gap:24px;align-items:center;font-size:42px;line-height:54px;font-weight:600"><span style="flex:none;width:58px;height:58px;border-radius:50%;background:{MAG};color:#fff;font-size:30px;display:flex;align-items:center;justify-content:center">✓</span>{t}</div>' for t in items) + '</div>'

