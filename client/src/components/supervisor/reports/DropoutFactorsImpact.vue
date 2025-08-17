<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useFacultiesStore } from '@/stores/faculties'
import { useSupervisorModelsStore } from '@/stores/supervisor/models'
import { useSupervisorReportsStore } from '@/stores/supervisor/reports'
import TitleH3 from '@/components/common/TitleH3.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import NoResultsFound from '@/components/common/NoResultsFound.vue'

const facultiesStore = useFacultiesStore()
const supervisorModelsStore = useSupervisorModelsStore()
const selectedFaculty = computed(() => facultiesStore.getSelectedFaculty)
const selectedModelVersion = computed(() => supervisorModelsStore.getSelectedModel)

const supervisorReportsStore = useSupervisorReportsStore()

const isLoading = ref(false)
const error = ref(null)
const factorsData = ref(null)

const fetchFactorsData = async () => {
  isLoading.value = true
  error.value = null

  try {
    const response = await supervisorReportsStore.fetchDropoutFactorsImpact({
      modelVersionId: selectedModelVersion.value?.id,
      faculty: selectedFaculty.value?.short_name
    })
    factorsData.value = response
  } catch (err) {
    console.error('Error fetching dropout factors impact data:', err)
    error.value = 'Error al cargar los datos de factores de deserción'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchFactorsData()
})

watch(
  () => [selectedModelVersion.value, selectedFaculty.value],
  () => {
    fetchFactorsData()
  }
)

// Format the impact score for display
const formatImpactScore = (score) => {
  return score.toFixed(1)
}

// Get color based on impact score
const getImpactColor = (score) => {
  if (score >= 80) return 'bg-error'
  if (score >= 60) return 'bg-warning'
  if (score >= 40) return 'bg-accent'
  if (score >= 20) return 'bg-info'
  return 'bg-success'
}
</script>

<template>
  <div>
    <TitleH3 class="mb-2">Factores de mayor impacto en la deserción</TitleH3>
    <LoadingState v-if="isLoading" />
    <NoResultsFound v-else-if="!factorsData || factorsData.factors.length === 0" />
    <div v-else-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div v-else class="grid grid-cols-1 gap-6">
      <div class="card border shadow">
        <div class="card-body">
          <p class="mb-4 text-sm">
            Basado en el análisis de {{ factorsData.total_students_analyzed }} estudiantes, estos
            son los factores que más influyen en la probabilidad de deserción.
          </p>

          <div class="overflow-x-auto">
            <table class="table table-zebra w-full">
              <thead>
                <tr>
                  <th>Factor</th>
                  <th>Impacto</th>
                  <th>Descripción</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(factor, index) in factorsData.factors" :key="index">
                  <td class="font-medium">{{ factor.factor }}</td>
                  <td>
                    <div class="flex items-center gap-2">
                      <div class="w-12 bg-base-300 rounded-full h-2.5">
                        <div
                          class="h-2.5 rounded-full"
                          :class="getImpactColor(factor.impact_score)"
                          :style="{ width: `${factor.impact_score}%` }"
                        ></div>
                      </div>
                      <span class="text-sm">{{ formatImpactScore(factor.impact_score) }}%</span>
                    </div>
                  </td>
                  <td class="text-sm">{{ factor.description }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="mt-4 text-sm text-base-content/70">
            <p>
              <strong>Nota:</strong> El impacto se calcula analizando cómo varía la probabilidad de
              deserción entre diferentes valores de cada factor.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
