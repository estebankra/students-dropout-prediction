<script setup>
import { computed } from 'vue'
import { useAdminModelsStore } from '@/stores/admin/models'
import ConfirmModal from '@/components/modals/ConfirmNewTraining.vue'

const adminModelsStore = useAdminModelsStore()
const isTrainingInProgress = computed(() => adminModelsStore.isTraining)

const confirmTrainModel = async () => {
  await adminModelsStore.trainModel()
}

const openConfirmTrainModelModal = () => {
  document.getElementById('confirm_train_model').showModal()
}
</script>

<template>
  <ConfirmModal
    modalId="confirm_train_model"
    title="¿Estás seguro de ejecutar un nuevo entrenamiento?"
    :confirmAction="confirmTrainModel"
  />

  <button
    class="btn btn-sm btn-primary text-white self-end"
    @click="openConfirmTrainModelModal"
    :disabled="isTrainingInProgress"
  >
    <div class="flex items-center gap-2" v-if="isTrainingInProgress">
      <span class="loading loading-spinner loading-xs"></span>
      Entrenando un nuevo modelo
    </div>
    <div class="flex items-center gap-2" v-else>
      <span class="material-symbols-outlined text-xl">add</span>
      Entrenar nuevo modelo
    </div>
  </button>
</template>
