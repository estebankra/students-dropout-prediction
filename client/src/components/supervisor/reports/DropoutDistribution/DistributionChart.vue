<script setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'

// Register Chart.js components
Chart.register(...registerables)

const props = defineProps({
  distribution: {
    type: Object,
    required: true
  },
  percentages: {
    type: Object,
    required: true
  }
})

const chartCanvas = ref(null)
let chart = null

const getRiskColor = (percentage) => {
  if (percentage < 40) {
    return {
      background: 'rgba(34, 197, 94, 0.6)',
      border: 'rgb(22, 163, 74)'
    }
  }
  if (percentage < 70) {
    return {
      background: 'rgba(234, 179, 8, 0.6)',
      border: 'rgb(202, 138, 4)'
    }
  }
  return {
    background: 'rgba(239, 68, 68, 0.6)',
    border: 'rgb(220, 38, 38)'
  }
}

const createChart = () => {
  if (!chartCanvas.value) return

  const labels = Object.keys(props.distribution)
  const data = Object.values(props.percentages)

  const backgroundColors = labels.map(
    (label) => getRiskColor(parseInt(label.split('-')[0])).background
  )
  const borderColors = labels.map((label) => getRiskColor(parseInt(label.split('-')[0])).border)

  // Destroy existing chart if it exists
  if (chart) {
    chart.destroy()
    chart = null
  }

  const ctx = chartCanvas.value.getContext('2d')
  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          data: data,
          backgroundColor: backgroundColors,
          borderColor: borderColors,
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: {
            generateLabels: () => {
              return [
                {
                  text: 'Riesgo bajo (0-40%)',
                  fillStyle: 'rgba(34, 197, 94, 0.6)'
                },
                {
                  text: 'Riesgo medio (40-70%)',
                  fillStyle: 'rgba(234, 179, 8, 0.6)'
                },
                {
                  text: 'Riesgo alto (70-100%)',
                  fillStyle: 'rgba(239, 68, 68, 0.6)'
                }
              ]
            }
          }
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const label = context.label
              const value = context.raw
              const students = props.distribution[label]
              return `${label}: ${value}% (${students} students)`
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            callback: (value) => `${value}%`
          }
        }
      }
    }
  })
}

onMounted(() => {
  createChart()
})

watch(
  () => props.distribution,
  () => {
    createChart()
  },
  { deep: true }
)
</script>

<template>
  <div class="w-full h-80">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>
