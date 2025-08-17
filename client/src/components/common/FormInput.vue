<script setup>
import { toRef } from 'vue'
import { useField } from 'vee-validate'

const props = defineProps({
  type: {
    type: String,
    default: 'text'
  },
  value: {
    type: undefined,
    default: undefined
  },
  name: {
    type: String,
    required: true
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
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const name = toRef(props, 'name')
const {
  value: inputValue,
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
      <input
        :class="{ 'input input-bordered w-full': !!labelTop, grow: !!labelLeft }"
        :name="name"
        :id="name"
        :type="type"
        :value="inputValue"
        :placeholder="placeholder"
        :disabled="disabled"
        @input="handleChange"
        @blur="handleBlur"
      />
    </label>

    <p v-show="errorMessage" class="text-error">{{ errorMessage }}</p>
    <p v-show="successMessage && meta.valid" class="text-success">
      {{ successMessage }}
    </p>
  </div>
</template>
