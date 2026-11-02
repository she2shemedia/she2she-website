# She2She blog cover builder

This folder isn't part of the live site. It holds what any Claude session needs to build a blog cover once Anita sends the photo she made in ChatGPT.

- `template.png` – the cover template (torn-paper frame, magenta #CB328D, lilac waves, black stripes, she2shemedia.com), with colors matched to the published covers.
- `Poppins-Bold.ttf` – the title font.
- The logo comes from `public/images/she2she-wordmark.png` (the Gloock/Poppins wordmark, no crescent).
- `make_cover.py` – builds the cover.

## How to build a cover

From the repo root (needs Pillow, numpy and scipy: `pip install --break-system-packages pillow numpy scipy`):

```
python3 design/blog-cover/make_cover.py PHOTO.jpg "Title line one" "Title line two" public/images/blog/<post-file-name>.jpg
```

- The photo fills the torn-paper frame (cropped to fit, keeping the upper part of the photo, where faces usually are).
- The title goes in bold black Poppins, centered over two lines. Long lines shrink automatically to fit.
- The wordmark goes bottom right, and the output is a 940 x 788 .jpg.
- The two title lines are in the pull request description for each post.

Then show Anita a preview, and once she's happy, commit the image to that post's `claude/blog-` branch so it's part of the same pull request. Don't merge; Anita merges to publish.
