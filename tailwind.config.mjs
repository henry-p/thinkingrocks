import typography from "@tailwindcss/typography";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        cream: "#FFF1E5",
      },
      fontFamily: {
        serif: ["Merriweather", "ui-serif", "Georgia", "Cambria", "Times New Roman", "Times", "serif"],
      },
    },
  },
  plugins: [typography],
};
