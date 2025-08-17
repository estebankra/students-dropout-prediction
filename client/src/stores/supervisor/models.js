import axios from '@/lib/axios'
import { defineStore } from 'pinia'

const modelsInitialState = {
  items: [],
  total: 0,
  limit: 0,
  offset: 0
}

export const useSupervisorModelsStore = defineStore('supervisorModels', {
  state: () => ({
    models: { ...modelsInitialState },
    selectedModel: null
  }),
  getters: {
    getModels: (state) => state.models,
    getSelectedModel: (state) => state.selectedModel
  },
  actions: {
    async fetchModels() {
      try {
        const params = new URLSearchParams()
        params.append('offset', 0)
        params.append('limit', 100)
        params.append('status', 'COMPLETED')

        const { data } = await axios.get(`/models?${params.toString()}`)
        this.models = {
          items: data.items,
          total: data.total,
          limit: data.limit,
          offset: data.offset
        }
        return this.models
      } catch (error) {
        console.error('Error fetching models')
      }
    },
    setSelectedModel(model) {
      this.selectedModel = model
    },
    resetModelsState() {
      this.models = { ...modelsInitialState }
    }
  }
})

