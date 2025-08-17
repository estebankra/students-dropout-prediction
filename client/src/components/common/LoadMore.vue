<script setup>
const emit = defineEmits(['loadMore'])
</script>

<template>
  <div class="flex justify-center pt-0 pb-6">
    <button
      @click="() => emit('loadMore')"
      class="btn btn-secondary h-8 md:h-9 min-h-8 text-base md:text-base text-white"
    >
      <span>Load more</span>
    </button>
  </div>
</template>
