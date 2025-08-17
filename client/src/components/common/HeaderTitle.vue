<script setup>
import { useRouter } from 'vue-router'
import TitleH1 from '@/components/common/TitleH1.vue'

const router = useRouter()
</script>

<template>
  <div class="flex container items-center mx-auto gap-2 pt-4 md:pt-5 pb-3">
    <button
      v-if="router.currentRoute.value.name !== 'Home'"
      class="btn btn-primary btn-circle border border-gray-100 btn-sm"
      @click="router.back()"
    >
      <span class="rotate-180 material-symbols-outlined text-white text-2xl leading-none">
        chevron_right
      </span>
    </button>
    <TitleH1><slot></slot></TitleH1>
  </div>
</template>
