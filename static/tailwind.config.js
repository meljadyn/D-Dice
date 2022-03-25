module.exports = {
  content: ["../templates/*.html", "../index.html"],
  theme: {
    darkMode: 'class',
    extend: {},
  },
  
  plugins: [
    require('@tailwindcss/typography'),
    require("daisyui")
  ],

  daisyui: {
    themes: ["cupcake", "night"],
    styled: true,
    darkTheme: "night",
  }
}
