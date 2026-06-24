module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: 0, transform: 'translateY(14px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.6s ease-out both',
        'fade-in': 'fadeIn 0.8s ease-out both',
      },
    },
  },
  plugins: [],
}