import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";

export default defineConfig({
  site: process.env.SITE ?? "https://thinking.rocks",
  base: process.env.BASE_PATH ?? "/",
  redirects: {
    "/": "/posts",
  },
  vite: {
    server: {
      allowedHosts: [".ngrok-free.app"],
    },
  },
  build: {
    // Keep the current output style (e.g. /about.html, /b/post.html)
    format: "file",
  },
  integrations: [tailwind()],
});
