import axios from '@/lib/axios'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: null
  }),
  getters: {
    isAuthenticated: (state) => !!state.currentUser,
    getCurrentUser: (state) => state.currentUser
  },
  actions: {
    async login(user) {
      await axios.post('/auth/credentials/login', user)
      this.fetchCurrentUser()
    },
    async fetchCurrentUser() {
      const { data: user } = await axios.get('/users/me')
      this.currentUser = user
    },
    isUserAnAdmin() {
      return this.currentUser && this.currentUser.role === 'ADMIN'
    },
    isUserASupervisor() {
      return this.currentUser && this.currentUser.role === 'SUPERVISOR'
    },
    async logout() {
      await axios.get('/auth/logout')
      this.resetCurrentUser()
    },
    resetCurrentUser() {
      this.currentUser = null
    }
  }
})
