<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useFacultiesStore } from '@/stores/faculties'
import { useSupervisorModelsStore } from '@/stores/supervisor/models'
import { useSupervisorReportsStore } from '@/stores/supervisor/reports'
import TitleH3 from '@/components/common/TitleH3.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import NoResultsFound from '@/components/common/NoResultsFound.vue'
import DistributionChart from './DistributionChart.vue'
import RiskSummary from './RiskSummary.vue'

const loading = ref(true)
const facultiesStore = useFacultiesStore()
const supervisorModelsStore = useSupervisorModelsStore()
const supervisorReportsStore = useSupervisorReportsStore()
const hasData = computed(() => reportData.value.total_students > 0)
const selectedFaculty = computed(() => facultiesStore.getSelectedFaculty)
const selectedModelVersion = computed(() => supervisorModelsStore.getSelectedModel)

// State
const reportData = ref({
  total_students: 0,
  distribution: {},
  distribution_percentages: {},
  risk_summary: {
    high_risk: { count: 0, percentage: 0 },
    medium_risk: { count: 0, percentage: 0 },
    low_risk: { count: 0, percentage: 0 }
  }
})

const loadData = async () => {
  loading.value = true
  try {
    const data = await supervisorReportsStore.fetchDropoutDistribution({
      modelVersionId: selectedModelVersion.value?.id,
      faculty: selectedFaculty.value?.short_name
    })
    reportData.value = data
  } catch (error) {
    console.error('Failed to load dropout distribution data', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => loadData())

watch(
  () => [selectedModelVersion.value, selectedFaculty.value],
  () => loadData()
)
</script>

<template>
  <div>
    <TitleH3 class="mb-2">Distribución de la probabilidad de deserción</TitleH3>
    <LoadingState v-if="loading" />
    <NoResultsFound v-else-if="!hasData" />

    <div v-if="!loading && hasData">
      <!-- Risk Summary Cards -->
      <RiskSummary
        :risk-summary="reportData.risk_summary"
        :total-students="reportData.total_students"
      />

      <!-- Distribution Chart -->
      <div class="card bg-base-100 shadow-md mb-6 border">
        <div class="card-body border">
          <DistributionChart
            :distribution="reportData.distribution"
            :percentages="reportData.distribution_percentages"
          />
        </div>
      </div>
    </div>
  </div>
</template>

