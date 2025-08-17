<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminStatsStore } from '@/stores/admin/dashboard'
import ModelStatus from '@/components/admin/dashboard/ModelStatus.vue'
import LastModels from '@/components/admin/dashboard/LastModels.vue'
import UserStats from '@/components/admin/dashboard/UserStats.vue'
import ModelComparison from '@/components/admin/dashboard/ModelComparison.vue'
import SystemHealth from '@/components/admin/dashboard/SystemHealth.vue'
import TitleH3 from '@/components/common/TitleH3.vue'

const isLoading = ref(false)
const adminStatsStore = useAdminStatsStore()
const stats = computed(() => adminStatsStore.getStats)

const fetchData = async () => {
  isLoading.value = true
  adminStatsStore.fetchStats().finally(() => {
    isLoading.value = false
  })
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <section v-if="!isLoading && stats" class="flex flex-col py-6 gap-8">
    <SystemHealth />
    <UserStats :userStats="stats.user_stats" />
    <ModelStatus :currentModel="stats.active_model" />
    <div>
      <TitleH3 class="card-title mb-2">Comparación del rendimiento de los modelos</TitleH3>
      <ModelComparison :hideTable="true" />
    </div>
    <LastModels />
  </section>
</template>
