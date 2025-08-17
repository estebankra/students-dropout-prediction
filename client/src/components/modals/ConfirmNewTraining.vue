<script setup>
const props = defineProps({
  modalId: { type: String, required: false, default: 'confirm_modal' },
  title: { type: String, required: false, default: 'Are you sure?' },
  description: { type: String, required: false, default: null },
  cancelAction: { type: Function, required: false },
  confirmAction: { type: Function, required: true }
})
</script>

<template>
  <dialog :id="modalId" class="modal">
    <div class="modal-box py-10">
      <form method="dialog">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
      </form>
      <div class="flex flex-col items-center gap-3">
        <h3 class="text-xl md:text-2xl max-w-96 py-2 font-semibold text-center">
          {{ props.title }}
        </h3>
      </div>

      <div class="modal-action justify-center">
        <form class="flex gap-2" method="dialog">
          <button @click="props.cancelAction" class="btn btn-ghost text-lg">Cancelar</button>
          <button @click="props.confirmAction" class="btn btn-primary text-white text-lg">
            Confirmar
          </button>
        </form>
      </div>
    </div>
  </dialog>
</template>
