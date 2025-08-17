<script setup>
const props = defineProps({
  users: { type: Array, required: true, default: () => [] }
})

const emit = defineEmits(['editUser'])
const handleEditUser = (user) => {
  emit('editUser', user)
  document.getElementById('admin_users_form').showModal()
}
</script>
<template>
  <div class="overflow-x-auto">
    <table class="table table-xs lg:table-lg md:table-md sm:table-sm">
      <thead>
        <tr>
          <th>#</th>
          <th>Nombre</th>
          <th>Apellido</th>
          <th>Correo</th>
          <th>Rol</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in props.users" :key="user.id">
          <th>{{ index + 1 }}</th>
          <td>{{ user.first_name }}</td>
          <td>{{ user.last_name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role == 'ADMIN' ? 'Administrador' : 'Supervisor' }}</td>
          <td>
            <div v-if="user.active" class="badge badge-success badge-sm md:badge-md text-white">
              Activo
            </div>
            <div v-else class="badge badge-warning">Inactivo</div>
          </td>
          <td>
            <button class="btn btn-sm btn-ghost" @click="handleEditUser(user)">
              <span class="material-symbols-outlined">edit</span>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
