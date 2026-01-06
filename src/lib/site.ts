const X_PLATFORM_HANDLE = "@henryperschk";

export const SITE = {
  title: "Thinking Rocks",
  description: "",
  author: "Henry Perschk",
  url: "https://thinking.rocks",
  profileImage: "/assets/profile.jpeg",
  socialImage: "/assets/thinking_rocks_banner.jpeg",
  socialImageVersion: "20260106",
  postXPlatformCard: "summary_large_image",
  xPlatformHandle: X_PLATFORM_HANDLE,
  xPlatformUrl: `https://x.com/${X_PLATFORM_HANDLE.replace(/^@/, "")}`,
} as const;

export const OPENPANEL = {
  apiUrl: "https://api.openpanel.analytics.vibeps.zereal.ai",
  clientId: "ee88d6ce-bcd9-41a4-8bea-b8521593a356",
  cdnUrl: "https://dashboard.openpanel.analytics.vibeps.zereal.ai/op1.js",
} as const;
