<script setup>
import { computed } from 'vue'
import { getDropoutRiskClass } from '@/helpers/style'
import { useSupervisorModelsStore } from '@/stores/supervisor/models'

const props = defineProps({
  students: { type: Array, required: true, default: new Array() },
  hideActionButtons: { type: Boolean, required: false, default: false }
})

const supervisorModelsStore = useSupervisorModelsStore()
const selectedModelVersion = computed(() => supervisorModelsStore.getSelectedModel)

const emit = defineEmits(['viewStudent'])
const handleViewStudent = (student) => {
  emit('viewStudent', student)
  document.getElementById('supervisor_students_form').showModal()
}

const getPredictionByVersion = (predictions) => {
  return predictions.find(
    (prediction) => prediction.model_version === selectedModelVersion.value.version
  )
}
</script>

<template>
  <div class="overflow-x-auto">
    <table class="table table-xs lg:table-lg md:table-md sm:table-sm">
      <thead>
        <tr>
          <th>#</th>
          <th>Estado</th>
          <th>Facultad</th>
          <th>Nombre</th>
          <th>Apellido</th>
          <th>Riesgo de deserción</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(student, index) in props.students"
          :key="student.id"
          :class="{ 'bg-warning/20': student.archived }"
        >
          <th>{{ index + 1 }}</th>
          <td>
            <span v-if="student.estado === 'E'" class="badge badge-success text-white">
              Egresado
            </span>
            <span v-else-if="student.estado === 'A'" class="badge badge-error text-white">
              Abandono
            </span>
            <span v-else class="badge badge-primary text-white">Vigente</span>
          </td>
          <td>{{ student.faculty.short_name }}</td>
          <td>{{ student.first_name }}</td>
          <td>{{ student.last_name }}</td>
          <td>
            <span
              v-if="student.predictions.length > 0 && getPredictionByVersion(student.predictions)"
              class="badge text-white min-w-16"
              :class="
                getDropoutRiskClass(
                  getPredictionByVersion(student.predictions)['dropout_probability']
                )
              "
            >
              {{
                Math.round(
                  getPredictionByVersion(student.predictions)['dropout_probability'] * 100
                )
              }}%
            </span>
            <span v-else class="badge badge-warning">No hay datos</span>
          </td>
          <td v-if="!props.hideActionButtons">
            <button class="btn btn-sm btn-ghost text-primary" @click="handleViewStudent(student)">
              <span class="material-symbols-outlined">visibility</span>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
