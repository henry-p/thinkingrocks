# Thinking Rocks

This blog is built with [Astro](https://astro.build), styled with [Tailwind CSS](https://tailwindcss.com), and keeps content in Markdown files.

## Content

- Posts: `_posts/*.md`
- Pages: `src/pages/about.astro`, `src/pages/404.astro`
- The root path (`/`) redirects to the posts index at `/posts`
- Static assets: `public/` (e.g. `public/assets`, `public/favicon.png`)

## PDF embeds

For native PDF embeds that fit the first page, compute the PDF's page aspect ratio
and wrap the `<object>` in a container using that ratio.

```bash
scripts/pdf-aspect.sh path/to/file.pdf
```

Paste the generated `<div>/<object>` snippet into the post Markdown.

## Local development

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
npm run preview
```

## Deployment

GitHub Actions deploys the `dist/` output to GitHub Pages on pushes to `master`.
