import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        custom: ["PressStart2P-Regular", "sans-serif"],
      },
      dropShadow: {
        'glow': '0 0 5px rgba(255, 255, 255, 0.8)',
        'dark': '0 0 5px rgba(0, 0, 0, 0.2)',
      },
      colors: {
        customBlue1: "#40618C",
        customBlue2: "#235596",
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
    },
  },
  plugins: [],
} satisfies Config;
