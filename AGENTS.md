# AGENTS

## Obsidian post import helper

When asked to import or sync an Obsidian post into this blog, use the repo-local
`obsidian-blog-import` skill at:

```text
.codex/skills/obsidian-blog-import/SKILL.md
```

Prefer its converter script over manual copying. For existing posts, pass the
destination `_posts/YYYY-MM-DD-slug.md` so existing frontmatter and asset paths
are preserved.

## PDF embed helper

To fit a PDF's first page without internal scrollbars, compute the page aspect
ratio and embed the PDF in a wrapper with that ratio.

```bash
scripts/pdf-aspect.sh path/to/file.pdf
```

Paste the generated `<div>/<object>` snippet into the post Markdown.
