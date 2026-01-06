type MarkdownModule = {
  frontmatter?: Record<string, unknown>;
  Content: unknown;
};

export type BlogPost = {
  slug: string;
  title: string;
  date: Date;
  url: string;
  module: MarkdownModule;
};

const POST_FILENAME =
  /\/_posts\/(?<yyyy>\d{4})-(?<mm>\d{2})-(?<dd>\d{2})-(?<slug>.+)\.md$/;

const postModules = import.meta.glob<MarkdownModule>("../../_posts/*.md", {
  eager: true,
});

function parsePostFilePath(filePath: string) {
  const match = POST_FILENAME.exec(filePath);
  if (!match?.groups) return null;

  const { yyyy, mm, dd, slug } = match.groups;
  const iso = `${yyyy}-${mm}-${dd}T00:00:00.000Z`;

  return {
    slug,
    date: new Date(iso),
  };
}

export function getAllPosts(): BlogPost[] {
  const posts = Object.entries(postModules)
    .map(([filePath, module]) => {
      const parsed = parsePostFilePath(filePath);
      if (!parsed) return null;

      const title =
        typeof module.frontmatter?.title === "string"
          ? module.frontmatter.title
          : parsed.slug.replace(/-/g, " ");

      return {
        slug: parsed.slug,
        date: parsed.date,
        title,
        url: `/b/${parsed.slug}`,
        module,
      } satisfies BlogPost;
    })
    .filter((post): post is BlogPost => post !== null)
    .sort((a, b) => b.date.getTime() - a.date.getTime());

  return posts;
}

export function getPostBySlug(slug: string): BlogPost | undefined {
  return getAllPosts().find((post) => post.slug === slug);
}
