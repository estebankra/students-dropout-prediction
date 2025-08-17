<script setup>
import { ref, computed, onMounted } from 'vue'
import { useHeaderContent } from '@/composables/useHeaderContent'
import { useAdminModelsStore } from '@/stores/admin/models'
import ModelComparison from '@/components/admin/dashboard/ModelComparison.vue'
import AdminModelsCreate from '@/components/admin/models/Create.vue'
import AdminModelsList from '@/components/admin/models/List.vue'
import LoadMore from '@/components/common/LoadMore.vue'
import LoadingState from '@/components/common/LoadingState.vue'

const isLoading = ref(false)
const { setHeaderContent } = useHeaderContent()
const adminModelsStore = useAdminModelsStore()
const models = computed(() => adminModelsStore.getModels)
const sortBy = ref('version')
const sortOrder = ref('desc')

const sortOptions = [
  { value: 'version', label: 'Versión' },
  { value: 'num_samples', label: 'Cantidad de datos' },
  { value: 'num_features', label: 'Cantidad de características' },
  { value: 'accuracy', label: 'Accuracy' },
  { value: 'precision', label: 'Precision' },
  { value: 'recall', label: 'Recall' },
  { value: 'f1_score', label: 'F1 Score' },
  { value: 'created_at', label: 'Fecha de entrenamiento' }
]

const fetchData = async (resetOffset = false) => {
  const offset = resetOffset ? 0 : models.value.offset + models.value.limit
  if (!resetOffset && offset > models.value.total) return

  isLoading.value = true
  adminModelsStore
    .fetchModels({
      offset: offset,
      limit: 15,
      sortBy: sortBy.value,
      sortOrder: sortOrder.value
    })
    .then(() => {
      isLoading.value = false
    })
}

const handleSortChange = () => {
  fetchData(true)
}

onMounted(() => {
  setHeaderContent('Modelos')
  adminModelsStore.resetModelsState()
  fetchData()
})
</script>

<template>
  <section class="flex flex-col gap-4">
    <div class="flex gap-2 justify-end">
      <div class="flex flex-wrap gap-2 items-center">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Ordenar por</span>
          </label>
          <select
            v-model="sortBy"
            class="select select-sm select-bordered w-full max-w-xs"
            @change="handleSortChange"
          >
            <option v-for="option in sortOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
        </div>

        <div class="form-control">
          <label class="label">
            <span class="label-text">Orden</span>
          </label>
          <select
            v-model="sortOrder"
            class="select select-sm select-bordered w-full max-w-xs"
            @change="handleSortChange"
          >
            <option value="desc">Descendente</option>
            <option value="asc">Ascendente</option>
          </select>
        </div>
      </div>
      <AdminModelsCreate />
    </div>
    <AdminModelsList :models="models.items" />
    <LoadingState v-if="isLoading" />
    <LoadMore v-if="models.offset + models.limit < models.total" @loadMore="fetchData" />
    <div class="collapse collapse-arrow bg-primary/10 mb-4">
      <input type="checkbox" />
      <div class="collapse-title flex gap-2 items-center text-xl font-medium">
        <span class="material-symbols-outlined">compare_arrows</span>
        <span>Comparar el rendimiento de los modelos</span>
      </div>
      <div class="collapse-content">
        <ModelComparison />
      </div>
    </div>
  </section>
</template>
