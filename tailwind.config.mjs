/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      fontFamily: {
        heading: ['Cinzel Decorative', 'serif'],
        body: ['EB Garamond', 'serif'],
        'cormorant': ['Cormorant Garamond', 'serif'],
        'spectral': ['Spectral', 'serif'],
      },
      colors: {
        parchment: {
          50: '#fffbf0',
          100: '#fff8e5',
          200: '#fff2d6',
          300: '#ffe8c1',
          400: '#ffd89b',
          500: '#d4af37',
        },
      },
    },
  },
  plugins: [],
}
