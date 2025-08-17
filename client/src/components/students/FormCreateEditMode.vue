<script setup>
import { computed } from 'vue'
import { useFacultiesStore } from '@/stores/faculties'
import { formacionOptions } from '@/schemas/students'
import FormInput from '@/components/common/FormInput.vue'
import FormSelect from '@/components/common/FormSelect.vue'

const facultiesStore = useFacultiesStore()
const faculties = computed(() => facultiesStore.getFaculties)

const props = defineProps({
  mode: { type: String, required: false, default: 'create' }
})

const getFacultyOptions = () => {
  const options = []
  for (const faculty of faculties.value.items) {
    options.push({
      value: faculty.short_name,
      label: `(${faculty.short_name}) ${faculty.long_name}`
    })
  }
  return options
}
</script>

<template>
  <div v-if="faculties && faculties.items.length > 0">
    <div class="flex gap-2">
      <FormInput labelTop="Nombre" name="first_name" type="text" placeholder="" class="w-full" />
      <FormInput labelTop="Apellido" name="last_name" type="text" placeholder="" class="w-full" />
    </div>
    <div class="flex gap-2">
      <FormInput
        labelTop="Fecha de Nacimiento"
        name="fecha_nac"
        type="date"
        placeholder=""
        class="w-full"
      />
      <FormSelect
        labelTop="Facultad"
        name="faculty_short_name"
        :options="getFacultyOptions()"
        placeholder="Selecciona una opción"
        class="w-full"
      />
    </div>
    <div class="divider">Información académica</div>
    <div class="flex gap-2 flex-wrap sm:flex-nowrap">
      <FormInput
        v-if="props.mode == 'edit'"
        labelTop="Último semestre cursado"
        name="ultimo_semestre_cursado"
        type="number"
        placeholder=""
        class="w-full"
      />
      <FormInput
        labelTop="Año de egreso de secundaria"
        name="anio_egreso"
        type="text"
        placeholder=""
        class="w-full"
      />
      <FormSelect
        labelTop="Promedio en secundaria"
        name="promedio_secundaria"
        :options="[
          { value: '4 a 5', label: '4 a 5' },
          { value: '3 a 3,99', label: '3 a 3,99' },
          { value: '2,5 a 2,99', label: '2,5 a 2,99' },
          { value: '2 a 2,49', label: '2 a 2,49' }
        ]"
        placeholder="Selecciona una opción"
        class="w-full"
      />
      <FormInput
        labelTop="Colegios a los que asistió"
        name="cuantos_colegios_secundaria"
        type="number"
        class="w-full"
      />
    </div>
    <div class="divider">Información personal</div>
    <div class="flex gap-2 flex-wrap sm:flex-nowrap">
      <FormSelect
        labelTop="Estado Civil"
        name="estado_civil"
        :options="[
          { value: 'S', label: 'Soltero' },
          { value: 'C', label: 'Casado' },
          { value: 'D', label: 'Divorciado' }
        ]"
        placeholder="Selecciona una opción"
        class="w-full"
      />
      <FormInput
        labelTop="Número de hijos"
        name="nro_hijos"
        type="number"
        placeholder=""
        class="w-full"
      />
      <FormSelect
        labelTop="Vive con"
        name="vive_con"
        :options="[
          { value: 'Solo', label: 'Solo' },
          { value: 'Familia nuclear', label: 'Familia nuclear' },
          { value: 'Familia extensa', label: 'Familia extensa' },
          { value: 'Companeros', label: 'Compañeros de clase/trabajo' }
        ]"
        placeholder="Selecciona una opción"
        class="w-full"
      />
    </div>
    <div class="flex gap-2 flex-wrap sm:flex-nowrap">
      <FormSelect
        labelTop="Situación Ocupacional"
        name="situacion_ocupacional"
        :options="[
          { value: 'Solo Estudio', label: 'Solo Estudio' },
          { value: 'Trab Todo el dia', label: 'Trabajo Todo el día' },
          { value: 'Trab 1/2 dia', label: 'Trabajo 1/2 día' },
          { value: 'Trab con cambio de turno', label: 'Trabajo con cambio de turno' }
        ]"
        placeholder="Selecciona una opción"
        class="w-full"
      />
      <FormSelect
        labelTop="Sustento Económico"
        name="sustento_economico"
        :options="[
          { value: 'Familia', label: 'Familia' },
          { value: 'Trabajo', label: 'Trabajo' },
          { value: 'Becas', label: 'Becas' },
          { value: 'Beca parcial', label: 'Beca parcial' }
        ]"
        placeholder="Selecciona una opción"
        class="w-full"
      />
      <FormSelect
        labelTop="Posee enfermedad"
        name="posee_enfermedad"
        :options="[
          { value: 'No', label: 'No' },
          { value: 'Leve', label: 'Leve' },
          { value: 'Compleja', label: 'Compleja' }
        ]"
        placeholder="Selecciona una opción"
        class="w-full"
      />
    </div>
    <div class="divider">Antecedentes familiares</div>
    <div class="flex gap-2 flex-wrap sm:flex-nowrap">
      <FormSelect
        labelTop="Formación del Padre"
        name="formacion_academica_padre"
        :options="formacionOptions"
        placeholder="Selecciona una opción"
        class="w-full"
      />
      <FormSelect
        labelTop="Formación de la Madre"
        name="formacion_academica_madre"
        :options="formacionOptions"
        placeholder="Selecciona una opción"
        class="w-full"
      />
      <FormSelect
        labelTop="Formación de Hermanos"
        name="formacion_academica_hermanos"
        :options="formacionOptions"
        placeholder="Selecciona una opción"
        class="w-full"
      />
    </div>
  </div>
</template>

