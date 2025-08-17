<script setup>
import { ref, watch, computed } from 'vue'
import { useForm } from 'vee-validate'
import { useToast } from 'vue-toastification'
import { studentSchema } from '@/schemas/students'
import { useSupervisorModelsStore } from '@/stores/supervisor/models'
import { useSupervisorStudentsStore } from '@/stores/supervisor/students'
import StudentFormEditMode from '@/components/students/FormCreateEditMode.vue'
import StudentFormViewMode from '@/components/students/FormViewMode.vue'
import FormSelect from '@/components/common/FormSelect.vue'

const emit = defineEmits(['cancelViewStudent', 'studentUpdated'])

const props = defineProps({
  studentToView: { type: Object, default: null }
})

const supervisorStudentsStore = useSupervisorStudentsStore()
const supervisorModelsStore = useSupervisorModelsStore()
const selectedModelVersion = computed(() => supervisorModelsStore.getSelectedModel)
const studentDropoutProbability = ref(null)
const isEditing = ref(false)
const isViewMode = ref(true)
const archiveStudent = ref(false)
const toast = useToast()

const { handleSubmit, resetForm, setValues } = useForm({
  validationSchema: studentSchema,
  validateOnMount: false
})

const getPredictionByVersion = (predictions) => {
  return predictions.find(
    (prediction) => prediction.model_version === selectedModelVersion.value.version
  )
}

watch(
  () => props.studentToView,
  (newStudent) => {
    if (newStudent) {
      isViewMode.value = true
      isEditing.value = false
      studentDropoutProbability.value = getPredictionByVersion(newStudent.predictions)
      const { faculty, ...studentData } = newStudent
      setValues({ ...studentData, faculty_short_name: faculty.short_name })
      archiveStudent.value = newStudent.archived || false
    } else {
      resetForm()
      archiveStudent.value = false
    }
  },
  { immediate: true }
)

const resetStudentForm = () => {
  isEditing.value = false
  isViewMode.value = true
  archiveStudent.value = false
  emit('cancelViewStudent')
  resetForm()
}

const closeSupervisorStudentFormModal = () => {
  resetStudentForm()
  document.getElementById('supervisor_students_form')?.close()
}

const enableEditMode = () => {
  isViewMode.value = false
  isEditing.value = true
}

const onSubmit = handleSubmit(async (values) => {
  const updatedValues = {
    ...values,
    archived: archiveStudent.value
  }
  await supervisorStudentsStore
    .updateStudent(props.studentToView.id, updatedValues)
    .then(() => {
      isViewMode.value = true
      isEditing.value = false
      toast.success('Estudiante actualizado correctamente')
      closeSupervisorStudentFormModal()
      emit('studentUpdated')
    })
    .catch(() => {
      toast.error('Error al actualizar la información del estudiante')
    })
})
</script>

<template>
  <dialog id="supervisor_students_form" class="modal">
    <div class="modal-box max-w-5xl">
      <button
        @click="closeSupervisorStudentFormModal"
        class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
      >
        ✕
      </button>
      <h3 class="text-lg font-bold">Información del Estudiante</h3>
      <div v-if="props.studentToView">
        <div v-if="isViewMode" class="mt-4">
          <div v-if="props.studentToView.archived" role="alert" class="alert alert-warning mb-4">
            <span class="material-symbols-outlined text-2xl">archive</span>
            <span>
              Este estudiante está archivado y no se usará para entrenar modelos futuros.
            </span>
          </div>
          <StudentFormViewMode
            :studentToView="studentToView"
            :studentDropoutProbability="studentDropoutProbability"
          />
          <div class="flex justify-end mt-4">
            <button @click="enableEditMode" class="btn btn-primary text-white">
              <span class="material-symbols-outlined text-xl">edit</span>
              Editar
            </button>
          </div>
        </div>
        <form v-else @submit.prevent="onSubmit" class="flex flex-col mt-4">
          <div>
            <FormSelect
              labelTop="Estado"
              name="estado"
              :options="[
                { value: 'V', label: 'Vigente' },
                { value: 'E', label: 'Egresado' },
                { value: 'A', label: 'Abandono' }
              ]"
              placeholder="Selecciona una opción"
              class="w-full text-primary"
            />
            <StudentFormEditMode />
          </div>
          <div class="divider"></div>
          <div class="flex flex-col">
            <div class="form-control self-center">
              <label class="label cursor-pointer">
                <input
                  type="checkbox"
                  v-model="archiveStudent"
                  class="checkbox checkbox-primary mr-2"
                />
                <span class="text-base">
                  Archivar estudiante (no se usará para entrenar modelos en el futuro)
                </span>
              </label>
            </div>
            <div class="self-center md:self-end">
              <button
                type="button"
                class="link link-secondary"
                @click="closeSupervisorStudentFormModal"
              >
                Cancelar
              </button>
              <button class="btn btn-sm btn-primary text-white self-end ml-4 mt-2">
                Actualizar
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </dialog>
</template>
