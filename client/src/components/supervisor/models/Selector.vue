<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useSupervisorModelsStore } from '@/stores/supervisor/models'
import { formatDate } from '@/helpers/style'

const props = defineProps({
  selectedModelId: { type: Number, default: null }
})

const modelsStore = useSupervisorModelsStore()
const isLoading = ref(false)
const models = computed(() => modelsStore.getModels)
const selectedModel = ref(props.selectedModelId)

const handleModelChange = () => {
  const selectedModelVersion = models.value.items.find((model) => model.id === selectedModel.value)
  modelsStore.setSelectedModel(selectedModelVersion)
}

// Watch for external changes to selectedModelId
watch(
  () => props.selectedModelId,
  (newValue) => {
    if (newValue !== selectedModel.value) {
      selectedModel.value = newValue
    }
  }
)

onMounted(async () => {
  isLoading.value = true
  await modelsStore.fetchModels()

  // If no model is selected yet, select the first one
  if (!selectedModel.value && models.value.total > 0) {
    selectedModel.value = models.value.items[0].id
    handleModelChange()
  }

  isLoading.value = false
})
</script>

<template>
  <div class="form-control flex flex-row items-center mx-2">
    <label class="label w-full justify-end gap-1">
      <span class="label-text">Versión del modelo</span>
      <span class="label-text">
        <div
          class="tooltip tooltip-left"
          data-tip="Selecciona la versión del modelo de la que se obtendrán los datos y/o se calculará el riesgo de deserción"
        >
          <span class="material-symbols-outlined text-sm">help</span>
        </div>
      </span>
    </label>
    <select
      v-model="selectedModel"
      class="select select-sm select-bordered w-80"
      @change="handleModelChange"
      :disabled="isLoading"
    >
      <option disabled value="null">Selecciona una versión</option>
      <option
        v-for="model in models.items"
        :key="model.id"
        :value="model.id"
        :class="{ 'font-bold': model.is_active }"
      >
        {{ model.version }} {{ model.is_active ? '(Activo)' : '' }}
        {{ formatDate(model.created_at) }}
      </option>
    </select>
  </div>
</template>

