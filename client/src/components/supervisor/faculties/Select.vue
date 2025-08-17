<script setup>
import { ref, onMounted, computed } from 'vue'
import { useFacultiesStore } from '@/stores/faculties'
import { onBeforeRouteLeave } from 'vue-router'

const props = defineProps({
  selectSize: { type: String, default: 'select-sm' },
  buttonSize: { type: String, default: 'max-w-52' }
})

const facultiesStore = useFacultiesStore()
const faculties = computed(() => facultiesStore.getFaculties)
const selectedFaculty = ref(0)

const handleUpdateFacultySelected = () => {
  facultiesStore.setSelectedFaculty(selectedFaculty.value)
}

const loadData = async () => {
  await facultiesStore.fetchFaculties({})
}

onMounted(() => loadData())
onBeforeRouteLeave(() => facultiesStore.setSelectedFaculty(null))
</script>

<template>
  <label
    v-if="faculties && faculties.items.length > 0"
    class="flex flex-col form-control w-full max-w-md"
  >
    <div class="label">
      <span class="label-text">Facultad</span>
    </div>
    <select
      class="select select-bordered w-full"
      :class="`${props.selectSize} ${props.buttonSize}`"
      v-model="selectedFaculty"
      @change="handleUpdateFacultySelected"
    >
      <option :value="0">Todos</option>
      <option v-for="faculty in faculties.items" :key="faculty.id" :value="faculty">
        ({{ faculty.short_name }}) {{ faculty.long_name }}
      </option>
    </select>
  </label>
</template>
