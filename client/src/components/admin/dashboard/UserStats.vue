<script setup>
import { useRouter } from 'vue-router'
import TitleH2 from '@/components/common/TitleH2.vue'

const router = useRouter()

const props = defineProps({
  userStats: { type: Object, required: true }
})

const navigateToUsers = () => {
  router.push('/admin/users')
}
</script>

<template>
  <section class="flex flex-col gap-4">
    <div class="flex justify-between">
      <TitleH2>Usuarios</TitleH2>
      <button class="btn btn-primary btn-sm text-white" @click="navigateToUsers">
        Administrar usuarios<span class="material-symbols-outlined text-xl">chevron_right</span>
      </button>
    </div>

    <div class="w-full stats shadow border">
      <div class="stat place-items-center">
        <div class="stat-title">Total</div>
        <div class="stat-value">{{ props.userStats.total_users }}</div>
        <div class="stat-desc">
          <span class="text-success">+{{ props.userStats.new_users_last_30_days }} </span> en los
          últimos 30 días
        </div>
      </div>
      <div class="stat place-items-center">
        <div class="stat-title">Administradores</div>
        <div class="stat-value">{{ props.userStats.total_admins }}</div>
        <div class="stat-desc text-base">
          <span class="text-success">{{ props.userStats.total_active_admins }} activo</span>
        </div>
      </div>
      <div class="stat place-items-center">
        <div class="stat-title">Supervisores</div>
        <div class="stat-value">{{ props.userStats.total_supervisors }}</div>
        <div class="stat-desc text-base">
          <span class="text-success">{{ props.userStats.total_active_supervisors }} activo</span>
        </div>
      </div>
    </div>
  </section>
</template>

