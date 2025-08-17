<script setup>
import { computed, onMounted } from 'vue'
import { useHeaderContent } from '@/composables/useHeaderContent'
import { useUserStore } from '@/stores/user'
import AdminDashboard from '@/views/admin/Dashboard.vue'
import SupervisorDashboard from '@/views/supervisor/Dashboard.vue'

const { setHeaderContent } = useHeaderContent()
const userStore = useUserStore()

const currentUser = computed(() => userStore.getCurrentUser)

onMounted(() => {
  setHeaderContent(`Bienvenido, ${currentUser.value.first_name}`)
})
</script>

<template>
  <div v-if="userStore.isUserAnAdmin()">
    <AdminDashboard />
  </div>
  <div v-else-if="userStore.isUserASupervisor()">
    <SupervisorDashboard />
  </div>
</template>
