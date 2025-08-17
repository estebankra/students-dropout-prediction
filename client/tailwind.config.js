import daisyui from 'daisyui'
import { corporate } from 'daisyui/src/theming/themes'

/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: [],
  theme: {
    extend: {}
  },
  plugins: [daisyui],
  daisyui: {
    themes: [
      {
        corporate: {
          ...corporate,
          secondary: '#E0B52B'
        }
      }
    ]
  }
}
