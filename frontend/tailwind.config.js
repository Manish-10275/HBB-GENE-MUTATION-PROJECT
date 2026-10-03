/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ["Georgia", "Cambria", "\"Times New Roman\"", "Times", "serif"],
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "\"Liberation Mono\"", "\"Courier New\"", "monospace"],
        sans: ["-apple-system", "BlinkMacSystemFont", "\"Segoe UI\"", "Roboto", "Helvetica", "Arial", "sans-serif"],
      },
      colors: {
        scientific: {
          50: "#f8fafc",
          100: "#f1f5f9",
          200: "#e2e8f0",
          300: "#cbd5e1",
          400: "#94a3b8",
          500: "#64748b",
          600: "#475569",
          700: "#334155",
          800: "#1e293b",
          900: "#0f172a",
          950: "#020617",
        },
        clinical: {
          teal: "#0f766e",
          amber: "#b45309",
          crimson: "#b91c1c",
          emerald: "#047857",
          cobalt: "#1d4ed8",
        }
      }
    },
  },
  plugins: [],
};
