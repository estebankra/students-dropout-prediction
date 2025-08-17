<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminFacultiesStore } from '@/stores/admin/faculties'
import { useHeaderContent } from '@/composables/useHeaderContent'
import AdminFacultiesForm from '@/components/admin/faculties/Form.vue'
import AdminFacultiesFilters from '@/components/admin/faculties/Filters.vue'
import AdminFacultiesList from '@/components/admin/faculties/List.vue'
import LoadMore from '@/components/common/LoadMore.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import NoResultsFound from '@/components/common/NoResultsFound.vue'

const isLoading = ref(false)
const facultyToEdit = ref(null)
const { setHeaderContent } = useHeaderContent()
const adminFacultiesStore = useAdminFacultiesStore()
const faculties = computed(() => adminFacultiesStore.getFaculties)

const cancelEditFaculty = () => {
  facultyToEdit.value = null
}

const handleEditFaculty = (faculty) => {
  facultyToEdit.value = faculty
}

const fetchData = async (facultiesFilters = null) => {
  if (facultiesFilters) adminFacultiesStore.resetFacultiesState()
  const newOffset = faculties.value.offset + faculties.value.limit
  if (newOffset > faculties.value.total) return

  isLoading.value = true
  adminFacultiesStore
    .fetchFaculties({
      filters: facultiesFilters,
      offset: newOffset,
      limit: 25
    })
    .finally(() => {
      isLoading.value = false
    })
}

onMounted(() => {
  setHeaderContent('Facultades')
  adminFacultiesStore.resetFacultiesState()
  fetchData()
})
</script>

<template>
  <section class="flex flex-col">
    <div class="flex justify-end items-center gap-6">
      <AdminFacultiesFilters @filtersUpdated="fetchData" />
      <AdminFacultiesForm :facultyToEdit="facultyToEdit" @cancelEditFaculty="cancelEditFaculty" />
    </div>
    <section v-if="faculties.items.length">
      <AdminFacultiesList :faculties="faculties.items" @editFaculty="handleEditFaculty" />
      <LoadMore v-if="faculties.offset + faculties.limit < faculties.total" @loadMore="fetchData" />
    </section>
    <NoResultsFound v-else-if="!isLoading" />
    <LoadingState v-if="isLoading" />
  </section>
</template>
