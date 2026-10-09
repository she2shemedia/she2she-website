import { posts } from '../posts';

const pages = ['/', '/services', '/pricing', '/work', '/about', '/book-online', '/blog', '/privacy', '/terms', '/disclaimer', '/accessibility'];

export function GET() {
  const site = 'https://www.she2shemedia.com';
  const urls = [...pages, ...posts.map((p) => `/post/${p.slug}`)];
  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((u) => `  <url><loc>${site}${u}</loc></url>`).join('\n')}
</urlset>`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml' } });
}
