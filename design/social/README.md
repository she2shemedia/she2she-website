# She2She social graphics builder

Renders She2She Media's Instagram, Facebook and LinkedIn graphics (1080 x 1350) in the
current brand style, from a small JSON spec. Used by the weekly social drafting run.

Style (October 2026 onward): magenta top field with torn white paper, a single white wavy
line top right, lilac waves bottom right, black hatch bottom left, Gloock headlines, Poppins
body text, round She2She wordmark badge. No teal, no emoji.

## Run it

```
pip install playwright pillow   # Chromium must be available to Playwright
python3 design/social/build.py spec.json out/
```

Output per post: `<name>.png` for a single graphic, or `<name>_01.png`, `_02.png`, ... plus
`<name>_LinkedIn.pdf` for a carousel. `out/contact_sheet.png` shows the whole week, one row
per post.

## Spec format

See `example-spec.json`. Name posts `YYYY-MM-DD_short-slug`. Wrap a word in `**double
asterisks**` to highlight it (magenta on white slides, black on magenta covers).

Slide types:

| type | fields | use |
| --- | --- | --- |
| `text_cover` | label, title, sub | single graphic with no photo |
| `tcover` | label, title, sub | first slide of a carousel |
| `cover` | photo (path to .jpg), title | carousel cover with a photo |
| `inner` | num, title, body, example (optional [label, text]) | numbered carousel slide |
| `missing` | title, items, body | checklist with question marks |
| `headline_card` | tag, quote, note, after, button | before/after or quote card |
| `recap` | title, items, cta | closing checklist slide |
| `closer` | title, body | closing line with logo |
| `poll` | label, title, options, sub | single poll graphic |

Carousels: 5 to 8 slides. Keep text clear of the 48 px edge; long titles wrap automatically.
Writing rules for anything on a graphic live in the She2She Media project doc
`claude/writing-style-rules.md`.
