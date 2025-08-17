import axios from '@/lib/axios'
import { defineStore } from 'pinia'

export const useAdminStatsStore = defineStore('adminStats', {
  state: () => ({
    stats: null
  }),
  getters: {
    getStats: (state) => state.stats
  },
  actions: {
    async fetchStats() {
      try {
        const { data } = await axios.get('/admin/dashboard/stats')
        this.stats = data
      } catch (error) {
        console.error('Error fetching stats')
      }
    },
    resetStatsState() {
      this.stats = null
    }
  }
})

