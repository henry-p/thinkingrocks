import typography from "@tailwindcss/typography";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}"],
  darkMode: "media",
  theme: {
    extend: {
      colors: {
        cream: "#FFF1E5",
        "cream-strong": "#F3E3D3",
        "cream-deep": "#E8D3C1",
        "cream-pill": "#D7B89D",
      },
      fontFamily: {
        serif: ["Spectral", "Merriweather", "ui-serif", "Georgia", "Cambria", "Times New Roman", "Times", "serif"],
        spectral: ["Spectral", "ui-serif", "Georgia", "Cambria", "Times New Roman", "Times", "serif"],
        merriweather: ["Merriweather", "ui-serif", "Georgia", "Cambria", "Times New Roman", "Times", "serif"],
      },
    },
  },
  plugins: [typography],
};
