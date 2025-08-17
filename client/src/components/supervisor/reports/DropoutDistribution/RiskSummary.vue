<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

defineProps({
  riskSummary: {
    type: Object,
    required: true
  },
  totalStudents: {
    type: Number,
    required: true
  }
})

const navigateToStudentsList = (minRisk, maxRisk) => {
  router.push({
    name: 'SupervisorStudents',
    query: { 'min-risk': minRisk, 'max-risk': maxRisk }
  })
}
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
    <!-- Total Students Card -->
    <div class="card bg-accent/10 shadow-md">
      <div class="card-body p-4">
        <h4 class="card-title text-lg">Total de estudiantes</h4>
        <p class="text-3xl font-bold">{{ totalStudents }}</p>
      </div>
    </div>

    <!-- High Risk Card -->
    <div
      class="card bg-error text-error-content shadow-md cursor-pointer hover:shadow-lg transition-shadow"
      @click="navigateToStudentsList(70, 100)"
    >
      <div class="card-body p-4">
        <h4 class="card-title text-lg">Riesgo alto (70-100%)</h4>
        <p class="text-3xl font-bold">{{ riskSummary.high_risk.count }}</p>
        <p class="text-sm">{{ riskSummary.high_risk.percentage }}% of students</p>
      </div>
    </div>

    <!-- Medium Risk Card -->
    <div
      class="card bg-warning text-warning-content shadow-md cursor-pointer hover:shadow-lg transition-shadow"
      @click="navigateToStudentsList(40, 70)"
    >
      <div class="card-body p-4">
        <h4 class="card-title text-lg">Riesgo medio (40-70%)</h4>
        <p class="text-3xl font-bold">{{ riskSummary.medium_risk.count }}</p>
        <p class="text-sm">{{ riskSummary.medium_risk.percentage }}% of students</p>
      </div>
    </div>

    <!-- Low Risk Card -->
    <div
      class="card bg-success text-success-content shadow-md cursor-pointer hover:shadow-lg transition-shadow border"
      @click="navigateToStudentsList(0, 40)"
    >
      <div class="card-body p-4">
        <h4 class="card-title text-lg">Riesgo bajo (0-40%)</h4>
        <p class="text-3xl font-bold">{{ riskSummary.low_risk.count }}</p>
        <p class="text-sm">{{ riskSummary.low_risk.percentage }}% of students</p>
      </div>
    </div>
  </div>
</template>

