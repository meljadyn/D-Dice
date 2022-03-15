module.exports = {
  content: ["../templates/*.html", "../index.html"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["garden", "dracula"],
    styled: true,
    darkTheme: "dracula",
  }
}
