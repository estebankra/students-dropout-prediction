<script setup>
import { Form } from 'vee-validate'
import { onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { useStudentsStore } from '@/stores/students'
import { studentSchema } from '@/schemas/students'
import { useRouter } from 'vue-router'
import { useFacultiesStore } from '@/stores/faculties'
import StudentFormCreateMode from '@/components/students/FormCreateEditMode.vue'

const toast = useToast()
const router = useRouter()
const studentsStore = useStudentsStore()
const facultiesStore = useFacultiesStore()

const onSubmit = async (values, form) => {
  await studentsStore
    .registerStudent(values)
    .then(() => {
      toast.success('Información registrada exitosamente')
      form.resetForm()
      router.push('/students')
    })
    .catch(() => {
      toast.error('Error al registrar la información del estudiante')
    })
}

const loadData = async () => {
  await facultiesStore.fetchFaculties({})
}

onMounted(() => loadData())
</script>
<template>
  <div class="py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <div class="border shadow-md rounded-lg px-8 py-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Registro de Estudiante</h2>
        <Form @submit="onSubmit" :validation-schema="studentSchema" v-slot="{ isSubmitting }">
          <div class="flex flex-col gap-2">
            <StudentFormCreateMode />
            <div class="flex justify-end pt-4">
              <button
                type="submit"
                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                :disabled="isSubmitting"
              >
                {{ isSubmitting ? 'Enviando...' : 'Registrar' }}
              </button>
            </div>
          </div>
        </Form>
      </div>
    </div>
  </div>
</template>
