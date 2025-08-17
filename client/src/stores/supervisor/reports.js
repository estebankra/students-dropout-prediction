import axios from '@/lib/axios'
import { defineStore } from 'pinia'

export const useSupervisorReportsStore = defineStore('supervisorReports', {
  actions: {
    async fetchDropoutDistribution({ modelVersionId = null, faculty = null }) {
      try {
        const params = new URLSearchParams()
        if (modelVersionId) params.append('model_version_id', modelVersionId)
        if (faculty) params.append('faculty', faculty)

        const { data } = await axios.get(
          `/supervisor/reports/dropout-distribution?${params.toString()}`
        )
        return data
      } catch (error) {
        console.error('Error fetching dropout distribution report', error)
        throw error
      }
    },
    async fetchDropoutFactorsImpact({ modelVersionId = null, faculty = null }) {
      try {
        const params = new URLSearchParams()
        if (modelVersionId) params.append('model_version_id', modelVersionId)
        if (faculty) params.append('faculty', faculty)

        const { data } = await axios.get(
          `/supervisor/reports/dropout-factors-impact?${params.toString()}`
        )
        return data
      } catch (error) {
        console.error('Error fetching dropout factors impact report', error)
        throw error
      }
    },
    async fetchFacultyDropoutDistribution({ modelVersionId = null }) {
      try {
        const params = new URLSearchParams()
        if (modelVersionId) params.append('model_version_id', modelVersionId)

        const { data } = await axios.get(
          `/supervisor/reports/faculty-dropout-distribution?${params.toString()}`
        )
        return data
      } catch (error) {
        console.error('Error fetching faculty dropout distribution report', error)
        throw error
      }
    }
  }
})
