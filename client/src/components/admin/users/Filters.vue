<script setup>
import { ref } from 'vue'

const emit = defineEmits(['filtersUpdated'])

const filters = ref({ active: null, role: null })
</script>

<template>
  <label class="flex flex-col form-control w-full max-w-40">
    <div class="label">
      <span class="label-text">Estado</span>
    </div>
    <select
      class="select select-bordered select-sm"
      v-model="filters.active"
      @change="() => emit('filtersUpdated', filters)"
    >
      <option selected :value="null">Todos</option>
      <option :value="true">Activo</option>
      <option :value="false">Inactivo</option>
    </select>
  </label>

  <label class="flex flex-col form-control w-full max-w-40">
    <div class="label">
      <span class="label-text">Rol</span>
    </div>
    <select
      class="select select-bordered select-sm"
      v-model="filters.role"
      @change="() => emit('filtersUpdated', filters)"
    >
      <option selected :value="null">Todos</option>
      <option value="ADMIN">Administrador</option>
      <option value="SUPERVISOR">Supervisor</option>
    </select>
  </label>
</template>
