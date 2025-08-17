# Manual de Uso - Supervisor - Sistema de Predicción de Deserción Estudiantil

Este manual proporciona instrucciones detalladas para usar el sistema de predicción de deserción estudiantil con rol de **Supervisor**.

## 📋 Índice

1. [Acceso al Sistema](#acceso-al-sistema)
2. [Panel de Supervisor](#panel-de-supervisor)
3. [Dashboard y Reportes](#dashboard-y-reportes)
4. [Gestión de Estudiantes](#gestión-de-estudiantes)
5. [Cálculo de Predicciones](#cálculo-de-predicciones)
6. [Análisis y Reportes](#análisis-y-reportes)
7. [Exportación de Datos](#exportación-de-datos)
8. [Solución de Problemas](#solución-de-problemas)

---

## 🔐 Acceso al Sistema

### Inicio de Sesión

1. **Acceder a la aplicación** en `http://localhost:4000`
2. **Ingresar credenciales** de supervisor:
   - Email del supervisor
   - Contraseña
3. **Hacer clic en "Iniciar Sesión"**

### Navegación Principal

Una vez autenticado como supervisor, tendrás acceso a:
- **Reportes** (Dashboard) - Vista general y análisis de datos
- **Estudiantes** - Gestión y seguimiento de estudiantes

---

## 👨‍🏫 Panel de Supervisor

### Funciones Principales del Supervisor

El rol de supervisor está diseñado para:
- **Monitorear estudiantes** en riesgo de deserción
- **Generar predicciones** de deserción 
- **Analizar reportes** y distribuciones de riesgo
- **Gestionar información** de estudiantes
- **Exportar datos** para análisis externos
- **Filtrar por facultad** específica

### Selección de Contexto

Antes de usar el sistema, el supervisor debe configurar:

#### 🏛️ **Selección de Facultad**
- **Ubicación**: Esquina superior derecha
- **Funcionalidad**: Filtra todos los datos por facultad específica
- **Opciones**: Lista de facultades activas en el sistema
- **Impacto**: Todos los reportes y listas se filtran automáticamente

#### 🤖 **Versión del Modelo**
- **Selección automática**: El sistema usa el modelo activo
- **Información mostrada**: Versión y métricas del modelo
- **Impacto**: Todas las predicciones usan este modelo

---

## 📊 Dashboard y Reportes

### Pantalla Principal de Reportes

Al acceder al sistema, el supervisor ve el dashboard principal con:

#### 📈 **Distribución de Probabilidad de Deserción**

**Resumen de Riesgo por Categorías**:
- **Alto Riesgo** (70-100%): Estudiantes que requieren intervención inmediata
- **Riesgo Medio** (40-69%): Estudiantes que necesitan seguimiento
- **Bajo Riesgo** (0-39%): Estudiantes con baja probabilidad de deserción

**Información mostrada**:
- **Cantidad absoluta** de estudiantes por categoría
- **Porcentaje** respecto al total
- **Gráfico de distribución** visual por rangos de probabilidad

#### 📊 **Gráfico de Distribución**
- **Barras por rango**: Distribución detallada en rangos de 10%
- **Datos absolutos**: Cantidad de estudiantes por rango
- **Porcentajes**: Proporción relativa de cada rango
- **Visualización interactiva**: Hover para ver detalles

#### 🔍 **Factores de Impacto en la Deserción**
- **Análisis de variables**: Qué factores más influyen en la deserción
- **Importancia relativa**: Peso de cada variable en el modelo
- **Interpretación visual**: Gráficos de importancia de características

### Estudiantes de Alto Riesgo

#### 📋 **Lista de Estudiantes Críticos**
- **Filtro automático**: Estudiantes con riesgo > 70%
- **Información básica**: Nombre, probabilidad, estado
- **Acceso rápido**: "Ver todos" para lista completa
- **Límite**: Muestra los 10 primeros casos críticos

### Estudiantes Sin Predicciones

#### ⚠️ **Estudiantes Pendientes**
- **Identificación**: Estudiantes sin predicción calculada
- **Prioridad**: Necesitan cálculo de riesgo
- **Acción requerida**: Ejecutar predicciones
- **Seguimiento**: Lista de casos pendientes

---

## 👥 Gestión de Estudiantes

### Acceso a la Lista de Estudiantes

1. **Navegar a "Estudiantes"** desde el menú principal
2. **Configurar contexto**:
   - Seleccionar facultad (si aplica)
   - Verificar modelo activo
3. **Ver lista completa** de estudiantes

### Información de Estudiantes

**Datos mostrados en la lista**:
- **Nombre completo** del estudiante
- **Estado académico** (Vigente, Egresado, Abandono)
- **Probabilidad de deserción** (si existe predicción)
- **Categoría de riesgo** (Alto, Medio, Bajo)
- **Facultad** de pertenencia
- **Indicadores visuales** de estado

### Filtros Disponibles

#### 🔍 **Filtro por Búsqueda**
- **Campo de texto**: Buscar por nombre o apellido
- **Búsqueda en tiempo real**: Resultados mientras escribes
- **Sin distinción**: Mayúsculas/minúsculas

#### 📊 **Filtro por Probabilidad de Deserción**
- **Rango personalizable**: Desde % hasta %
- **Casos comunes**:
  - Alto riesgo: 70% - 100%
  - Riesgo medio: 40% - 69%
  - Bajo riesgo: 0% - 39%
- **Filtro dinámico**: Actualización automática

#### 📚 **Filtro por Estado Académico**
- **Vigente**: Estudiantes activos
- **Egresado**: Estudiantes graduados
- **Abandono**: Estudiantes que abandonaron

#### 📁 **Filtro por Estudiantes Archivados**
- **Archivados**: Estudiantes marcados como archivados
- **Uso**: Excluidos de futuros entrenamientos de modelos
- **Checkbox**: Incluir/excluir archivados

### Visualización Detallada de Estudiante

#### 📋 **Ver Información Completa**

**Para acceder**:
1. **Localizar estudiante** en la lista
2. **Hacer clic en "Ver"** o en el nombre del estudiante
3. **Se abre modal** con información detallada

**Información mostrada**:

**Datos Académicos**:
- **Estado actual**: Vigente, Egresado, Abandono
- **Facultad**: Facultad de pertenencia
- **Año de egreso**: Año esperado de graduación
- **Promedio secundaria**: Rendimiento en educación media

**Datos Personales**:
- **Fecha de nacimiento** y edad calculada
- **Estado civil**: Soltero, casado, etc.
- **Número de hijos**: Cantidad de dependientes
- **Con quién vive**: Situación de convivencia

**Datos Socioeconómicos**:
- **Sustento económico**: Fuente de financiamiento
- **Situación ocupacional**: Estado laboral
- **Formación académica de familiares**:
  - Padre
  - Madre  
  - Hermanos

**Datos de Salud**:
- **Posee enfermedad**: Condiciones médicas

**Historial Educativo**:
- **Cantidad de colegios**: Cuántos colegios de secundaria

**Predicción de Deserción**:
- **Probabilidad calculada**: Porcentaje de riesgo
- **Versión del modelo**: Qué modelo generó la predicción
- **Fecha de cálculo**: Cuándo se calculó

### Edición de Información de Estudiante

#### ✏️ **Modo de Edición**

**Para editar**:
1. **Abrir información** del estudiante
2. **Hacer clic en "Editar"**
3. **Modificar campos** necesarios
4. **Guardar cambios**

**Campos editables**:
- **Estado académico**: Cambiar entre Vigente/Egresado/Abandono
- **Todos los datos personales**: Información demográfica
- **Datos socioeconómicos**: Información familiar y económica
- **Estado de archivo**: Marcar/desmarcar como archivado

#### 📁 **Archivar Estudiante**

**Funcionalidad**:
- **Checkbox** "Archivar estudiante"
- **Propósito**: Excluir de futuros entrenamientos de modelos
- **Uso**: Para estudiantes con datos inconsistentes o casos especiales
- **Efecto**: Mantiene histórico pero no influye en nuevos modelos

**Cuándo archivar**:
- Datos incompletos o inconsistentes
- Casos excepcionales que distorsionan el modelo
- Estudiantes transferidos a otras instituciones
- Situaciones especiales que no representan el patrón general

---

## 🔮 Cálculo de Predicciones

### Ejecutar Nuevas Predicciones

#### 🚀 **Proceso de Cálculo**

**Para ejecutar predicciones**:
1. **Hacer clic en "Calcular riesgo de deserción"**
2. **Confirmar acción** en el modal
3. **Esperar procesamiento** (puede tomar varios minutos)
4. **Revisar resultados** una vez completado

**Información del modal de confirmación**:
- **Modelo a usar**: Versión actual del modelo
- **Métricas del modelo**: Rendimiento esperado
- **Cantidad de estudiantes**: Cuántos se procesarán

#### ⏱️ **Tiempo de Procesamiento**

**Factores que afectan el tiempo**:
- **Cantidad de estudiantes**: Más estudiantes = más tiempo
- **Complejidad del modelo**: Tipo de algoritmo usado
- **Recursos del servidor**: Capacidad de procesamiento

**Indicadores de progreso**:
- **Botón deshabilitado**: Durante el procesamiento
- **Spinner de carga**: Indicador visual
- **Mensaje de estado**: "Calculando predicciones..."

### Interpretación de Resultados

#### 📊 **Probabilidades de Deserción**

**Rangos de interpretación**:
- **0-39%**: **Bajo riesgo** - Seguimiento rutinario
- **40-69%**: **Riesgo medio** - Seguimiento reforzado
- **70-100%**: **Alto riesgo** - Intervención inmediata

**Factores a considerar**:
- **Precisión del modelo**: F1 Score mostrado en la confirmación
- **Actualidad de datos**: Qué tan recientes son los datos del estudiante
- **Contexto individual**: Circunstancias específicas del estudiante

---

## 📈 Análisis y Reportes

### Dashboard Analítico

#### 📊 **Distribución por Facultad**

**Visualización disponible**:
- **Gráfico de distribución**: Por facultad seleccionada
- **Comparación entre facultades**: Si no hay filtro aplicado
- **Métricas comparativas**: Rendimiento por facultad

#### 📈 **Tendencias Temporales**

**Análisis disponible**:
- **Evolución del riesgo**: Cambios en el tiempo
- **Comparación de modelos**: Diferentes versiones
- **Impacto de intervenciones**: Efectividad de acciones

### Reportes Especializados

#### 🎯 **Estudiantes en Riesgo Crítico**

**Acceso rápido desde dashboard**:
- **Lista filtrada**: Automáticamente > 70% riesgo
- **Información prioritaria**: Casos que requieren atención inmediata
- **Acciones sugeridas**: Recomendaciones de intervención

#### 📋 **Estudiantes Sin Predicción**

**Identificación de casos pendientes**:
- **Lista de estudiantes**: Sin cálculo de riesgo
- **Priorización**: Casos que necesitan análisis
- **Acción requerida**: Ejecutar predicciones

### Interpretación de Gráficos

#### 📊 **Gráfico de Distribución**

**Elementos del gráfico**:
- **Eje X**: Rangos de probabilidad (0-10%, 11-20%, etc.)
- **Eje Y**: Cantidad de estudiantes
- **Barras**: Distribución por rango
- **Colores**: Código visual por nivel de riesgo

**Interpretación**:
- **Distribución normal**: La mayoría en rangos medios-bajos
- **Concentración alta**: Muchos estudiantes en alto riesgo (preocupante)
- **Concentración baja**: Pocos estudiantes en riesgo (positivo)

#### 📈 **Gráfico de Factores de Impacto**

**Variables analizadas**:
- **Importancia relativa**: Qué factores más influyen
- **Correlaciones**: Relación con la deserción
- **Interpretación**: Cuáles son los predictores más fuertes

---

## 📤 Exportación de Datos

### Formatos Disponibles

El sistema permite exportar datos en tres formatos:

#### 📄 **CSV (Comma-Separated Values)**
- **Uso**: Análisis en Excel, R, Python
- **Ventajas**: Universal, liviano
- **Contenido**: Datos tabulares completos

#### 📊 **Excel (XLSX)**
- **Uso**: Análisis avanzado en Excel
- **Ventajas**: Formateo, fórmulas, gráficos
- **Contenido**: Hojas múltiples con datos estructurados

#### 📋 **PDF (Portable Document Format)**
- **Uso**: Reportes formales, presentaciones
- **Ventajas**: Formato fijo, profesional
- **Contenido**: Reporte estructurado con gráficos

### Proceso de Exportación

#### 📥 **Pasos para Exportar**

1. **Aplicar filtros** deseados en la lista de estudiantes
2. **Hacer clic en "Exportar"**
3. **Seleccionar formato**:
   - CSV para análisis de datos
   - Excel para reportes detallados
   - PDF para presentaciones formales
4. **Esperar generación** del archivo
5. **Descargar archivo** automáticamente

#### 🎯 **Contenido Exportado**

**Datos incluidos**:
- **Información personal**: Nombre, edad, estado civil
- **Datos académicos**: Facultad, estado, promedio
- **Datos socioeconómicos**: Situación económica, familiar
- **Predicciones**: Probabilidad de deserción, modelo usado
- **Metadatos**: Fecha de exportación, filtros aplicados

**Respeta filtros aplicados**:
- **Facultad seleccionada**: Solo estudiantes de esa facultad
- **Filtros de búsqueda**: Nombres, estados, rangos de riesgo
- **Filtros de probabilidad**: Solo estudiantes en el rango especificado

### Casos de Uso de Exportación

#### 📊 **Análisis Estadístico**
- **Formato recomendado**: CSV
- **Uso**: Análisis en software estadístico
- **Beneficio**: Datos limpios para procesamiento

#### 📈 **Reportes Ejecutivos**
- **Formato recomendado**: PDF
- **Uso**: Presentaciones a directivos
- **Beneficio**: Formato profesional y fijo

#### 📋 **Trabajo Colaborativo**
- **Formato recomendado**: Excel
- **Uso**: Análisis en equipo
- **Beneficio**: Herramientas de análisis integradas

---

## 🔧 Solución de Problemas

### Problemas Comunes y Soluciones

#### No aparecen estudiantes en la lista
**Posibles causas**:
- Filtros muy restrictivos
- Facultad sin estudiantes
- Problema de conectividad

**Soluciones**:
1. **Revisar filtros** aplicados
2. **Cambiar facultad** o seleccionar "Todas"
3. **Refrescar página** si hay problemas de conexión
4. **Verificar permisos** de acceso

#### Las predicciones no se calculan
**Posibles causas**:
- Modelo no disponible
- Datos insuficientes
- Proceso ya en ejecución

**Soluciones**:
1. **Verificar modelo activo** en la configuración
2. **Esperar** si hay otro cálculo en progreso
3. **Revisar que hay estudiantes** para procesar
4. **Contactar administrador** si persiste el problema

#### Los filtros no funcionan correctamente
**Posibles causas**:
- Datos no sincronizados
- Error en rangos de valores
- Problema temporal del sistema

**Soluciones**:
1. **Refrescar la página**
2. **Verificar rangos** de probabilidad (0-100)
3. **Limpiar filtros** y aplicar nuevamente
4. **Verificar conexión** a internet

#### La exportación falla
**Posibles causas**:
- Demasiados datos para exportar
- Problema del servidor
- Formato no compatible

**Soluciones**:
1. **Aplicar filtros** para reducir cantidad de datos
2. **Intentar formato diferente** (CSV en lugar de PDF)
3. **Esperar unos minutos** y reintentar
4. **Verificar espacio** en disco local

#### No se puede editar información de estudiante
**Posibles causas**:
- Permisos insuficientes
- Estudiante bloqueado por sistema
- Datos requeridos faltantes

**Soluciones**:
1. **Verificar permisos** de supervisor
2. **Completar campos requeridos**
3. **Revisar formato** de datos ingresados
4. **Contactar administrador** para verificar permisos

### Mejores Prácticas

#### 📊 **Gestión de Datos**

1. **Actualización regular**:
   - Revisar información de estudiantes periódicamente
   - Actualizar estados académicos
   - Archivar casos especiales

2. **Uso de filtros**:
   - Comenzar con filtros amplios
   - Refinar gradualmente
   - Documentar criterios utilizados

3. **Interpretación de predicciones**:
   - Considerar contexto individual
   - No usar como única herramienta de decisión
   - Combinar con evaluación personal

#### 🎯 **Seguimiento de Estudiantes**

1. **Priorización**:
   - **Alto riesgo**: Revisión semanal
   - **Riesgo medio**: Revisión quincenal
   - **Bajo riesgo**: Revisión mensual

2. **Documentación**:
   - Registrar intervenciones realizadas
   - Documentar cambios en situación del estudiante
   - Mantener historial de contactos

3. **Coordinación**:
   - Comunicar casos críticos al equipo
   - Coordinar con servicios de apoyo
   - Seguir protocolos institucionales

### Mantenimiento del Sistema

#### 📅 **Tareas Regulares**

**Diarias**:
- Revisar estudiantes de alto riesgo
- Verificar nuevas alertas
- Actualizar casos críticos

**Semanales**:
- Ejecutar nuevas predicciones si hay datos nuevos
- Revisar tendencias en dashboard
- Actualizar información de estudiantes modificada

**Mensuales**:
- Exportar reportes para análisis
- Revisar efectividad de intervenciones
- Coordinar con administradores sobre mejoras

#### 🔍 **Monitoreo de Calidad**

1. **Verificar coherencia** de predicciones
2. **Reportar anomalías** al administrador
3. **Sugerir mejoras** en base a experiencia de uso
4. **Documentar casos** que requieren atención especial

### Contacto y Soporte

#### 📞 **Escalación de Problemas**

**Problemas técnicos**:
1. **Reintentar** la operación
2. **Refrescar** la página
3. **Verificar conexión** a internet
4. **Contactar administrador** con detalles del error

**Problemas de interpretación**:
1. **Consultar** este manual
2. **Revisar contexto** del estudiante
3. **Coordinar** con equipo académico
4. **Solicitar capacitación** adicional si es necesario

---

## 📝 Notas Importantes

### Consideraciones Éticas

#### 🔒 **Privacidad de Datos**
- **Confidencialidad**: Información sensible de estudiantes
- **Acceso limitado**: Solo personal autorizado
- **Uso responsable**: Fines educativos únicamente

#### ⚖️ **Uso de Predicciones**
- **Herramienta de apoyo**: No reemplazan criterio humano
- **Contexto individual**: Considerar circunstancias específicas
- **Decisiones informadas**: Combinar datos con evaluación personal

### Limitaciones del Sistema

#### 🤖 **Modelos Predictivos**
- **Probabilidades**: No predicciones absolutas
- **Basado en datos históricos**: Puede no reflejar situaciones nuevas
- **Requiere actualización**: Regular reentrenamiento de modelos

#### 📊 **Datos**
- **Calidad depende** de información ingresada
- **Completitud**: Predicciones mejores con datos completos
- **Actualidad**: Información desactualizada reduce precisión
