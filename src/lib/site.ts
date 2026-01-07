import fs from "node:fs";

const X_PLATFORM_HANDLE = "@henryperschk";
const SOCIAL_IMAGE_PATH = "/assets/banner.jpg";
const socialImageVersion = (() => {
  try {
    const fileUrl = new URL(`../../public${SOCIAL_IMAGE_PATH}`, import.meta.url);
    const stat = fs.statSync(fileUrl);
    return String(Math.floor(stat.mtimeMs));
  } catch {
    return undefined;
  }
})();

export const SITE = {
  title: "Thinking Rocks",
  description: "",
  author: "Henry Perschk",
  url: "https://thinking.rocks",
  profileImage: "/assets/profile.jpg",
  socialImage: SOCIAL_IMAGE_PATH,
  socialImageVersion,
  postXPlatformCard: "summary_large_image",
  xPlatformHandle: X_PLATFORM_HANDLE,
  xPlatformUrl: `https://x.com/${X_PLATFORM_HANDLE.replace(/^@/, "")}`,
} as const;

export const PAGE_META = {
  about: {
    title: "Henry Perschk",
    description: "AI, Digital Physics, Artificial Life, Open-Endedness, Evolutionary Algorithms.",
  },
  posts: {
    title: "Posts",
    description: "All posts and notes from Thinking Rocks.",
  },
  privacy: {
    title: "Privacy",
    description:
      "We use OpenPanel for basic page view analytics. It is cookie-free and does not identify users.",
  },
} as const;

export const OPENPANEL = {
  apiUrl: "https://api.openpanel.analytics.vibeps.zereal.ai",
  clientId: "ee88d6ce-bcd9-41a4-8bea-b8521593a356",
  cdnUrl: "https://dashboard.openpanel.analytics.vibeps.zereal.ai/op1.js",
} as const;
