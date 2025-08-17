<script setup>
const props = defineProps({
  faculties: { type: Array, required: true, default: () => [] }
})

const emit = defineEmits(['editFaculty'])
const handleEditFaculty = (faculty) => {
  emit('editFaculty', faculty)
  document.getElementById('admin_faculties_form').showModal()
}
</script>
<template>
  <div class="overflow-x-auto">
    <table class="table table-xs lg:table-lg md:table-md sm:table-sm">
      <thead>
        <tr>
          <th>#</th>
          <th>Acrónimo</th>
          <th>Nombre</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(faculty, index) in props.faculties" :key="faculty.id">
          <th>{{ index + 1 }}</th>
          <td>{{ faculty.short_name }}</td>
          <td>{{ faculty.long_name }}</td>
          <td>
            <div v-if="faculty.active" class="badge badge-success badge-sm md:badge-md text-white">
              Activo
            </div>
            <div v-else class="badge badge-warning">Inactivo</div>
          </td>
          <td>
            <button class="btn btn-sm btn-ghost" @click="handleEditFaculty(faculty)">
              <span class="material-symbols-outlined">edit</span>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
