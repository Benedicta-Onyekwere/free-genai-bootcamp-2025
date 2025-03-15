/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#3b82f6",
          foreground: "#ffffff"
        },
        card: {
          DEFAULT: "#ffffff",
          foreground: "#000000"
        }
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms')
  ]
} 