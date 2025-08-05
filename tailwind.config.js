/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      animation: {
        'time-pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'time-spin': 'spin 20s linear infinite',
        'time-glow': 'glow 2s ease-in-out infinite',
        'steam': 'steam 3s ease-in-out infinite',
        'gear': 'gear 10s linear infinite',
      },
      keyframes: {
        glow: {
          '0%, 100%': { opacity: 0.5, filter: 'brightness(1)' },
          '50%': { opacity: 1, filter: 'brightness(1.2)' },
        },
        steam: {
          '0%, 100%': { transform: 'translateY(0) scale(1)', opacity: 0 },
          '50%': { transform: 'translateY(-20px) scale(1.2)', opacity: 0.5 },
        },
        gear: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        }
      },
      backgroundImage: {
        'time-pattern': "url('data:image/svg+xml,%3Csvg width=\"60\" height=\"60\" viewBox=\"0 0 60 60\" xmlns=\"http://www.w3.org/2000/svg\"%3E%3Cg fill=\"none\" fill-rule=\"evenodd\"%3E%3Cg fill=\"%23f59e0b\" fill-opacity=\"0.05\"%3E%3Cpath d=\"M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')",
        'gear-pattern': "url('data:image/svg+xml,%3Csvg width=\"80\" height=\"80\" viewBox=\"0 0 80 80\" xmlns=\"http://www.w3.org/2000/svg\"%3E%3Cpath d=\"M40 0c-2.2 0-4 1.8-4 4v4c-3.4 0.8-6.6 2.2-9.4 4.2l-2.8-2.8c-1.6-1.6-4.2-1.6-5.8 0l-5.6 5.6c-1.6 1.6-1.6 4.2 0 5.8l2.8 2.8c-2 2.8-3.4 6-4.2 9.4h-4c-2.2 0-4 1.8-4 4v8c0 2.2 1.8 4 4 4h4c0.8 3.4 2.2 6.6 4.2 9.4l-2.8 2.8c-1.6 1.6-1.6 4.2 0 5.8l5.6 5.6c1.6 1.6 4.2 1.6 5.8 0l2.8-2.8c2.8 2 6 3.4 9.4 4.2v4c0 2.2 1.8 4 4 4h8c2.2 0 4-1.8 4-4v-4c3.4-0.8 6.6-2.2 9.4-4.2l2.8 2.8c1.6 1.6 4.2 1.6 5.8 0l5.6-5.6c1.6-1.6 1.6-4.2 0-5.8l-2.8-2.8c2-2.8 3.4-6 4.2-9.4h4c2.2 0 4-1.8 4-4v-8c0-2.2-1.8-4-4-4h-4c-0.8-3.4-2.2-6.6-4.2-9.4l2.8-2.8c1.6-1.6 1.6-4.2 0-5.8l-5.6-5.6c-1.6-1.6-4.2-1.6-5.8 0l-2.8 2.8c-2.8-2-6-3.4-9.4-4.2v-4c0-2.2-1.8-4-4-4h-8z\" fill=\"%23f59e0b\" fill-opacity=\"0.05\"/%3E%3C/svg%3E')",
      },
      colors: {
        copper: {
          50: '#fdf4e7',
          100: '#fbe3c3',
          200: '#f8d19f',
          300: '#f5bf7b',
          400: '#f2ad57',
          500: '#ef9b33',
          600: '#d98b2e',
          700: '#c37b29',
          800: '#ad6b24',
          900: '#975b1f',
        },
        brass: {
          50: '#fff8e7',
          100: '#ffefc3',
          200: '#ffe69f',
          300: '#ffdd7b',
          400: '#ffd457',
          500: '#ffcb33',
          600: '#e6b72e',
          700: '#cca329',
          800: '#b38f24',
          900: '#997b1f',
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}