<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useFacultiesStore } from '@/stores/faculties'
import { useSupervisorStudentsStore } from '@/stores/supervisor/students'
import { useSupervisorModelsStore } from '@/stores/supervisor/models'
import { useHeaderContent } from '@/composables/useHeaderContent'
import LoadMore from '@/components/common/LoadMore.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import NoResultsFound from '@/components/common/NoResultsFound.vue'
import SupervisorStudentsForm from '@/components/supervisor/students/Form.vue'
import SupervisorStudentsFilters from '@/components/supervisor/students/Filters.vue'
import SupervisorStudentsList from '@/components/supervisor/students/List.vue'
import SupervisorPredictDropout from '@/components/supervisor/models/PredictDropout.vue'
import FacultyDistribution from '@/components/supervisor/reports/DropoutDistribution/FacultyDistribution.vue'
import SupervisorFacultySelect from '@/components/supervisor/faculties/Select.vue'

const isLoading = ref(false)
const studentToView = ref(null)
const studentFilters = ref({
  dropoutProbability: {
    min: 0,
    max: 100
  }
})
const { setHeaderContent } = useHeaderContent()
const facultiesStore = useFacultiesStore()
const supervisorStudentsStore = useSupervisorStudentsStore()
const supervisorModelsStore = useSupervisorModelsStore()
const students = computed(() => supervisorStudentsStore.getStudents)
const selectedFaculty = computed(() => facultiesStore.getSelectedFaculty)
const selectedModelVersion = computed(() => supervisorModelsStore.getSelectedModel)

const cancelViewStudent = () => {
  studentToView.value = null
}

const handleViewStudent = (student) => {
  studentToView.value = student
}

const fetchData = async () => {
  const newOffset = students.value.offset + students.value.limit
  if (newOffset > students.value.total) return

  isLoading.value = true
  supervisorStudentsStore
    .fetchStudents({
      filters: studentFilters.value,
      offset: newOffset,
      limit: 25,
      modelVersionId: selectedModelVersion.value?.id,
      faculty: selectedFaculty.value?.short_name
    })
    .then(() => {
      isLoading.value = false
    })
}

const updateFilters = (updatedFilters) => {
  supervisorStudentsStore.resetStudentsState()
  studentFilters.value = updatedFilters
  fetchData()
}

onMounted(() => {
  setHeaderContent('Estudiantes')
  supervisorStudentsStore.resetStudentsState()
  fetchData()
})

watch(
  () => [selectedModelVersion.value, selectedFaculty.value],
  () => updateFilters(studentFilters.value)
)
</script>

<template>
  <section class="flex flex-col">
    <div class="flex gap-2 items-end mb-2 justify-between">
      <div class="flex flex-row items-end gap-1">
        <FacultyDistribution />
        <SupervisorFacultySelect />
      </div>
      <div class="flex items-end gap-1">
        <SupervisorStudentsFilters @filtersUpdated="updateFilters" />
        <SupervisorPredictDropout />
        <SupervisorStudentsForm
          :studentToView="studentToView"
          @cancelViewStudent="cancelViewStudent"
          @studentUpdated="() => updateFilters(studentFilters)"
        />
      </div>
    </div>

    <section v-if="students.items.length">
      <SupervisorStudentsList :students="students.items" @viewStudent="handleViewStudent" />
      <LoadMore v-if="students.offset + students.limit < students.total" @loadMore="fetchData" />
    </section>
    <NoResultsFound v-else-if="!isLoading" />
    <LoadingState v-if="isLoading" />
  </section>
</template>

