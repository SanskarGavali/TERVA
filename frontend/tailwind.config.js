/** @type {import("tailwindcss").Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        terva: {
          primary: "#7779E8",
          background: "#F5F5FF",
          surface: "#FFFFFF",
          lavender: "#E9E8FF",
          text: "#292A45"
        }
      }
    }
  },
  plugins: []
};
