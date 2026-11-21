"""Render a week of She2She social graphics from a JSON spec.

Usage:
    python3 design/social/build.py spec.json OUT_DIR

Writes, for each post: <name>.png (single graphic) or <name>_01.png ... (carousel)
plus <name>_LinkedIn.pdf for carousels, and OUT_DIR/contact_sheet.png showing every
slide of the week. See README.md for the spec format.
"""
import json, re, sys, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import s2s_social as s

def mark(t, on_magenta=False):
    """**word** -> highlight: magenta on paper slides, black on magenta covers. HTML allowed."""
    hl = (lambda w: f"<span style='color:#000'>{w}</span>") if on_magenta else s.M
    return re.sub(r"\*\*(.+?)\*\*", lambda m: hl(m.group(1)), t or "")

def slide_html(sl, n, seed):
    t = sl["type"]
    on_mag = t in ("text_cover", "tcover", "poll", "recap")
    g = lambda k, d="": mark(sl.get(k, d), on_mag and k == "title")
    if t == "text_cover":   # single graphic, no slide number
        return s.text_cover(sl.get("label", ""), g("title"), g("sub"), seed, strike=sl.get("strike", False))
    if t == "tcover":       # carousel cover without a photo
        return s.tcover(sl.get("label", ""), g("title"), g("sub"), n, seed)
    if t == "cover":        # carousel cover with a photo (path to a .jpg)
        return s.cover(sl["photo"], g("title"), n, seed)
    if t == "inner":
        ex = sl.get("example")
        return s.inner(sl["num"], g("title"), g("body"), n, seed, ex=(ex[0], mark(ex[1])) if ex else None)
    if t == "missing":
        return s.missing(g("title"), [mark(i) for i in sl["items"]], g("body"), n, seed)
    if t == "headline_card":
        return s.headline_card(sl.get("tag", ""), g("quote"), g("note"), n, seed, after=sl.get("after", False), button=sl.get("button"))
    if t == "recap":
        return s.recap(g("title"), [mark(i) for i in sl["items"]], g("cta"), n, seed)
    if t == "closer":
        return s.closer(g("title"), g("body"), n, seed)
    if t == "poll":
        return s.poll(sl.get("label", ""), g("title"), [mark(o) for o in sl["options"]], g("sub"), seed)
    raise ValueError(f"unknown slide type: {t}")

def main(spec_path, out_dir):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    made = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": s.W, "height": s.H})
        for pi, post in enumerate(spec["posts"]):
            slides = post["slides"]; total = len(slides); files = []
            for i, sl in enumerate(slides, 1):
                n = f"{i}/{total}" if total > 1 else None
                pg.set_content(slide_html(sl, n, 100 * (pi + 1) + i)); pg.evaluate("document.fonts.ready")
                fn = out / (f"{post['name']}_{i:02d}.png" if total > 1 else f"{post['name']}.png")
                pg.screenshot(path=str(fn)); files.append(fn); print(fn.name)
            if total > 1:
                ims = [Image.open(f).convert("RGB") for f in files]
                pdf = out / f"{post['name']}_LinkedIn.pdf"
                ims[0].save(pdf, save_all=True, append_images=ims[1:], resolution=150); print(pdf.name)
            made.append(files)
        b.close()
    # contact sheet: one row per post
    w, h, gap = 240, 300, 10
    cols = max(len(f) for f in made)
    sheet = Image.new("RGB", (cols * (w + gap) + gap, len(made) * (h + gap) + gap), "white")
    for r, files in enumerate(made):
        for c, f in enumerate(files):
            sheet.paste(Image.open(f).convert("RGB").resize((w, h)), (gap + c * (w + gap), gap + r * (h + gap)))
    sheet.save(out / "contact_sheet.png"); print("contact_sheet.png")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
