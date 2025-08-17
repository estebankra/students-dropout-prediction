import axios from '@/lib/axios'
import { defineStore } from 'pinia'

const facultiesInitialState = {
  items: [],
  total: 0,
  limit: 0,
  offset: 0
}

export const useAdminFacultiesStore = defineStore('adminFaculties', {
  state: () => ({
    faculties: { ...facultiesInitialState }
  }),
  getters: {
    getFaculties: (state) => state.faculties
  },
  actions: {
    async fetchFaculties({ filters = null, offset = 0, limit = 25 }) {
      try {
        const params = new URLSearchParams()
        if (offset) params.append('offset', offset)
        if (limit) params.append('limit', limit)

        if (filters && filters.active != null) {
          params.append('active', filters.active)
        }

        const { data } = await axios.get(`/admin/faculties?${params.toString()}`)

        this.faculties = {
          items: offset === 0 ? data.items : [...this.faculties.items, ...data.items],
          total: data.total,
          limit: data.limit,
          offset: data.offset
        }
      } catch (error) {
        console.error('Error fetching faculties')
      }
    },
    async createFaculty(facultyData) {
      try {
        const { data } = await axios.post('/admin/faculties', facultyData)
        this.faculties.items.push(data)
        this.faculties.total += 1
        return data
      } catch (error) {
        console.error('Error creating faculty')
        throw null
      }
    },
    async updateFaculty(facultyId, facultyData) {
      try {
        const { data } = await axios.put(`/admin/faculties/${facultyId}`, facultyData)
        this.fetchFaculties({})
        return data
      } catch (error) {
        console.error('Error updating faculty')
        throw null
      }
    },
    resetFacultiesState() {
      this.faculties = { ...facultiesInitialState }
    }
  }
})

