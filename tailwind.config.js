/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.html", "./**/static/**/*.js"],
  theme: {
    extend: {
      colors: {
        'custom-color': '#F0EAEA',
      },
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

