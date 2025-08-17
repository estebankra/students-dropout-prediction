<script setup>
import { useRouter } from 'vue-router'
import TitleH1 from '@/components/common/TitleH1.vue'

const router = useRouter()

const newRegistration = () => {
  router.push('/students/new')
}
</script>
<template>
  <div class="flex flex-col items-center gap-8 py-24 sm:px-6 lg:px-8">
    <div class="flex flex-col items-center">
      <span class="material-symbols-outlined text-7xl md:text-8xl">school</span>
      <TitleH1>Registro de Estudiantes</TitleH1>
    </div>
    <button @click="newRegistration" class="btn btn-primary text-white btn-lg">
      Nuevo registro
    </button>
  </div>
</template>
