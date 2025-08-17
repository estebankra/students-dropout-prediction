# Sistema de Predicción de Deserción Estudiantil

Un sistema de machine learning para predecir y prevenir la deserción estudiantil universitaria, diseñado para ayudar a las instituciones educativas a identificar estudiantes en riesgo y tomar medidas preventivas oportunas.

## 🎯 Descripción del Proyecto

Este sistema utiliza técnicas de aprendizaje automático para analizar datos socioeconómicos, académicos y demográficos de estudiantes universitarios, generando predicciones sobre el riesgo de deserción. La solución incluye una API, una interfaz web y herramientas completas de análisis y reportes.

### Características Principales

- **🤖 Modelos de ML**: Algoritmos de clasificación entrenados (Decision Tree, Logistic Regression, Naive Bayes, Neural Networks)
- **📊 Dashboard Analítico**: Visualizaciones interactivas y reportes detallados
- **👥 Gestión de Roles**: Administradores y Supervisores con funcionalidades específicas
- **📈 Predicciones en Tiempo Real**: Cálculo dinámico de probabilidades de deserción
- **📤 Exportación de Datos**: Reportes en CSV, Excel y PDF
- **🏛️ Gestión por Facultades**: Análisis segmentado por unidades académicas
- **🔐 Autenticación Segura**: Sistema de login con roles diferenciados

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Data Science  │
│   (Vue.js)      │◄──►│   (FastAPI)     │◄──►│   (Jupyter)     │
│                 │    │                 │    │                 │
│ • Dashboard     │    │ • REST API      │    │ • Data Process  │
│ • User Mgmt     │    │ • Authentication│    │ • Model Training│
│ • Reports       │    │ • ML Integration│    │ • Model Export  │
│ • Data Export   │    │ • Database      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   Database      │
                       └─────────────────┘
```

## Documentación
- 📖 [Manual de Instalación](MANUAL-INSTALACION.md)
- 👨‍💼 [Manual de uso Administrador](MANUAL-USO.md)
- 👨‍🏫 [Manual de uso Supervisor](MANUAL-USO-SUPERVISOR.md)
