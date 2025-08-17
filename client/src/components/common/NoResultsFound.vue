<script setup>
const props = defineProps({
  text: { type: String, required: false, default: 'No pudimos encontrar ningún resultado' }
})
</script>

<template>
  <div class="flex justify-center py-16 text-xl md:text-2xl">{{ props.text }}</div>
</template>

