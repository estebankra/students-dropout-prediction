import axios from '@/lib/axios'
import { defineStore } from 'pinia'

export const useStudentsStore = defineStore('students', {
  actions: {
    async registerStudent(formData) {
      try {
        const { data } = await axios.post('/students/register', formData)
        return data
      } catch (error) {
        console.error('Error al registrar la información del estudiante')
        throw error
      }
    }
  }
})

