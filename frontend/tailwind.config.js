/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          500: "#340CB9",
          650: "#290990",
          800: "#1C0665",
          fg: "#FFFFFF"
        },
        surface: {
          DEFAULT: "#FFFFFF",
          soft: "#F6F7FB",
          ring: "#E5E7EB"
        },
        text: {
          DEFAULT: "#111827",
          muted: "#6B7280"
        }
      },
      borderRadius: {
        pill: "22px",
        xl: "1rem",
        "2xl": "1.25rem"
      },
      boxShadow: {
        card: "0 4px 16px rgba(0,0,0,0.06)",
        soft: "0 2px 8px rgba(0,0,0,0.05)"
      }
    }
  },
  plugins: [require("@tailwindcss/forms")]
};
