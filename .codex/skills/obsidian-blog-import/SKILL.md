---
name: obsidian-blog-import
description: Convert Obsidian published Markdown posts into Thinking Rocks blog posts. Use when a user gives a path to an Obsidian note and wants it imported, copied, synced, or transformed into this Astro blog's `_posts/YYYY-MM-DD-slug.md` format with blog frontmatter, cleaned publishable body content, and copied Obsidian attachments.
---

# Obsidian Blog Import

Use this skill to import a published Obsidian note into the Thinking Rocks Astro blog without changing the site's layout or runtime behavior.

## Blog Contract

- Destination posts live in `_posts/YYYY-MM-DD-slug.md`.
- The date and slug come from the destination filename.
- Expected frontmatter keys are `title`, optional `subtitle`, optional `image`, and optional `imageAlt`.
- Post assets live in `public/assets/posts/<date-slug>/`, matching the destination Markdown filename without `.md`, and are referenced as `/assets/posts/<date-slug>/<file>`.
- PDF embeds should use a fixed aspect-ratio wrapper so they do not show internal scrollbars.

## Workflow

1. Read the Obsidian source note path from the user.
2. If updating an existing blog post, pass `--dest _posts/YYYY-MM-DD-slug.md` to preserve the existing filename and frontmatter by default.
3. If creating a new blog post, pass `--date YYYY-MM-DD`; pass `--slug`, `--title`, and `--subtitle` when the source note does not make them unambiguous.
4. Run the converter from the blog repo root:

```bash
python3 .codex/skills/obsidian-blog-import/scripts/import_obsidian_post.py \
  "/path/to/Obsidian Published/Post.md" \
  --dest _posts/YYYY-MM-DD-slug.md
```

5. Inspect the generated Markdown before finalizing:

```bash
git diff -- _posts public/assets/posts
npm run build
```

## Conversion Rules

- Preserve existing destination frontmatter unless the user passes explicit overrides.
- Extract the publishable essay from Obsidian notes that contain a `ChatGPT:` section by using the content between the first two Markdown horizontal rules after `ChatGPT:`.
- Drop generated title lines such as `**Title: ...**` from the Markdown body; use them as title candidates only when no stronger title is available.
- Normalize smart quotes to straight quotes in the generated blog Markdown.
- Convert Obsidian wiki links like `[[Note|label]]` to `label` and `[[Note]]` to `Note`.
- Resolve Obsidian embeds like `![[file.pdf]]` from the source folder, `attachments/`, or parent `attachments/` folders.
- Copy PDF and image attachments into `public/assets/posts/<date-slug>/`.
- Convert PDF embeds into the blog's `<div>/<object>` wrapper with the copied asset path.
- Convert image embeds into ordinary Markdown images.

## Script Notes

The bundled script is deterministic and should be preferred over hand-editing for imports. If `pdfinfo` is available, it computes the first page size for the PDF wrapper. If it is missing, install Poppler or run the repo's `scripts/pdf-aspect.sh` manually before accepting the output.
