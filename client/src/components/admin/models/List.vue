<script setup>
import { ref } from 'vue'
import { useAdminModelsStore } from '@/stores/admin/models'
import {
  formatDate,
  getModelPerformanceColorClass,
  getModelPerformanceLabel,
  getModelPerformancePercentage
} from '@/helpers/style'

const props = defineProps({
  models: { type: Array, required: true, default: new Array() }
})

const modelsStore = useAdminModelsStore()
const isLoading = ref(false)
const activeModelId = ref(null)

const setActiveModel = async (modelId) => {
  isLoading.value = true
  activeModelId.value = modelId
  try {
    await modelsStore.setActiveModel(modelId)
    await modelsStore.fetchModels({ offset: 0 })
  } catch (error) {
    console.error('Error setting active model:', error)
  } finally {
    isLoading.value = false
    activeModelId.value = null
  }
}
</script>

<template>
  <div class="overflow-x-auto">
    <table class="table table-xs lg:table-lg md:table-md sm:table-sm">
      <thead>
        <tr>
          <th>#</th>
          <th>Versión</th>
          <th># Datos</th>
          <th># Features</th>
          <th>Accuracy</th>
          <th>Precision</th>
          <th>Recall</th>
          <th>F1</th>
          <th>Fecha de entrenamiento</th>
          <th>Rendimiento</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(model, index) in props.models"
          :key="model.id"
          :class="{ 'bg-success/10': model.is_active }"
        >
          <th>{{ index + 1 }}</th>
          <td>{{ model.version }}</td>
          <td>{{ model.num_samples }}</td>
          <td>{{ model.num_features }}</td>
          <td>{{ model.accuracy }}</td>
          <td>{{ model.precision }}</td>
          <td>{{ model.recall }}</td>
          <td>{{ model.f1_score }}</td>
          <td>{{ formatDate(model.created_at) }}</td>
          <td>
            <div class="flex items-center gap-2">
              <div
                class="radial-progress text-base"
                :class="getModelPerformanceColorClass(getModelPerformancePercentage(model))"
                :style="{
                  '--value': getModelPerformancePercentage(model),
                  '--size': '2.5rem',
                  '--thickness': '0px'
                }"
              >
                {{ getModelPerformancePercentage(model) }}%
              </div>
              <span class="text-xs">{{
                getModelPerformanceLabel(getModelPerformancePercentage(model))
              }}</span>
            </div>
          </td>
          <td>
            <div class="badge badge-success text-white float" v-if="model.is_active">Activo</div>
            <button
              class="btn btn-xs btn-primary text-white"
              @click="setActiveModel(model.id)"
              :disabled="
                model.is_active ||
                isLoading ||
                (activeModelId !== null && activeModelId !== model.id)
              "
              v-if="!model.is_active"
            >
              <span
                v-if="isLoading && activeModelId === model.id"
                class="loading loading-spinner loading-xs"
              ></span>
              Activar
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

