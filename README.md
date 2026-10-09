# She2She Media website

The website for [she2shemedia.com](https://www.she2shemedia.com), built with [Astro](https://astro.build) and hosted on Cloudflare Pages.

## Pages

| Page | File |
| --- | --- |
| Home | `src/pages/index.astro` |
| Services | `src/pages/services.astro` |
| Pricing | `src/pages/pricing.astro` |
| About | `src/pages/about.astro` |
| Work | `src/pages/work.astro` (projects are listed at the top of the file) |
| Book a call | `src/pages/book-online.astro` (Calendly embed) |
| Blog | `src/pages/blog/index.astro`, posts in `src/content/posts/` |
| Legal | `src/pages/privacy.md`, `terms.md`, `disclaimer.md`, `accessibility.md` |

Shared pieces: header and footer in `src/components/`, the page wrapper in `src/layouts/Base.astro`, brand colors at the top of `src/styles/global.css`.

## Brand

- Colors: Magenta `#CA328D` (lead), ink black, paper white; lilac `#D6AACD` and teal `#00C8DC` for decoration only
- Font: Poppins (self-hosted)
- Voice: warm, with a dry edge; first person ("I")

## Blog

Each post is a Markdown file in `src/content/posts/`. The file name is the URL: `src/content/posts/my-post.md` → `/post/my-post`. Cover images go in `public/images/blog/`.

Four July 2025 posts are kept in `src/content/held/` but not published, because they contain client examples that need confirming. Their old URLs redirect to `/blog` (see `public/_redirects`). To restore one, move it to `src/content/posts/`, add a `description`, and delete its line from `_redirects`.

## Redirects

`public/_redirects` sends the old Wix URLs (/start-here, /about-us, /our-services, /our-work, legal pages) to their new pages.

## Rebrand special

The banner sits near the top of `src/pages/index.astro` and the offer box at the top of `src/pages/pricing.astro` (`id="special"`). Remove both when the 5 spots are filled.

## Working on the site

```
npm install
npm run dev      # local preview at http://localhost:4321
npm run build    # production build into dist/
```

Cloudflare Pages settings: build command `npm run build`, output directory `dist`, Node 22. Pushing to `main` publishes the site.
