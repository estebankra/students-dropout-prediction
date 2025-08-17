import axios from '@/lib/axios'
import { defineStore } from 'pinia'

const modelsInitialState = {
  items: [],
  total: 0,
  limit: 0,
  offset: 0
}

export const useAdminModelsStore = defineStore('adminModels', {
  state: () => ({
    models: { ...modelsInitialState },
    isTrainingInProgress: false
  }),
  getters: {
    getModels: (state) => state.models,
    isTraining: (state) => state.isTrainingInProgress
  },
  actions: {
    async fetchModels({ offset = 0, limit = 25, sortBy = 'created_at', sortOrder = 'desc' }) {
      try {
        const params = new URLSearchParams()
        params.append('offset', offset)
        params.append('limit', limit)
        params.append('sort_by', sortBy)
        params.append('sort_order', sortOrder)

        const { data } = await axios.get(`/models?${params.toString()}`)

        this.models = {
          items: offset === 0 ? data.items : [...this.models.items, ...data.items],
          total: data.total,
          limit: data.limit,
          offset: data.offset
        }

        // Check if any model is currently training
        this.isTrainingInProgress = this.models.items.some(
          (model) => model.status === 'TRAINING' || model.status === 'PENDING'
        )
        return this.models
      } catch (error) {
        console.error('Error fetching models')
      }
    },
    async compareModels(model1Id, model2Id) {
      const { data } = await axios.get(
        `/admin/models/compare?model1_id=${model1Id}&model2_id=${model2Id}`
      )
      return data
    },
    async fetchSystemHealth() {
      const { data } = await axios.get(`/admin/dashboard/system-health`)
      return data
    },
    async setActiveModel(modelId) {
      try {
        const { data } = await axios.post(`/admin/models/${modelId}/activate`)
        return data
      } catch (error) {
        console.error('Error setting active model:', error)
        throw error
      }
    },
    async trainModel() {
      try {
        this.isTrainingInProgress = true
        const { data } = await axios.post('/admin/models')
        // After training is initiated, fetch the models to get the updated list with the new model
        await this.fetchModels({ offset: 0 })
        return data
      } catch (error) {
        console.error('Error training model:', error)
        throw error
      } finally {
        this.isTrainingInProgress = false
      }
    },
    resetModelsState() {
      this.models = { ...modelsInitialState }
    }
  }
})
