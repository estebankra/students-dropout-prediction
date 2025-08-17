<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useFacultiesStore } from '@/stores/faculties'
import { useSupervisorStudentsStore } from '@/stores/supervisor/students'
import { useSupervisorModelsStore } from '@/stores/supervisor/models'

const emit = defineEmits(['filtersUpdated'])
const supervisorStudentsStore = useSupervisorStudentsStore()
const facultiesStore = useFacultiesStore()
const supervisorModelsStore = useSupervisorModelsStore()

const toast = useToast()
const route = useRoute()
const selectedFaculty = computed(() => facultiesStore.getSelectedFaculty)
const selectedModelVersion = computed(() => supervisorModelsStore.getSelectedModel)

const debounceTimeout = ref(null)
const isExporting = ref(false)

const filters = ref({
  dropoutProbability: {
    min: 0,
    max: 100
  },
  search: '',
  estado: 'V',
  archived: false
})

// Check for query parameters on component mount
onMounted(() => {
  if (route.query['min-risk'] !== undefined && route.query['max-risk'] !== undefined) {
    filters.value.dropoutProbability.min = parseInt(route.query['min-risk'])
    filters.value.dropoutProbability.max = parseInt(route.query['max-risk'])
    emit('filtersUpdated', filters.value)
  }
})

const debouncedEmitFilters = () => {
  if (debounceTimeout.value) clearTimeout(debounceTimeout.value)

  debounceTimeout.value = setTimeout(() => {
    emit('filtersUpdated', filters.value)
  }, 1000)
}

const exportData = async (format) => {
  try {
    isExporting.value = true

    const response = await supervisorStudentsStore.exportStudents({
      format: format,
      filters: filters.value,
      modelVersionId: selectedModelVersion.value?.id,
      faculty: selectedFaculty.value?.short_name
    })

    // Create a blob URL and trigger download
    const blob = new Blob([response.data], {
      type: {
        csv: 'text/csv',
        excel: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        pdf: 'application/pdf'
      }[format]
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url

    // Extract filename from Content-Disposition header
    const contentDisposition = response.headers['content-disposition']
    const filenameMatch = contentDisposition.match(/filename="(.+)"/)
    const filename = filenameMatch[1]

    // Download
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    toast.success('Reporte generado correctamente')

    // Clean up
    window.URL.revokeObjectURL(url)
    document.body.removeChild(link)
  } catch (error) {
    console.error(`Error exporting to ${format}:`, error)
    toast.error(`Error al exportar a ${format.toUpperCase()}. Por favor, inténtelo de nuevo.`)
  } finally {
    isExporting.value = false
  }
}

const exportToCsv = () => exportData('csv')
const exportToExcel = () => exportData('excel')
const exportToPdf = () => exportData('pdf')

watch(
  () => [
    filters.value.dropoutProbability.min,
    filters.value.dropoutProbability.max,
    filters.value.search,
    filters.value.estado,
    filters.value.archived
  ],
  () => {
    debouncedEmitFilters()
  },
  { deep: true }
)
</script>

<template>
  <div class="flex flex-col form-control">
    <label class="label cursor-pointer gap-2">
      <input type="checkbox" v-model="filters.archived" :value="true" class="checkbox" />
      <span class="label-text">Archivados</span>
    </label>
  </div>

  <label class="flex flex-col form-control w-full lg:max-w-48">
    <div class="label">
      <span class="label-text">Nombres</span>
    </div>
    <div class="input input-sm input-bordered flex items-center gap-2">
      <span class="material-symbols-outlined text-gray-400">search</span>
      <input type="text" class="w-full" v-model="filters.search" />
    </div>
  </label>

  <label class="flex flex-col form-control w-full max-w-40">
    <div class="label">
      <span class="label-text">Estado</span>
    </div>
    <select class="select select-bordered select-sm" v-model="filters.estado">
      <option selected value="V">Vigente</option>
      <option value="E">Egresado</option>
      <option value="A">Abandono</option>
    </select>
  </label>

  <div class="flex flex-col form-control">
    <div class="label">
      <span class="label-text">Probabilidad de deserción (%)</span>
    </div>

    <div class="flex gap-2 items-center">
      <label class="input input-sm input-bordered flex items-center gap-2 p-0 pl-2">
        <span class="w-max text-gray-400">Desde (%)</span>
        <input
          type="number"
          min="0"
          max="100"
          class="w-10 text-right"
          v-model.number="filters.dropoutProbability.min"
        />
      </label>

      <label class="input input-sm input-bordered flex items-center gap-2 p-0 pl-2">
        <span class="w-max text-gray-400">Hasta (%)</span>
        <input
          type="number"
          min="0"
          max="100"
          class="w-10 text-right"
          v-model.number="filters.dropoutProbability.max"
        />
      </label>
    </div>
  </div>

  <div class="dropdown dropdown-bottom">
    <button tabindex="0" class="btn btn-sm btn-secondary text-white w-max" :disabled="isExporting">
      <span v-if="isExporting" class="loading loading-spinner loading-sm"></span>
      <span v-else class="material-symbols-outlined text-xl">file_export</span>
      Exportar
    </button>
    <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
      <li>
        <button @click="exportToCsv" :disabled="isExporting" class="flex items-center gap-2">
          <span class="material-symbols-outlined">description</span>
          CSV
        </button>
      </li>
      <li>
        <button @click="exportToExcel" :disabled="isExporting" class="flex items-center gap-2">
          <span class="material-symbols-outlined">table_view</span>
          Excel
        </button>
      </li>
      <li>
        <button @click="exportToPdf" :disabled="isExporting" class="flex items-center gap-2">
          <span class="material-symbols-outlined">picture_as_pdf</span>
          PDF
        </button>
      </li>
    </ul>
  </div>
</template>

