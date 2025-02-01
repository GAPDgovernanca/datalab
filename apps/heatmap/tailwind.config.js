/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  safelist: [
    'bg-gray-200',
    'bg-gray-400',
    'bg-red-300',
    'bg-red-500',
    'bg-blue-400',
    'bg-blue-600',
    'border-gray-100',
    'border-gray-200',
    'text-white'
  ]
}