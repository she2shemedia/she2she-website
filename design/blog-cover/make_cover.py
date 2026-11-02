"""Build a She2She blog cover.

Usage (from the repo root):
  python3 design/blog-cover/make_cover.py PHOTO "Title line one" "Title line two" OUTPUT.jpg

Places the photo inside the torn-paper frame of template.png, adds the title in
Poppins Bold (black, centered, two lines), the She2She wordmark bottom right,
and saves a 940 x 788 .jpg (the size the blog displays).
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as nd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
W, H = 940, 788

def frame_mask(tpl):
    """Pixels of the placeholder 'window' (sky, hills, cloud) in the template."""
    a = np.asarray(tpl.convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    sky = (b > r + 8) & (b >= g)                 # pale blue sky
    hills = (g > r + 10) & (g > b + 10)          # greens
    m = sky | hills
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    m &= (xx < a.shape[1] * 0.72) & (yy < a.shape[0] * 0.70)
    m = nd.binary_closing(m, np.ones((5, 5)), iterations=2)
    lab, n = nd.label(m)
    sizes = nd.sum(m, lab, range(1, n + 1))
    m = lab == (np.argmax(sizes) + 1)
    # add the white cloud (near-white blob near the top of the frame)
    white = (a.min(2) > 235)
    xs = np.nonzero(m.any(0))[0]
    band = np.zeros_like(white)
    band[: int(a.shape[0] * 0.30), xs.min(): xs.max() + 1] = True
    wl, wn = nd.label(white & band)
    for i in range(1, wn + 1):
        blob = wl == i
        if blob.sum() > 500 and nd.binary_dilation(blob, iterations=3)[m].any():
            m |= blob
    # fill each column between its top and bottom edge (covers the white cloud)
    out = np.zeros_like(m)
    for x in np.nonzero(m.any(0))[0]:
        ys = np.nonzero(m[:, x])[0]
        out[ys.min():ys.max() + 1, x] = True
    return out

def cover_fit(photo, bw, bh, focus_y=0.35):
    s = max(bw / photo.width, bh / photo.height)
    p = photo.resize((round(photo.width * s), round(photo.height * s)), Image.LANCZOS)
    x0 = (p.width - bw) // 2
    y0 = int((p.height - bh) * focus_y)
    return p.crop((x0, y0, x0 + bw, y0 + bh))

def main(photo_path, line1, line2, out_path):
    tpl = Image.open(os.path.join(HERE, "template.png")).convert("RGB").resize((W, H), Image.LANCZOS)
    m = frame_mask(tpl)
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    photo = Image.open(photo_path).convert("RGB")
    fitted = cover_fit(photo, x1 - x0, y1 - y0)
    canvas = tpl.copy()
    alpha = Image.fromarray((m[y0:y1, x0:x1] * 255).astype("uint8")).filter(
        __import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(0.6))
    canvas.paste(fitted, (x0, y0), alpha)

    d = ImageDraw.Draw(canvas)
    cx = 349
    longest = max(line1, line2, key=len)
    size = 40
    font = ImageFont.truetype(os.path.join(HERE, "Poppins-Bold.ttf"), size)
    while d.textlength(longest, font=font) > 590 and size > 26:
        size -= 1
        font = ImageFont.truetype(os.path.join(HERE, "Poppins-Bold.ttf"), size)
    for text, y in ((line1, 569), (line2, 627)):
        d.text((cx, y), text, font=font, fill=(0, 0, 0), anchor="ms")

    logo = Image.open(os.path.join(ROOT, "public/images/she2she-wordmark.png")).convert("RGBA")
    lw = 160
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    canvas.paste(logo, (566, 711 - logo.height // 2), logo)

    canvas.save(out_path, quality=92)
    print("saved", out_path)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:])
