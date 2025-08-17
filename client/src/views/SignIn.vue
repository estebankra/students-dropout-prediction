<script setup>
import axios from '@/lib/axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useHeaderContent } from '@/composables/useHeaderContent'

const router = useRouter()
const { setHeaderContent } = useHeaderContent()

const email = ref('')
const password = ref('')

const login = async () => {
  try {
    const formData = new FormData()
    formData.append('username', email.value)
    formData.append('password', password.value)

    const response = await axios.post('/auth/login', formData)
    if (!response.statusText === 'OK') {
      throw new Error('Login failed')
    }
    router.push('/')
  } catch (error) {
    console.error('Login failed:', error)
    throw error
  }
}

onMounted(() => setHeaderContent(''))
</script>

<template>
  <div class="flex justify-center py-12 sm:px-6 lg:px-8">
    <form @submit.prevent="login" class="card bg-base-100 w-96 h-min shadow border">
      <div class="card-body">
        <h1 class="card-title justify-center">Iniciar sesión</h1>

        <label class="input input-bordered flex items-center gap-2">
          <span class="material-symbols-outlined leading-none">mail</span>
          <input v-model="email" type="email" class="grow" placeholder="Email" />
        </label>

        <label class="input input-bordered flex items-center gap-2">
          <span class="material-symbols-outlined leading-none">key</span>
          <input
            v-model="password"
            type="password"
            class="grow"
            value=""
            placeholder="Contraseña"
          />
        </label>

        <div class="card-actions">
          <button type="submit" class="btn btn-primary w-full text-white">Iniciar sesión</button>
        </div>
      </div>
    </form>
  </div>
</template>
