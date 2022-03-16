module.exports = {
  content: ["../templates/*.html", "../index.html"],
  theme: {
    extend: {},
  },
  
  plugins: [
    require('@tailwindcss/typography'),
    require("daisyui")
  ],

  daisyui: {
    themes: ["cupcake", "dracula"],
    styled: true,
    darkTheme: "dracula",
  }
}
