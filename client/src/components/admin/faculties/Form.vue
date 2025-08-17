<script setup>
import * as yup from 'yup'
import { ref, watch } from 'vue'
import { useForm } from 'vee-validate'
import { useToast } from 'vue-toastification'
import { useAdminFacultiesStore } from '@/stores/admin/faculties'
import FormInput from '@/components/common/FormInput.vue'
import FormSelect from '@/components/common/FormSelect.vue'

const emit = defineEmits(['cancelEditFaculty'])

const props = defineProps({
  facultyToEdit: { type: Object, default: null }
})

const adminFacultiesStore = useAdminFacultiesStore()
const toast = useToast()
const isEditing = ref(false)

const schema = yup.object().shape({
  short_name: yup.string().required('Campo requerido').min(2).max(200).label('Acrónimo'),
  long_name: yup.string().required('Campo requerido').min(2).max(200).label('Nombre'),
  active: yup.boolean().required('Campo requerido').label('Estado')
})

schema.describe({ value: { isEditing: isEditing.value } })

const { handleSubmit, resetForm, setValues } = useForm({
  validationSchema: schema,
  validateOnMount: false,
  initialValues: {
    short_name: '',
    long_name: '',
    active: true
  }
})

watch(
  () => props.facultyToEdit,
  (newFaculty) => {
    if (newFaculty) {
      isEditing.value = true
      setValues({
        short_name: newFaculty.short_name,
        long_name: newFaculty.long_name,
        active: newFaculty.active
      })
    } else {
      resetForm()
    }
  },
  { immediate: true }
)

const resetFacultyForm = () => {
  isEditing.value = false
  emit('cancelEditFaculty')
  resetForm()
}

const openAdminFacultyFormModal = () => {
  resetFacultyForm()
  document.getElementById('admin_faculties_form').showModal()
}

const closeAdminFacultyFormModal = () => {
  resetFacultyForm()
  document.getElementById('admin_faculties_form')?.close()
}

const onSubmit = handleSubmit(async (values) => {
  try {
    if (isEditing.value) {
      const updateData = { ...values }
      if (!updateData.password) {
        delete updateData.password
        delete updateData.confirm_password
      }

      await adminFacultiesStore.updateFaculty(props.facultyToEdit.id, updateData)
      closeAdminFacultyFormModal()
      toast.success('Facultad actualizada correctamente')
    } else {
      await adminFacultiesStore.createFaculty(values).then(() => {
        closeAdminFacultyFormModal()
        toast.success('Facultad creada correctamente')
      })
    }
  } catch (error) {
    toast.error('Ocurrió un error al procesar la solicitud')
  }
})
</script>

<template>
  <button class="btn btn-sm btn-primary text-white self-end" @click="openAdminFacultyFormModal">
    <span class="material-symbols-outlined text-xl">add</span>Nueva facultad
  </button>
  <dialog id="admin_faculties_form" class="modal">
    <div class="modal-box">
      <button
        @click="closeAdminFacultyFormModal"
        class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
      >
        ✕
      </button>
      <h3 class="text-lg font-bold">{{ isEditing ? 'Editar' : 'Crear' }} facultad</h3>

      <form @submit.prevent="onSubmit" class="flex flex-col">
        <div>
          <FormInput labelTop="Acrónimo" name="short_name" type="text" placeholder="" />
          <FormInput labelTop="Nombre" name="long_name" type="text" placeholder="" />
          <FormSelect
            v-if="isEditing"
            name="active"
            :options="[
              { value: 'true', label: 'Activo' },
              { value: 'false', label: 'Inactivo' }
            ]"
            labelTop="Estado"
            placeholder="Selecciona un estado"
          />
        </div>
        <button class="btn btn-primary text-white self-end mt-2">
          {{ isEditing ? 'Actualizar' : 'Crear' }}
        </button>
      </form>
    </div>
  </dialog>
</template>

