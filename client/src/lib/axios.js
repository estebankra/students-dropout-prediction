import axios from 'axios'
import { useToast } from 'vue-toastification'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
  timeout: 60000
})

const toast = useToast()
const router = useRouter()

instance.interceptors.response.use(
  (response) => {
    if (response?.data?.message) toast.success(response.data.message)
    return response
  },
  (error) => {
    const originalRequest = error.config
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      if (error.response?.data?.detail) {
        toast.warning(error.response.data.detail)
      }
      useUserStore().logout()
      router.push('/sign-in')
    } else if (error.response.status === 404 || error.response.status === 403) {
      return
    } else if (error.response?.data?.detail) {
      const errorDetail = error.response.data.detail
      if (Array.isArray(errorDetail)) {
        const errorDetails = errorDetail
        for (const error of errorDetails) {
          toast.warning(error['msg'])
        }
      } else if (error.response.status === 400) {
        toast.warning(errorDetail)
      } else {
        toast.error(errorDetail)
      }
    } else {
      toast.error('Se ha producido un error. Vuelva a intentarlo más tarde')
    }
    return Promise.reject(error)
  }
)

export default instance
