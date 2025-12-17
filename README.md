# Thinking Rocks

This blog is built with [Astro](https://astro.build), styled with [Tailwind CSS](https://tailwindcss.com), and keeps content in Markdown files.

## Content

- Posts: `_posts/*.md`
- Pages: `about.md`, `404.md`
- Static assets: `public/` (e.g. `public/assets`, `public/favicon.png`)

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
