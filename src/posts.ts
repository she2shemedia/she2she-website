// Blog posts live as Markdown in src/content/posts/. Each file name is its URL: /post/<file name>.
// Posts in src/content/held/ are kept for reference but not published.
export interface PostMeta { title: string; date: string; author: string; description: string; image: string }
export interface Post { slug: string; frontmatter: PostMeta; Content: any }

const files = import.meta.glob<{ frontmatter: PostMeta; Content: any }>('./content/posts/*.md', { eager: true });

export const posts: Post[] = Object.entries(files)
  .map(([path, mod]) => ({ slug: path.split('/').pop()!.replace(/\.md$/, ''), frontmatter: mod.frontmatter, Content: mod.Content }))
  .sort((a, b) => +new Date(b.frontmatter.date) - +new Date(a.frontmatter.date));

export const formatDate = (d: string | Date) =>
  new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });
