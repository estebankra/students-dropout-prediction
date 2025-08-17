<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useFacultiesStore } from '@/stores/faculties'
import LoadingState from '@/components/common/LoadingState.vue'
import { useSupervisorReportsStore } from '@/stores/supervisor/reports'
import { useSupervisorModelsStore } from '@/stores/supervisor/models'

const facultiesStore = useFacultiesStore()
const supervisorReportsStore = useSupervisorReportsStore()
const supervisorModelsStore = useSupervisorModelsStore()

const loading = ref(true)
const reportData = ref({ faculty_distributions: {} })
const faculties = computed(() => facultiesStore.getFaculties)
const selectedFaculty = computed(() => facultiesStore.getSelectedFaculty)
const selectedModelVersion = computed(() => supervisorModelsStore.getSelectedModel)

// Methods
const loadData = async () => {
  loading.value = true
  try {
    const data = await supervisorReportsStore.fetchFacultyDropoutDistribution({
      modelVersionId: selectedModelVersion.value?.id
    })
    reportData.value = data
  } catch (error) {
    console.error('Failed to load faculty dropout distribution data', error)
  } finally {
    loading.value = false
  }
}

const selectedDistribution = computed(() => {
  if (!selectedFaculty.value) return null
  return reportData.value.faculty_distributions[selectedFaculty.value.short_name]
})

// Calculate total students for a faculty
const getFacultyTotal = (faculty) => {
  const distribution = reportData.value.faculty_distributions[faculty.short_name]
  if (!distribution) return
  return Object.values(distribution).reduce((sum, count) => sum + count, 0)
}

// Calculate percentage for a specific bucket in a faculty
const getPercentage = (faculty, bucket) => {
  const distribution = reportData.value.faculty_distributions[faculty.short_name]
  const total = getFacultyTotal(faculty)
  return total > 0 ? (distribution[bucket] / total) * 100 : 0
}

// Get color based on risk level
const getBucketColor = (bucket) => {
  const percentage = parseInt(bucket.split('-')[0])
  if (percentage < 40) return 'bg-success/60'
  if (percentage < 70) return 'bg-warning/60'
  return 'bg-error/60'
}

onMounted(() => {
  loadData()
})

watch(
  () => selectedModelVersion.value,
  () => loadData()
)
</script>

<template>
  <div
    v-if="selectedFaculty"
    class="tooltip"
    data-tip="Ver distribución de probabilidad de deserción"
  >
    <button
      class="btn btn-secondary btn-square btn-sm"
      onclick="faculty_dropout_distribution.showModal()"
    >
      <span class="material-symbols-outlined text-xl text-white">query_stats</span>
    </button>
  </div>

  <dialog v-if="selectedFaculty" id="faculty_dropout_distribution" class="modal">
    <div class="modal-box w-11/12 max-w-6xl">
      <form method="dialog">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
      </form>
      <div class="flex flex-col">
        <div v-if="!loading && faculties && faculties.items.length > 0">
          <div class="mt-4">
            <h4 class="text-lg font-semibold mb-2">
              ({{ selectedFaculty.short_name }}) {{ selectedFaculty.long_name }} -
              {{ getFacultyTotal(selectedFaculty) }} estudiantes
            </h4>

            <div class="overflow-x-auto">
              <table class="table table-zebra w-full">
                <thead>
                  <tr>
                    <th>Rango</th>
                    <th># Estudiantes</th>
                    <th>Porcentaje</th>
                    <th>Distribución</th>
                  </tr>
                </thead>
                <tbody v-if="selectedDistribution">
                  <tr v-for="bucket in Object.keys(selectedDistribution)" :key="bucket">
                    <td>{{ bucket }}</td>
                    <td>{{ selectedDistribution[bucket] }}</td>
                    <td>{{ getPercentage(selectedFaculty, bucket).toFixed(1) }}%</td>
                    <td class="w-1/3">
                      <div class="w-full bg-base-300 rounded-full h-2.5">
                        <div
                          class="h-2.5 rounded-full"
                          :class="getBucketColor(bucket)"
                          :style="{ width: `${getPercentage(selectedFaculty, bucket)}%` }"
                        ></div>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <LoadingState v-else />
      </div>
    </div>
  </dialog>
</template>
