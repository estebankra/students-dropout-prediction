import './index.css'
import 'vue-toastification/dist/index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import Toast, { useToast } from 'vue-toastification'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toast, {
  transition: 'Vue-Toastification__bounce',
  maxToasts: 2,
  newestOnTop: true
})

app.config.errorHandler = (err, _, info) => {
  if (err.status === 400) return
  const toast = useToast()
  toast.error('Se ha producido un error. Vuelva a intentarlo más tarde')
  console.error(err, info)
}

app.mount('#app')
