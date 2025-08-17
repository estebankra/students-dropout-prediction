<script setup>
import { useRouter } from 'vue-router'
import { formatDate } from '@/helpers/style'
import TitleH2 from '@/components/common/TitleH2.vue'

const router = useRouter()

const props = defineProps({
  currentModel: { type: Object, required: true }
})

const navigateToModels = () => {
  router.push('/admin/models')
}
</script>

<template>
  <section class="flex flex-col gap-4">
    <div class="flex justify-between">
      <TitleH2>Modelo predictivo actual</TitleH2>
      <button class="btn btn-primary btn-sm text-white" @click="navigateToModels">
        Entrenar nuevo modelo<span class="material-symbols-outlined text-xl">chevron_right</span>
      </button>
    </div>
    <div class="w-full stats shadow border">
      <div class="stat place-items-center">
        <div class="stat-title">Versión actual</div>
        <div class="stat-value">{{ props.currentModel.version }}</div>
        <div class="stat-desc">Entrenado el {{ formatDate(props.currentModel.created_at) }}</div>
      </div>

      <div class="stat place-items-center">
        <div class="stat-title">Rendimiento</div>
        <div class="stat-value">{{ (props.currentModel.f1_score * 100).toFixed(1) }}%</div>
        <div class="stat-desc">F1 Score</div>
      </div>

      <div class="stat place-items-center">
        <div class="stat-title">Datos</div>
        <div class="stat-value">{{ props.currentModel.num_samples || 0 }}</div>
        <div class="stat-desc">Cantidad de datos</div>
      </div>
    </div>
  </section>
</template>

