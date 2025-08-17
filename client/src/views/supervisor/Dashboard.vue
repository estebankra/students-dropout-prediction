<script setup>
import TitleH3 from '@/components/common/TitleH3.vue'
import { useRouter } from 'vue-router'
import { ref, onMounted, computed, watch } from 'vue'
import { useFacultiesStore } from '@/stores/faculties'
import { useHeaderContent } from '@/composables/useHeaderContent'
import { useSupervisorModelsStore } from '@/stores/supervisor/models'
import { useSupervisorStudentsStore } from '@/stores/supervisor/students'
import DropoutDistribution from '@/components/supervisor/reports/DropoutDistribution/DropoutDistribution.vue'
import DropoutFactorsImpact from '@/components/supervisor/reports/DropoutFactorsImpact.vue'
import SupervisorPredictDropout from '@/components/supervisor/models/PredictDropout.vue'
import SupervisorFacultySelect from '@/components/supervisor/faculties/Select.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import NoResultsFound from '@/components/common/NoResultsFound.vue'
import SupervisorStudentsList from '@/components/supervisor/students/List.vue'

const activeTab = ref('dropout-distribution')
const router = useRouter()
const { setHeaderContent } = useHeaderContent()
const facultiesStore = useFacultiesStore()
const supervisorStudentsStore = useSupervisorStudentsStore()
const supervisorModelsStore = useSupervisorModelsStore()
const selectedFaculty = computed(() => facultiesStore.getSelectedFaculty)
const selectedModelVersion = computed(() => supervisorModelsStore.getSelectedModel)

const highRiskStudents = ref(null)
const studentsWithoutPrediction = ref(null)

const isLoadingHighRiskStudents = ref(false)
const isLoadingStudentsWithoutPrediction = ref(false)

const highRiskstudentFilters = ref({
  dropoutProbability: {
    min: 80,
    max: 100
  }
})

const fetchHighRiskStudents = async () => {
  isLoadingHighRiskStudents.value = true
  supervisorStudentsStore
    .fetchStudents({
      filters: highRiskstudentFilters.value,
      offset: 0,
      limit: 10,
      faculty: selectedFaculty.value?.short_name,
      modelVersionId: selectedModelVersion.value?.id
    })
    .then((data) => {
      highRiskStudents.value = data.items
      isLoadingHighRiskStudents.value = false
    })
}

const fetchStudentsWithoutPrediction = async () => {
  isLoadingStudentsWithoutPrediction.value = true
  supervisorStudentsStore
    .fetchStudents({
      filters: null,
      offset: 0,
      limit: 10,
      faculty: selectedFaculty.value?.short_name,
      modelVersionId: selectedModelVersion.value?.id
    })
    .then((data) => {
      studentsWithoutPrediction.value = data.items
      isLoadingStudentsWithoutPrediction.value = false
    })
}

const navigateToStudentsList = (minRisk, maxRisk) => {
  router.push({
    name: 'SupervisorStudents',
    query: { 'min-risk': minRisk, 'max-risk': maxRisk }
  })
}

onMounted(() => {
  setHeaderContent('Reportes')
  fetchHighRiskStudents()
  fetchStudentsWithoutPrediction()
})

watch(
  () => [selectedModelVersion.value, selectedFaculty.value],
  () => {
    fetchHighRiskStudents()
    fetchStudentsWithoutPrediction()
  }
)
</script>

<template>
  <div class="p-4 container mx-auto">
    <div class="flex flex-wrap gap-2 items-end mb-2 justify-end">
      <SupervisorFacultySelect select-size="select-md" button-size="max-w-lg" />
      <SupervisorPredictDropout button-size="btn-md" />
    </div>

    <!-- <div role="tablist" class="tabs tabs-boxed mb-0 mt-6">
      <a
        class="tab"
        :class="{ 'tab-active ': activeTab === 'dropout-distribution' }"
        @click="activeTab = 'dropout-distribution'"
      >
        <span class="text-white">Dropout Distribution</span>
      </a>
      <a class="tab" @click="activeTab = 'dropout-distribution'">
        <span>Estudiantes en riesgo</span>
      </a>
    </div> -->

    <section class="card bg-base-100">
      <div class="card-body p-0 mt-2">
        <DropoutDistribution v-if="activeTab === 'dropout-distribution'" />
      </div>
    </section>

    <DropoutFactorsImpact />

    <div class="flex justify-between">
      <TitleH3 class="card-title mt-8">Estudiantes con alto riesgo de deserción</TitleH3>
      <button class="flex items-center link-secondary" @click="navigateToStudentsList(70, 100)">
        <span class="hover:underline">Ver todos</span>
        <span class="material-symbols-outlined text-secondary text-2xl no-underline">
          chevron_right
        </span>
      </button>
    </div>
    <section class="flex flex-col">
      <div v-if="highRiskStudents && highRiskStudents.length > 0">
        <SupervisorStudentsList :students="highRiskStudents" :hide-action-buttons="true" />
      </div>
      <NoResultsFound v-else-if="!isLoadingHighRiskStudents" />
      <LoadingState v-if="isLoadingHighRiskStudents" />
    </section>

    <div class="flex justify-between mt-8">
      <TitleH3 class="card-title">Estudiantes sin predicciones ejecutadas</TitleH3>
      <button class="flex items-center link-secondary" @click="navigateToStudentsList(null, null)">
        <span class="hover:underline">Ver todos</span>
        <span class="material-symbols-outlined text-secondary text-2xl no-underline">
          chevron_right
        </span>
      </button>
    </div>
    <section class="flex flex-col">
      <div v-if="studentsWithoutPrediction && studentsWithoutPrediction.length > 0">
        <SupervisorStudentsList :students="studentsWithoutPrediction" :hide-action-buttons="true" />
      </div>
      <NoResultsFound v-else-if="!isLoadingStudentsWithoutPrediction" />
      <LoadingState v-if="isLoadingStudentsWithoutPrediction" />
    </section>
  </div>
</template>

