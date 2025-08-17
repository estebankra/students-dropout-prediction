<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useAdminModelsStore } from '@/stores/admin/models'
import { Chart, registerables } from 'chart.js'
import LoadingState from '@/components/common/LoadingState.vue'

const props = defineProps({
  hideTable: { type: Boolean, default: false }
})

const adminModelsStore = useAdminModelsStore()

// Register Chart.js components
Chart.register(...registerables)

const chartCanvas = ref(null)
const isLoading = ref(false)
const selectedModel1 = ref('')
const selectedModel2 = ref('')
const availableModels = ref([])
const modelData = ref({})
let chart = null

const metrics = [
  { name: 'f1_score', label: 'F1 Score' },
  { name: 'recall', label: 'Recall' },
  { name: 'precision', label: 'Precision' },
  { name: 'accuracy', label: 'Accuracy' }
]

const fetchAvailableModels = async () => {
  try {
    const models = await adminModelsStore.fetchModels({ offset: 0, limit: 100 }).finally(() => {
      isLoading.value = false
    })
    availableModels.value = models.items

    // Set default selections if models are available
    if (availableModels.value.length >= 2) {
      selectedModel1.value = availableModels.value[0].id
      selectedModel2.value = availableModels.value[1].id
      fetchModelData()
    }
  } catch (error) {
    console.error('Error fetching available models:', error)
  }
}

const fetchModelData = async () => {
  if (!selectedModel1.value || !selectedModel2.value) return

  isLoading.value = true
  try {
    modelData.value = await adminModelsStore.compareModels(
      selectedModel1.value,
      selectedModel2.value
    )
    // Use nextTick to ensure the DOM is updated before rendering the chart
    await nextTick()
    renderChart()
  } catch (error) {
    console.error('Error fetching model comparison data:', error)
  } finally {
    isLoading.value = false
  }
}

const updateComparison = () => {
  // Reset chart when selection changes
  if (chart) {
    chart.destroy()
    chart = null
  }
  fetchModelData()
}

const renderChart = async () => {
  if (!chartCanvas.value || !modelData.value.model1 || !modelData.value.model2) {
    console.error('Chart canvas or data not available')
    return
  }

  // Wait for the DOM to update
  await nextTick()

  // Destroy previous chart if exists
  if (chart) {
    chart.destroy()
  }

  try {
    // Prepare data for chart
    const labels = metrics.map((m) => m.label)

    const model1Data = metrics.map((m) => {
      const value = modelData.value.model1.metrics[m.name]
      return value !== undefined ? value : 0
    })

    const model2Data = metrics.map((m) => {
      const value = modelData.value.model2.metrics[m.name]
      return value !== undefined ? value : 0
    })

    // Create new chart
    chart = new Chart(chartCanvas.value, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: `Modelo v${modelData.value.model1.version}.0`,
            data: model1Data,
            backgroundColor: '#36D399',
            borderColor: '#36D399',
            borderWidth: 1
          },
          {
            label: `Modelo v${modelData.value.model2.version}.0`,
            data: model2Data,
            backgroundColor: '#3ABFF8',
            borderColor: '#3ABFF8',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 1,
            ticks: {
              callback: function (value) {
                return value.toFixed(2)
              }
            }
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                return `${context.dataset.label}: ${context.raw.toFixed(3)}`
              }
            }
          }
        }
      }
    })
  } catch (error) {
    console.error('Error rendering chart:', error)
  }
}

const formatValue = (value) => {
  return value !== undefined ? value.toFixed(3) : 'N/A'
}

const formatImprovement = (value) => {
  if (value === undefined) return 'N/A'
  return value > 0 ? `+${value.toFixed(2)}%` : `${value.toFixed(2)}%`
}

const getImprovementClass = (value) => {
  if (value === undefined) return ''
  return value > 0 ? 'text-success font-bold' : value < 0 ? 'text-error font-bold' : ''
}

onMounted(async () => {
  await fetchAvailableModels()
})

// Clean up chart when component is unmounted
onUnmounted(() => {
  if (chart) {
    chart.destroy()
    chart = null
  }
})
</script>

<template>
  <div class="card bg-base-100 shadow border">
    <div class="card-body">
      <div class="flex flex-col md:flex-row gap-4 mb-2 items-center">
        <div class="form-control w-full">
          <select
            class="select select-bordered w-full"
            v-model="selectedModel1"
            @change="updateComparison"
          >
            <option value="" disabled>Selecciona un modelo</option>
            <option v-for="model in availableModels" :key="model.id" :value="model.id">
              {{ model.name }} ({{ model.version }})
            </option>
          </select>
        </div>

        <span>vs</span>

        <div class="form-control w-full">
          <select
            class="select select-bordered w-full"
            v-model="selectedModel2"
            @change="updateComparison"
          >
            <option value="" disabled>Selecciona un modelo</option>
            <option v-for="model in availableModels" :key="model.id" :value="model.id">
              {{ model.name }} ({{ model.version }})
            </option>
          </select>
        </div>
      </div>

      <div v-if="modelData.model1 && modelData.model2" class="w-full" style="height: 300px">
        <canvas ref="chartCanvas"></canvas>
      </div>

      <LoadingState v-if="isLoading" />

      <template v-else-if="!props.hideTable && modelData.model1 && modelData.model2">
        <div class="overflow-x-auto">
          <table class="table table-zebra w-full">
            <thead>
              <tr>
                <th>Métrica</th>
                <th>Modelo v{{ modelData.model1.version }}.0</th>
                <th>Modelo v{{ modelData.model2.version }}.0</th>
                <th>Diferencias</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="metric in metrics" :key="metric.name">
                <td class="font-medium">{{ metric.label }}</td>
                <td>{{ formatValue(modelData.model1.metrics[metric.name]) }}</td>
                <td>{{ formatValue(modelData.model2.metrics[metric.name]) }}</td>
                <td :class="getImprovementClass(modelData.improvement.differences[metric.name])">
                  {{ formatImprovement(modelData.improvement.percentage[metric.name]) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>
  </div>
</template>

