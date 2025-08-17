<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import ModelSelector from '@/components/supervisor/models/Selector.vue'

const router = useRouter()
const userStore = useUserStore()

const logout = async () => {
  await userStore.logout()
  router.push('/sign-in')
}
</script>

<template>
  <div class="navbar bg-primary/10">
    <div class="navbar-start">
      <div class="dropdown">
        <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
          <span class="material-symbols-outlined">menu</span>
        </div>
        <ul
          tabindex="0"
          class="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow gap-2"
        >
          <li><RouterLink :to="{ name: 'Home' }">Reportes</RouterLink></li>
          <li><RouterLink :to="{ name: 'SupervisorStudents' }">Estudiantes</RouterLink></li>
        </ul>
      </div>
      <RouterLink :to="{ name: 'Home' }" class="btn btn-ghost text-xl">
        <span class="material-symbols-outlined text-4xl md:text-5xl">school</span>
      </RouterLink>
    </div>
    <div class="navbar-center hidden lg:flex">
      <ul class="menu menu-horizontal px-1">
        <li><RouterLink :to="{ name: 'Home' }">Reportes</RouterLink></li>
        <li><RouterLink :to="{ name: 'SupervisorStudents' }">Estudiantes</RouterLink></li>
      </ul>
    </div>
    <div class="navbar-end">
      <ModelSelector />
      <div class="dropdown dropdown-end">
        <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
          <div class="w-10 rounded-full border-2 border-primary">
            <span class="material-symbols-outlined text-3xl text-primary">person</span>
          </div>
        </div>
        <ul
          tabindex="0"
          class="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
        >
          <li><button @click="logout">Cerrar sesión</button></li>
        </ul>
      </div>
    </div>
  </div>
</template>
