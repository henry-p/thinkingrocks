# AGENTS

## PDF embed helper

To fit a PDF's first page without internal scrollbars, compute the page aspect
ratio and embed the PDF in a wrapper with that ratio.

```bash
scripts/pdf-aspect.sh path/to/file.pdf
```

Paste the generated `<div>/<object>` snippet into the post Markdown.
