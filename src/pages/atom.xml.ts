import type { APIRoute } from "astro";
import { getAllPosts } from "../lib/posts";
import { SITE } from "../lib/site";

function escapeXml(value: string) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

export const GET: APIRoute = ({ site }) => {
  const base = site?.href?.replace(/\/$/, "") ?? "https://thinking.rocks";
  const posts = getAllPosts();
  const updated = new Date().toISOString();

  const entries = posts
    .map((post) => {
      const link = `${base}${post.url}`;
      const id = `${base}${post.url}`;
      const postUpdated = post.date.toISOString();
      const summary = escapeXml(post.title);

      return [
        "<entry>",
        `<title>${escapeXml(post.title)}</title>`,
        `<link href="${escapeXml(link)}"/>`,
        `<updated>${escapeXml(postUpdated)}</updated>`,
        `<id>${escapeXml(id)}</id>`,
        `<summary type="html">${summary}</summary>`,
        "</entry>",
      ].join("");
    })
    .join("");

  const xml = [
    '<?xml version="1.0" encoding="utf-8"?>',
    '<feed xmlns="http://www.w3.org/2005/Atom">',
    `<title>${escapeXml(SITE.title)}</title>`,
    `<link href="${escapeXml(`${base}/atom.xml`)}" rel="self"/>`,
    `<link href="${escapeXml(`${base}/`)}"/>`,
    `<updated>${escapeXml(updated)}</updated>`,
    `<id>${escapeXml(base)}</id>`,
    "<author>",
    `<name>${escapeXml(SITE.author)}</name>`,
    "</author>",
    entries,
    "</feed>",
  ].join("");

  return new Response(xml, {
    headers: {
      "Content-Type": "application/atom+xml; charset=utf-8",
    },
  });
};

