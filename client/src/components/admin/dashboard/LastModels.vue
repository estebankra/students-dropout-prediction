<script setup>
import { useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import { useAdminModelsStore } from '@/stores/admin/models'
import AdminModelsList from '@/components/admin/models/List.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import TitleH3 from '@/components/common/TitleH3.vue'

const router = useRouter()
const adminModelsStore = useAdminModelsStore()

const isLoading = ref(false)
const models = computed(() => adminModelsStore.getModels)

const fetchData = async () => {
  isLoading.value = true
  adminModelsStore.fetchModels({ offset: 0, limit: 3 }).finally(() => {
    isLoading.value = false
  })
}

const navigateToModels = () => {
  router.push('/admin/models')
}

onMounted(() => {
  adminModelsStore.resetModelsState()
  fetchData()
})
</script>

<template>
  <section class="flex flex-col">
    <div class="flex justify-between">
      <TitleH3>Entrenamientos pasados</TitleH3>
      <button @click="navigateToModels" class="flex items-center link-secondary">
        <span class="hover:underline">Ver todos</span>
        <span class="material-symbols-outlined text-secondary text-2xl no-underline">
          chevron_right
        </span>
      </button>
    </div>
    <AdminModelsList :models="models.items" />
    <LoadingState v-if="isLoading" />
  </section>
</template>

