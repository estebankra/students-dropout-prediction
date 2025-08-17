<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import GuestNavbar from '@/components/guest/Navbar.vue'
import AdminNavbar from '@/components/admin/Navbar.vue'
import SupervisorNavbar from '@/components/supervisor/Navbar.vue'

const userStore = useUserStore()
const userIsAuthenticated = computed(() => userStore.isAuthenticated)
</script>

<template>
  <GuestNavbar v-if="!userIsAuthenticated" />
  <AdminNavbar v-else-if="userStore.isUserAnAdmin()" />
  <SupervisorNavbar v-else-if="userStore.isUserASupervisor()" />
</template>
