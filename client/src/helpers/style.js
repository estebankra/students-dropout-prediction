export const getDropoutRiskClass = (probability) => {
  if (probability >= 0.7) {
    return 'badge-error' // High risk (red)
  } else if (probability >= 0.4) {
    return 'badge-warning' // Medium risk (yellow/orange)
  } else {
    return 'badge-success' // Low risk (green)
  }
}

export const getDropoutRiskText = (probability) => {
  if (probability >= 0.7) {
    return 'text-error' // High risk (red)
  } else if (probability >= 0.4) {
    return 'text-warning' // Medium risk (yellow/orange)
  } else {
    return 'text-success' // Low risk (green)
  }
}

// Calculate performance percentage based on a weighted average of metrics
export const getModelPerformancePercentage = (model) => {
  // Using a weighted average of F1 score (50%), accuracy (30%), and precision (20%)
  // This gives more importance to F1 score which balances precision and recall
  const weightedScore = (model.f1_score * 0.5 + model.accuracy * 0.3 + model.precision * 0.2) * 100
  return Math.round(weightedScore)
}

// Determine color class based on performance percentage
export const getModelPerformanceColorClass = (percentage) => {
  if (percentage >= 80) return 'bg-success text-white'
  if (percentage >= 60) return 'bg-warning text-white'
  return 'bg-error text-white'
}

// Get performance label based on percentage
export const getModelPerformanceLabel = (percentage) => {
  if (percentage >= 80) return 'Excelente'
  if (percentage >= 60) return 'Bueno'
  if (percentage >= 40) return 'Regular'
  return 'Bajo'
}

export const formatDate = (dateString) => {
  if (!dateString) return 'No disponible'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
