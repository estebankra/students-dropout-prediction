<script setup>
import { ref, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { useSupervisorModelsStore } from '@/stores/supervisor/models'
import { useSupervisorStudentsStore } from '@/stores/supervisor/students'
import ConfirmModal from '@/components/modals/ConfirmNewPredict.vue'

const props = defineProps({
  buttonSize: { type: String, default: 'btn-sm' }
})

const isPredicting = ref(false)
const supervisorModelsStore = useSupervisorModelsStore()
const supervisorStudentsStore = useSupervisorStudentsStore()
const toast = useToast()
const selectedModelVersion = computed(() => supervisorModelsStore.getSelectedModel)

const confirmPredictDropoutProbability = async () => {
  isPredicting.value = true
  await supervisorStudentsStore
    .predictDropoutProbability({ modelVersionId: selectedModelVersion.value.id })
    .then(() => {
      toast.success('Predicción calculada correctamente. Revisa los resultados.')
    })
    .finally(() => {
      isPredicting.value = false
    })
}

const openConfirmPredictDropoutProbabilityModal = () => {
  document.getElementById('confirm_predict_dropout_probability').showModal()
}
</script>

<template>
  <ConfirmModal
    modalId="confirm_predict_dropout_probability"
    title="¿Estás seguro de ejecutar una nueva tarea para calcular el riesgo de deserción?"
    :confirmAction="confirmPredictDropoutProbability"
    :selectedModelVersion="selectedModelVersion"
  />

  <button
    @click="openConfirmPredictDropoutProbabilityModal"
    class="btn btn-primary text-white"
    :class="props.buttonSize"
    :disabled="isPredicting"
  >
    <span v-if="isPredicting" class="loading loading-spinner loading-sm"></span>
    <span v-else class="material-symbols-outlined text-xl rotate-180">add_chart</span>
    Calcular riesgo de deserción
  </button>
</template>

