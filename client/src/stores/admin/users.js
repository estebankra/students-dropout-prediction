import axios from '@/lib/axios'
import { defineStore } from 'pinia'

const usersInitialState = {
  items: [],
  total: 0,
  limit: 0,
  offset: 0
}

export const useAdminUsersStore = defineStore('adminUsers', {
  state: () => ({
    users: { ...usersInitialState }
  }),
  getters: {
    getUsers: (state) => state.users
  },
  actions: {
    async fetchUsers({ filters = null, offset = 0, limit = 25 }) {
      try {
        const params = new URLSearchParams()
        if (offset) params.append('offset', offset)
        if (limit) params.append('limit', limit)

        if (filters && filters.active != null) {
          params.append('active', filters.active)
        }

        if (filters && filters.role) {
          params.append('role', filters.role)
        }

        const { data } = await axios.get(`/admin/users?${params.toString()}`)

        this.users = {
          items: offset === 0 ? data.items : [...this.users.items, ...data.items],
          total: data.total,
          limit: data.limit,
          offset: data.offset
        }
      } catch (error) {
        console.error('Error fetching users')
      }
    },
    async createUser(userData) {
      try {
        const { data } = await axios.post('/admin/users', userData)
        this.users.items.push(data)
        this.users.total += 1
        return data
      } catch (error) {
        console.error('Error creating user')
        throw null
      }
    },

    async updateUser(userId, userData) {
      try {
        const { data } = await axios.put(`/admin/users/${userId}`, userData)
        this.fetchUsers({})
        return data
      } catch (error) {
        console.error('Error updating user')
        throw null
      }
    },
    resetUsersState() {
      this.users = { ...usersInitialState }
    }
  }
})
