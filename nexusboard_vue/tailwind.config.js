module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Dark grey base palette
        'mb-bg': '#0b0b0d',
        'mb-surface': '#17181a',
        'mb-muted': '#b3bac3',
        // Accents
        'mb-primary': '#60a5fa',
        'mb-secondary': '#34d399',
        'mb-highlight': '#a78bfa'
      },
      fontFamily: {
        sans: ['Atkinson Hyperlegible', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial'],
        heading: ['Space Grotesk', 'sans-serif']
      }
    }
  },
  plugins: []
}
