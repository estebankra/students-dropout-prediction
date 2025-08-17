<script setup>
import { getDropoutRiskText, formatDate } from '@/helpers/style'

const props = defineProps({
  studentToView: { type: Object, default: null },
  studentDropoutProbability: { type: Object, default: null }
})
</script>

<template>
  <div class="grid grid-cols-5 gap-2">
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Estado</span>
      </label>
      <p v-if="studentToView.estado === 'E'" class="bg-base-200 p-2 text-success rounded">
        Egresado
      </p>
      <p v-else-if="studentToView.estado === 'A'" class="bg-base-200 p-2 text-error rounded">
        Abandono
      </p>
      <p v-else class="bg-base-200 p-2 text-primary rounded">Vigente</p>
    </div>
    <div class="form-control col-span-2">
      <label class="label">
        <span class="label-text font-semibold">Nombre</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.first_name }} {{ studentToView.last_name }}
      </p>
    </div>
    <div class="form-control col-span-2">
      <label class="label">
        <span class="label-text font-semibold">Facultad</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        ({{ studentToView.faculty.short_name }}) {{ studentToView.faculty.long_name }}
      </p>
    </div>
  </div>

  <!-- Prediction Info -->
  <div v-if="studentDropoutProbability">
    <div class="divider">Información de predicción</div>
    <div class="grid grid-cols-3 gap-2">
      <div class="form-control">
        <label class="label">
          <span class="label-text font-semibold">Riesgo de deserción</span>
        </label>
        <p
          class="p-2 rounded bg-base-200"
          :class="getDropoutRiskText(studentDropoutProbability.dropout_probability)"
        >
          {{ (studentDropoutProbability.dropout_probability * 100).toFixed(1) }}%
        </p>
      </div>
      <div class="form-control">
        <label class="label">
          <span class="label-text font-semibold">Versión del modelo</span>
        </label>
        <p class="p-2 bg-base-200 rounded">
          {{ studentDropoutProbability.model_version }}
        </p>
      </div>
      <div class="form-control">
        <label class="label">
          <span class="label-text font-semibold">Fecha de predicción</span>
        </label>
        <p class="p-2 bg-base-200 rounded">
          {{ formatDate(studentDropoutProbability.created_at) }}
        </p>
      </div>
    </div>
  </div>

  <!-- Academic Info -->
  <div class="divider">Información académica</div>

  <div class="grid grid-cols-4 gap-2">
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Último semestre</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.ultimo_semestre_cursado || 'N/A' }}
      </p>
    </div>
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Año de egreso de secundaria</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.anio_egreso || 'N/A' }}
      </p>
    </div>
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Promedio en secundaria</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.promedio_secundaria || 'N/A' }}
      </p>
    </div>
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Colegios a los que asistió</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.cuantos_colegios_secundaria || 'N/A' }}
      </p>
    </div>
  </div>

  <!-- Personal Info -->
  <div class="divider">Información personal</div>

  <div class="grid grid-cols-3 gap-2">
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Estado Civil</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.estado_civil || 'N/A' }}
      </p>
    </div>
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Número de hijos</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.nro_hijos || '0' }}
      </p>
    </div>
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Vive con</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.vive_con || 'N/A' }}
      </p>
    </div>
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Situación Ocupacional</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.situacion_ocupacional || 'N/A' }}
      </p>
    </div>
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Sustento Económico</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.sustento_economico || 'N/A' }}
      </p>
    </div>
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Posee Enfermedad</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.posee_enfermedad || 'N/A' }}
      </p>
    </div>
  </div>

  <!-- Family Background -->
  <div class="divider">Antecedentes familiares</div>

  <div class="grid grid-cols-3 gap-2">
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Formación del Padre</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.formacion_academica_padre || 'N/A' }}
      </p>
    </div>
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Formación de la Madre</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.formacion_academica_madre || 'N/A' }}
      </p>
    </div>
    <div class="form-control">
      <label class="label">
        <span class="label-text font-semibold">Formación de Hermanos</span>
      </label>
      <p class="p-2 bg-base-200 rounded">
        {{ studentToView.formacion_academica_hermanos || 'N/A' }}
      </p>
    </div>
  </div>
</template>
