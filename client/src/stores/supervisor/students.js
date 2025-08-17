import axios from '@/lib/axios'
import { defineStore } from 'pinia'

const studentsInitialState = {
  items: [],
  total: 0,
  limit: 0,
  offset: 0
}

export const useSupervisorStudentsStore = defineStore('supervisorStudents', {
  state: () => ({
    students: { ...studentsInitialState }
  }),
  getters: {
    getStudents: (state) => state.students
  },
  actions: {
    async fetchStudents({
      filters = null,
      offset = 0,
      limit = 25,
      modelVersionId = null,
      faculty = null
    }) {
      try {
        const params = new URLSearchParams()
        if (offset) params.append('offset', offset)
        if (limit) params.append('limit', limit)
        if (modelVersionId) params.append('model_version_id', modelVersionId)
        if (faculty) params.append('faculty', faculty)

        if (filters) {
          if (filters.dropoutProbability) {
            if (Number.isInteger(filters.dropoutProbability.min)) {
              params.append('min_probability', filters.dropoutProbability.min)
            }
            if (Number.isInteger(filters.dropoutProbability.max)) {
              params.append('max_probability', filters.dropoutProbability.max)
            }
          }

          if (filters.estado) {
            params.append('estado', filters.estado)
          }

          if (filters.archived) {
            params.append('archived', true)
          }

          if (filters.search) {
            params.append('search', filters.search)
          }
        }

        const { data } = await axios.get(`/supervisor/students?${params.toString()}`)

        this.students = {
          items: offset === 0 ? data.items : [...this.students.items, ...data.items],
          total: data.total,
          limit: data.limit,
          offset: data.offset
        }
        return this.students
      } catch (error) {
        console.error('Error fetching students')
      }
    },
    async updateStudent(studentId, formData) {
      try {
        const { data } = await axios.put(`/supervisor/students/${studentId}`, formData)
        return data
      } catch (error) {
        console.error('Error al actualizar la información del estudiante')
        throw error
      }
    },
    async exportStudents({ format = null, filters = null, modelVersionId = null, faculty = null }) {
      try {
        const params = new URLSearchParams()
        if (modelVersionId) params.append('model_version_id', modelVersionId)
        if (faculty) params.append('faculty', faculty)

        if (filters) {
          if (filters.dropoutProbability) {
            if (Number.isInteger(filters.dropoutProbability.min)) {
              params.append('min_probability', filters.dropoutProbability.min)
            }
            if (Number.isInteger(filters.dropoutProbability.max)) {
              params.append('max_probability', filters.dropoutProbability.max)
            }
          }

          if (filters.estado) {
            params.append('estado', filters.estado)
          }

          if (filters.archived) {
            params.append('archived', true)
          }

          if (filters.search) {
            params.append('search', filters.search)
          }
        }

        const response = await axios.get(
          `/supervisor/students/export/${format}?${params.toString()}`,
          { responseType: 'blob' }
        )
        return response
      } catch (error) {
        console.error(`Error al exportar a ${format} a la información del estudiante`)
        throw error
      }
    },
    async predictDropoutProbability({ modelVersionId = null }) {
      try {
        const params = new URLSearchParams()
        if (modelVersionId) params.append('model_version_id', modelVersionId)

        const { data } = await axios.post(`/predictions/predict?${params.toString()}`)
        return data
      } catch (err) {
        console.error('Error predicting dropout probability')
        throw err
      }
    },
    resetStudentsState() {
      this.students = { ...studentsInitialState }
    }
  }
})

