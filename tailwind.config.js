/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.html", "./**/static/**/*.js"],
  theme: {
    extend: {
      spacing: {
        '0-15em': '0.15em',
      },
      fontFamily: {
        abril: ["abril", "serif"],
      },
    },
  },
  plugins: [],
}

