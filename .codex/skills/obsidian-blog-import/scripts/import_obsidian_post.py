#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
EMBED_RE = re.compile(r"!\[\[([^\]]+)\]\]")
WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
POST_NAME_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.+)\.md$")


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "post"


def normalize_text(value: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201a": "'",
        "\u201b": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u201e": '"',
        "\u201f": '"',
        "\u00a0": " ",
    }
    for source, target in replacements.items():
        value = value.replace(source, target)
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text

    raw = text[4:end].strip("\n")
    body = text[end + len("\n---") :].lstrip("\n")
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        data[key.strip()] = value
    return data, body


def yaml_value(value: str) -> str:
    if value == "":
        return '""'
    if re.search(r"[:#{}\[\],&*?|\-<>=!%@`]", value) and not re.match(r"^[A-Za-z0-9/][A-Za-z0-9 '/()._-]*$", value):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def format_frontmatter(data: dict[str, str]) -> str:
    preferred = ["title", "subtitle", "image", "imageAlt"]
    keys = [key for key in preferred if key in data]
    keys.extend(key for key in data if key not in keys)
    lines = ["---"]
    for key in keys:
        lines.append(f"{key}: {yaml_value(data[key])}")
    lines.append("---")
    return "\n".join(lines)


def extract_title_line(body: str) -> tuple[str | None, str]:
    lines = body.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return None, ""

    first = lines[0].strip()
    match = re.match(r"\*\*Title:\s*(.+?)\*\*$", first, re.IGNORECASE)
    if match:
        return match.group(1).strip(), "\n".join(lines[1:]).lstrip("\n")

    match = re.match(r"#\s+(.+)$", first)
    if match:
        return match.group(1).strip(), "\n".join(lines[1:]).lstrip("\n")

    return None, body


def extract_publishable_body(source_body: str) -> tuple[str | None, str]:
    text = source_body
    if "ChatGPT:" in text:
        text = text.split("ChatGPT:", 1)[1]

    text = text.strip()
    parts = re.split(r"(?m)^---\s*$", text)
    if len(parts) >= 3:
        text = parts[1].strip()

    title, text = extract_title_line(text)
    text = WIKILINK_RE.sub(lambda m: m.group(2) or m.group(1), text)
    text = normalize_text(text.strip())
    return title, text


def post_info_from_dest(dest: Path) -> tuple[str, str] | None:
    match = POST_NAME_RE.match(dest.name)
    if not match:
        return None
    return match.group("date"), match.group("slug")


def find_existing_dest(posts_dir: Path, slug: str) -> Path | None:
    matches = sorted(posts_dir.glob(f"????-??-??-{slug}.md"))
    return matches[0] if matches else None


def resolve_embed(source: Path, target: str) -> Path | None:
    name = target.split("|", 1)[0].strip()
    if "#" in name:
        name = name.split("#", 1)[0]
    candidates = [
        source.parent / name,
        source.parent / "attachments" / name,
        source.parent.parent / "attachments" / name,
    ]
    for parent in source.parents:
        candidates.append(parent / "attachments" / name)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def pdf_page_size(pdf: Path) -> tuple[str, str] | None:
    try:
        result = subprocess.run(
            ["pdfinfo", str(pdf)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    for line in result.stdout.splitlines():
        if line.startswith("Page size:"):
            match = re.search(r"([0-9.]+)\s+x\s+([0-9.]+)", line)
            if match:
                return match.group(1), match.group(2)
    return None


def copy_embed_and_render(source_md: Path, embed_target: str, repo: Path, asset_dir_name: str, dry_run: bool) -> str:
    source_asset = resolve_embed(source_md, embed_target)
    if source_asset is None:
        return f"<!-- Unresolved Obsidian embed: ![[{embed_target}]] -->"

    asset_dir = repo / "public" / "assets" / "posts" / asset_dir_name
    safe_name = f"{slugify(source_asset.stem)}{source_asset.suffix.lower()}"
    dest_asset = asset_dir / safe_name
    public_path = f"/assets/posts/{asset_dir_name}/{safe_name}"

    if not dry_run:
        asset_dir.mkdir(parents=True, exist_ok=True)
        if source_asset.resolve() != dest_asset.resolve():
            shutil.copy2(source_asset, dest_asset)

    suffix = source_asset.suffix.lower()
    if suffix == ".pdf":
        size = pdf_page_size(source_asset)
        if size is None:
            aspect = "1 / 1.414"
        else:
            aspect = f"{size[0]} / {size[1]}"
        return (
            f'<div style="width: 100%; aspect-ratio: {aspect}; margin-bottom: 1rem;">\n'
            f'  <object data="{public_path}#toolbar=0&view=Fit"\n'
            f'          type="application/pdf"\n'
            f'          style="width: 100%; height: 100%; display: block;">\n'
            f"  </object>\n"
            f"</div>"
        )

    if suffix in IMAGE_EXTS:
        alt = source_asset.stem.replace("-", " ").replace("_", " ")
        return f"![{alt}]({public_path})"

    return f"[{source_asset.name}]({public_path})"


def render_embed_block(source_md: Path, source_text: str, repo: Path, asset_dir_name: str, dry_run: bool) -> str:
    rendered: list[str] = []
    seen: set[str] = set()
    for match in EMBED_RE.finditer(source_text):
        target = match.group(1).strip()
        if target in seen:
            continue
        seen.add(target)
        rendered.append(copy_embed_and_render(source_md, target, repo, asset_dir_name, dry_run))
    return "\n\n".join(rendered)


def build_output(args: argparse.Namespace) -> tuple[Path, str]:
    repo = Path(args.repo).expanduser().resolve()
    source_md = Path(args.source).expanduser().resolve()
    posts_dir = repo / "_posts"

    source_text = source_md.read_text(encoding="utf-8")
    source_fm, source_body = parse_frontmatter(source_text)
    source_title, body = extract_publishable_body(source_body)

    title_candidate = args.title or source_fm.get("title") or source_title or source_md.stem
    slug = args.slug or slugify(title_candidate)

    if args.dest:
        dest = (repo / args.dest).resolve() if not Path(args.dest).is_absolute() else Path(args.dest).resolve()
    else:
        existing = find_existing_dest(posts_dir, slug)
        if existing:
            dest = existing.resolve()
        else:
            if not args.date:
                raise SystemExit("New posts require --date YYYY-MM-DD or an existing --dest.")
            dest = (posts_dir / f"{args.date}-{slug}.md").resolve()

    info = post_info_from_dest(dest)
    if info:
        date_from_dest, slug_from_dest = info
        slug = args.slug or slug_from_dest
        if args.date and args.date != date_from_dest:
            raise SystemExit(f"--date {args.date} does not match destination filename date {date_from_dest}.")

    existing_fm: dict[str, str] = {}
    if dest.exists():
        existing_fm, _ = parse_frontmatter(dest.read_text(encoding="utf-8"))

    frontmatter = {**source_fm, **existing_fm}
    frontmatter["title"] = args.title or frontmatter.get("title") or title_candidate
    if args.subtitle is not None:
        frontmatter["subtitle"] = args.subtitle
    elif "subtitle" not in frontmatter and source_fm.get("subtitle"):
        frontmatter["subtitle"] = source_fm["subtitle"]
    if args.image is not None:
        frontmatter["image"] = args.image
    if args.image_alt is not None:
        frontmatter["imageAlt"] = args.image_alt

    asset_dir_name = dest.stem
    embed_block = render_embed_block(source_md, source_text, repo, asset_dir_name, args.dry_run)
    chunks = [format_frontmatter(frontmatter)]
    if embed_block:
        chunks.append(embed_block)
    chunks.append(body)
    return dest, "\n\n".join(chunk.rstrip() for chunk in chunks if chunk.strip()) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Import an Obsidian published note into Thinking Rocks blog format.")
    parser.add_argument("source", help="Path to the Obsidian Markdown note")
    parser.add_argument("--repo", default=os.getcwd(), help="Path to the Thinking Rocks repo")
    parser.add_argument("--dest", help="Destination post path, relative to repo or absolute")
    parser.add_argument("--date", help="Publish date for new posts, YYYY-MM-DD")
    parser.add_argument("--slug", help="Destination slug")
    parser.add_argument("--title", help="Frontmatter title override")
    parser.add_argument("--subtitle", help="Frontmatter subtitle override")
    parser.add_argument("--image", help="Frontmatter image override")
    parser.add_argument("--image-alt", dest="image_alt", help="Frontmatter imageAlt override")
    parser.add_argument("--dry-run", action="store_true", help="Print the destination and converted Markdown without writing")
    args = parser.parse_args()

    if args.date:
        try:
            dt.date.fromisoformat(args.date)
        except ValueError as exc:
            raise SystemExit("--date must be YYYY-MM-DD") from exc

    dest, output = build_output(args)
    if args.dry_run:
        print(f"Destination: {dest}")
        print()
        print(output, end="")
        return 0

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(output, encoding="utf-8")
    print(f"Wrote {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
