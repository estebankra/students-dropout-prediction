<script setup>
import { ref, onMounted } from 'vue'
import { useAdminModelsStore } from '@/stores/admin/models'
import { formatDate } from '@/helpers/style'
import TitleH2 from '@/components/common/TitleH2.vue'
import LoadingState from '@/components/common/LoadingState.vue'

const adminModelsStore = useAdminModelsStore()

const systemHealth = ref({
  cpu_usage: 0,
  memory_usage: 0,
  disk_usage: 0,
  api_status: 'offline',
  database_status: 'offline',
  last_backup: null,
  uptime: 0
})

const isLoading = ref(true)
const error = ref(null)

const fetchSystemHealth = async () => {
  try {
    isLoading.value = true
    error.value = null
    systemHealth.value = await adminModelsStore.fetchSystemHealth()
  } catch (err) {
    error.value = 'Error al cargar información del sistema: ' + err.message
    console.error('Error fetching system health:', err)
  } finally {
    isLoading.value = false
  }
}

const getStatusColor = (status) => {
  return status === 'online' ? 'text-success' : 'text-error'
}

const getUsageColor = (percentage) => {
  if (percentage < 50) return 'text-success'
  if (percentage < 80) return 'text-warning'
  return 'text-error'
}

onMounted(() => {
  fetchSystemHealth()
})
</script>

<template>
  <section class="flex flex-col gap-4">
    <div class="flex justify-between">
      <TitleH2>Estado del sistema</TitleH2>
      <button class="btn btn-primary btn-sm text-white" @click="fetchSystemHealth">
        Actualizar<span class="material-symbols-outlined text-xl">refresh</span>
      </button>
    </div>

    <LoadingState v-if="isLoading" />

    <div v-else-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Resource Usage -->
      <div class="card bg-base-100 shadow border">
        <div class="card-body">
          <h3 class="card-title">Uso de recursos</h3>

          <div class="mt-2">
            <div class="flex justify-between mb-1">
              <span>CPU</span>
              <span :class="getUsageColor(systemHealth.cpu_usage)"
                >{{ systemHealth.cpu_usage }}%</span
              >
            </div>
            <progress
              class="progress"
              :class="getUsageColor(systemHealth.cpu_usage)"
              :value="systemHealth.cpu_usage"
              max="100"
            ></progress>
          </div>

          <div class="mt-2">
            <div class="flex justify-between mb-1">
              <span>Memoria</span>
              <span :class="getUsageColor(systemHealth.memory_usage)"
                >{{ systemHealth.memory_usage }}%</span
              >
            </div>
            <progress
              class="progress"
              :class="getUsageColor(systemHealth.memory_usage)"
              :value="systemHealth.memory_usage"
              max="100"
            ></progress>
          </div>

          <div class="mt-2">
            <div class="flex justify-between mb-1">
              <span>Disco</span>
              <span :class="getUsageColor(systemHealth.disk_usage)"
                >{{ systemHealth.disk_usage }}%</span
              >
            </div>
            <progress
              class="progress"
              :class="getUsageColor(systemHealth.disk_usage)"
              :value="systemHealth.disk_usage"
              max="100"
            ></progress>
          </div>
        </div>
      </div>

      <!-- Service Status -->
      <div class="card bg-base-100 shadow border">
        <div class="card-body">
          <h3 class="card-title">Estado de servicios</h3>

          <div class="overflow-x-auto">
            <table class="table">
              <tbody>
                <tr>
                  <td>API</td>
                  <td :class="getStatusColor(systemHealth.api_status)">
                    <div class="flex items-center gap-2">
                      <div
                        class="badge"
                        :class="
                          systemHealth.api_status === 'online' ? 'badge-success' : 'badge-error'
                        "
                      ></div>
                      {{ systemHealth.api_status === 'online' ? 'En línea' : 'Fuera de línea' }}
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>Base de datos</td>
                  <td :class="getStatusColor(systemHealth.database_status)">
                    <div class="flex items-center gap-2">
                      <div
                        class="badge"
                        :class="
                          systemHealth.database_status === 'online'
                            ? 'badge-success'
                            : 'badge-error'
                        "
                      ></div>
                      {{
                        systemHealth.database_status === 'online' ? 'En línea' : 'Fuera de línea'
                      }}
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>Último respaldo</td>
                  <td>{{ formatDate(systemHealth.last_backup) }}</td>
                </tr>
                <tr>
                  <td>Tiempo activo</td>
                  <td>{{ systemHealth.uptime }} días</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

