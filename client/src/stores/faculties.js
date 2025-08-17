import axios from '@/lib/axios'
import { defineStore } from 'pinia'

export const useFacultiesStore = defineStore('faculties', {
  state: () => ({
    faculties: null,
    selectedFaculty: null
  }),
  getters: {
    getFaculties: (state) => state.faculties,
    getSelectedFaculty: (state) => state.selectedFaculty
  },
  actions: {
    async fetchFaculties({ offset = 0, limit = 25 }) {
      try {
        const params = new URLSearchParams()
        params.append('offset', offset)
        params.append('limit', limit)

        const { data } = await axios.get(`/faculties?${params.toString()}`)

        this.faculties = {
          items: offset === 0 ? data.items : [...this.models.items, ...data.items],
          total: data.total,
          limit: data.limit,
          offset: data.offset
        }

        return this.faculties
      } catch (error) {
        console.error('Error fetching faculties')
      }
    },
    setSelectedFaculty(faculty) {
      this.selectedFaculty = faculty
    },
    resetFaculties() {
      this.faculties = null
    }
  }
})

