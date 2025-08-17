<script setup>
import { toRef } from 'vue'
import { useField } from 'vee-validate'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  value: {
    type: undefined,
    default: undefined
  },
  options: {
    type: Array,
    required: true // Array of options for the select dropdown
  },
  labelTop: {
    type: String,
    default: ''
  },
  labelLeft: {
    type: String,
    default: ''
  },
  successMessage: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Select an option'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const name = toRef(props, 'name')
const {
  value: selectValue,
  errorMessage,
  handleBlur,
  handleChange,
  meta
} = useField(name, undefined, {
  initialValue: props.value
})
</script>

<template>
  <div>
    <label
      :class="{
        'form-control w-full': !!labelTop,
        'input input-bordered flex items-center gap-2': !!labelLeft,
        'input-error': !!errorMessage,
        'input-success': meta.valid
      }"
    >
      <div class="label px-0 py-2">
        <div class="flex items-center gap-1 label-text">
          <span>{{ !!labelTop ? labelTop : labelLeft }}</span>
          <span v-if="meta.valid" class="material-symbols-outlined text-lg text-success">
            check_circle
          </span>
        </div>
      </div>
      <select
        :class="{ 'select select-bordered w-full': !!labelTop, grow: !!labelLeft }"
        :name="name"
        :id="name"
        v-model="selectValue"
        :disabled="disabled"
        @change="handleChange"
        @blur="handleBlur"
      >
        <option disabled value="">{{ placeholder }}</option>
        <option
          v-for="option in options"
          :key="option.value || option"
          :value="option.value || option"
        >
          {{ option.label || option }}
        </option>
      </select>
    </label>

    <p v-show="errorMessage" class="text-error">{{ errorMessage }}</p>
    <p v-show="successMessage && meta.valid" class="text-success">
      {{ successMessage }}
    </p>
  </div>
</template>
