import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      animation: {
        moveSearch: "moveSearch 1s ease-in-out forwards",
        fadeIn: "fadeIn 0.5s ease-in-out forwards",
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      fontFamily: {
        quicksand: ["var(--font-quicksand)"],
      },
      keyframes: {
        moveSearch: {
          "0%": { bottom: "50%", translateY: "50%" },
          "50%": { bottom: "70%", translateY: "25%" },
          "100%": { top: "96px", translateY: "0%" },
        },
        fadeIn: {
          "0%": { opacity: "0" },
          "50%": { opacity: "0.5" },
          "100%": { opacity: "1" },
        },
      },
    },
  },
  plugins: [],
};
export default config;
