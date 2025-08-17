<script setup>
import * as yup from 'yup'
import { ref, watch } from 'vue'
import { useForm } from 'vee-validate'
import { useToast } from 'vue-toastification'
import { useAdminUsersStore } from '@/stores/admin/users'
import FormInput from '@/components/common/FormInput.vue'
import FormSelect from '@/components/common/FormSelect.vue'

const emit = defineEmits(['cancelEditUser'])

const props = defineProps({
  userToEdit: { type: Object, default: null }
})

const adminUsersStore = useAdminUsersStore()
const toast = useToast()
const isEditing = ref(false)

const rolesOptions = [
  { value: 'ADMIN', label: 'Administrador' },
  { value: 'SUPERVISOR', label: 'Supervisor' }
]

const statusOptions = [
  { value: 'true', label: 'Activo' },
  { value: 'false', label: 'Inactivo' }
]

const schema = yup.object().shape({
  password: yup.string().when([], {
    is: () => isEditing.value,
    then: () =>
      yup
        .string()
        .nullable()
        .test('password-validation', 'La contraseña debe ser de 8-128 caracteres', (value) => {
          if (!value) return true // Empty is OK
          return value.length >= 8 && value.length <= 128
        })
        .label('Contraseña'),
    otherwise: () => yup.string().required('Campo requerido').min(8).max(128).label('Contraseña')
  }),
  first_name: yup.string().required('Campo requerido').min(2).max(200).label('Nombre'),
  last_name: yup.string().required('Campo requerido').min(2).max(200).label('Apellido'),
  email: yup.string().email().required('Campo requerido').label('Correo'),
  confirm_password: yup.string().when('password', {
    is: (val) => val && val.length > 0,
    then: () =>
      yup
        .string()
        .required('Campo requerido')
        .oneOf([yup.ref('password')], 'Las contraseñas no coinciden')
        .label('Confirmar contraseña'),
    otherwise: () => yup.string().optional()
  }),
  role: yup.string().required('Campo requerido').label('Rol'),
  active: yup.boolean().required('Campo requerido').label('Estado')
})

schema.describe({ value: { isEditing: isEditing.value } })

const { handleSubmit, resetForm, setValues } = useForm({
  validationSchema: schema,
  validateOnMount: false,
  initialValues: {
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirm_password: '',
    role: '',
    active: true
  }
})

watch(
  () => props.userToEdit,
  (newUser) => {
    if (newUser) {
      isEditing.value = true
      setValues({
        first_name: newUser.first_name,
        last_name: newUser.last_name,
        email: newUser.email,
        role: newUser.role,
        active: newUser.active,
        password: '',
        confirm_password: ''
      })
    } else {
      resetForm()
    }
  },
  { immediate: true }
)

const resetUserForm = () => {
  isEditing.value = false
  emit('cancelEditUser')
  resetForm()
}

const openAdminUserFormModal = () => {
  resetUserForm()
  document.getElementById('admin_users_form').showModal()
}

const closeAdminUserFormModal = () => {
  resetUserForm()
  document.getElementById('admin_users_form')?.close()
}

const onSubmit = handleSubmit(async (values) => {
  try {
    if (isEditing.value) {
      const updateData = { ...values }
      if (!updateData.password) {
        delete updateData.password
        delete updateData.confirm_password
      }

      await adminUsersStore.updateUser(props.userToEdit.id, updateData)
      closeAdminUserFormModal()
      toast.success('Usuario actualizado correctamente')
    } else {
      await adminUsersStore.createUser(values).then(() => {
        closeAdminUserFormModal()
        toast.success('Usuario creado correctamente')
      })
    }
  } catch (error) {
    toast.error('Ocurrió un error al procesar la solicitud')
  }
})
</script>

<template>
  <button class="btn btn-sm btn-primary text-white self-end" @click="openAdminUserFormModal">
    <span class="material-symbols-outlined text-xl">add</span>Nuevo usuario
  </button>
  <dialog id="admin_users_form" class="modal">
    <div class="modal-box">
      <button
        @click="closeAdminUserFormModal"
        class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
      >
        ✕
      </button>
      <h3 class="text-lg font-bold">{{ isEditing ? 'Editar' : 'Crear' }} usuario</h3>

      <form @submit.prevent="onSubmit" class="flex flex-col">
        <div>
          <FormInput labelTop="Nombre" name="first_name" type="text" placeholder="" />
          <FormInput labelTop="Apellido" name="last_name" type="text" placeholder="" />
          <FormInput labelTop="Correo" name="email" type="email" placeholder="" />
          <FormSelect
            name="role"
            :options="rolesOptions"
            labelTop="Rol"
            placeholder="Selecciona un rol"
          />
          <FormSelect
            v-if="isEditing"
            name="active"
            :options="statusOptions"
            labelTop="Estado"
            placeholder="Selecciona un estado"
          />
          <div v-if="isEditing" class="divider"></div>
          <FormInput labelTop="Contraseña" name="password" type="password" placeholder="" />
          <FormInput
            labelTop="Confirmar contraseña"
            name="confirm_password"
            type="password"
            placeholder=""
          />
        </div>
        <button class="btn btn-primary text-white self-end mt-2">
          {{ isEditing ? 'Actualizar' : 'Crear' }}
        </button>
      </form>
    </div>
  </dialog>
</template>

