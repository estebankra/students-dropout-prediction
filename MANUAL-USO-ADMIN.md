# Manual de Uso - Administrador - Sistema de Predicción de Deserción Estudiantil

Este manual proporciona instrucciones detalladas para usar el sistema de predicción de deserción estudiantil según el rol de usuario Administrador.

## 📋 Índice

1. [Acceso al Sistema](#acceso-al-sistema)
2. [Panel de Administrador](#panel-de-administrador)
3. [Gestión de Usuarios](#gestión-de-usuarios)
4. [Gestión de Facultades](#gestión-de-facultades)
5. [Gestión de Modelos](#gestión-de-modelos)
6. [Dashboard y Métricas](#dashboard-y-métricas)
7. [Solución de Problemas](#solución-de-problemas)

---

## 🔐 Acceso al Sistema

### Inicio de Sesión

1. **Acceder a la aplicación** en `http://localhost:4000`
2. **Ingresar credenciales** de administrador:
   - Email del administrador
   - Contraseña
3. **Hacer clic en "Iniciar Sesión"**

### Navegación Principal

Una vez autenticado como administrador, tendrás acceso a:
- **Dashboard** - Vista general del sistema
- **Usuarios** - Gestión de usuarios del sistema
- **Facultades** - Gestión de facultades universitarias
- **Modelos** - Gestión y entrenamiento de modelos predictivos

---

## 👨‍💼 Panel de Administrador

### Dashboard Principal

El dashboard proporciona una vista general del estado del sistema:

#### 🏥 **Estado del Sistema**
- **Salud del Sistema**: Indicadores de funcionamiento
- **Conectividad de la API**: Estado de conexión
- **Estado de la Base de Datos**: Verificación de conectividad

#### 👥 **Estadísticas de Usuarios**
- **Total de usuarios** registrados en el sistema
- **Usuarios activos** vs inactivos
- **Distribución por roles** (Administradores, Supervisores)

#### 🤖 **Estado del Modelo Actual**
- **Versión del modelo** activo
- **Fecha de entrenamiento**
- **Rendimiento del modelo** (F1 Score)
- **Cantidad de datos** utilizados para entrenar

#### 📊 **Comparación de Modelos**
- **Gráfico comparativo** de rendimiento entre modelos
- **Métricas de precisión** (Accuracy, Precision, Recall, F1 Score)
- **Evolución temporal** del rendimiento

#### 📋 **Últimos Modelos**
- **Lista de modelos recientes** entrenados
- **Estado de cada modelo** (Activo, Entrenando, Completado)
- **Acceso rápido** para activar modelos

---

## 👥 Gestión de Usuarios

### Visualizar Usuarios

1. **Navegar a "Usuarios"** desde el menú principal
2. **Ver lista completa** de usuarios del sistema
3. **Información mostrada**:
   - Nombre completo
   - Email
   - Rol (Administrador/Supervisor)
   - Estado (Activo/Inactivo)
   - Fecha de creación

### Filtrar Usuarios

**Opciones de filtrado disponibles**:
- **Por rol**: Administrador, Supervisor
- **Por estado**: Activo, Inactivo
- **Por texto**: Búsqueda por nombre o email

**Pasos para filtrar**:
1. **Hacer clic en el botón de filtros**
2. **Seleccionar criterios** deseados
3. **Aplicar filtros** para actualizar la lista

### Crear Nuevo Usuario

1. **Hacer clic en "Nuevo usuario"**
2. **Completar el formulario**:
   - **Nombre**: Mínimo 2 caracteres, máximo 200
   - **Apellido**: Mínimo 2 caracteres, máximo 200
   - **Correo**: Debe ser un email válido
   - **Rol**: Seleccionar entre Administrador o Supervisor
   - **Contraseña**: Mínimo 8 caracteres, máximo 128
   - **Confirmar contraseña**: Debe coincidir con la contraseña
3. **Hacer clic en "Crear"**

### Editar Usuario Existente

1. **Localizar al usuario** en la lista
2. **Hacer clic en el botón de editar** (ícono de lápiz)
3. **Modificar los datos** necesarios:
   - Todos los campos son editables
   - **Estado**: Puede cambiar entre Activo/Inactivo
   - **Contraseña**: Opcional - dejar vacío para mantener la actual
4. **Hacer clic en "Actualizar"**

### Gestión de Estados

**Estados disponibles**:
- **Activo**: Usuario puede acceder al sistema
- **Inactivo**: Usuario bloqueado, sin acceso al sistema

**Para cambiar estado**:
1. **Editar el usuario**
2. **Cambiar el campo "Estado"**
3. **Guardar cambios**

---

## 🏛️ Gestión de Facultades

### Visualizar Facultades

1. **Navegar a "Facultades"** desde el menú principal
2. **Ver lista completa** de facultades
3. **Información mostrada**:
   - Nombre de la facultad
   - Descripción
   - Estado (Activa/Inactiva)
   - Fecha de creación

### Filtrar Facultades

**Opciones de filtrado**:
- **Por estado**: Activa, Inactiva
- **Por texto**: Búsqueda por nombre

**Aplicar filtros**:
1. **Usar la barra de filtros**
2. **Seleccionar criterios**
3. **Ver resultados filtrados**

### Crear Nueva Facultad

1. **Hacer clic en "Nueva facultad"**
2. **Completar información**:
   - **Nombre**: Nombre oficial de la facultad
   - **Descripción**: Descripción detallada (opcional)
   - **Estado**: Activa por defecto
3. **Guardar facultad**

### Editar Facultad

1. **Localizar facultad** en la lista
2. **Hacer clic en editar**
3. **Modificar información**:
   - Cambiar nombre
   - Actualizar descripción
   - Cambiar estado (Activa/Inactiva)
4. **Guardar cambios**

### Estados de Facultades

- **Activa**: Disponible para asignar a estudiantes
- **Inactiva**: No disponible para nuevos estudiantes

---

## 🤖 Gestión de Modelos

### Visualizar Modelos

1. **Navegar a "Modelos"** desde el menú principal
2. **Ver lista de todos los modelos** entrenados
3. **Información de cada modelo**:
   - **Versión**: Número de versión del modelo
   - **Cantidad de datos**: Número de registros utilizados
   - **Características**: Número de features del modelo
   - **Métricas de rendimiento**:
     - Accuracy (Precisión)
     - Precision (Precisión positiva)
     - Recall (Sensibilidad)
     - F1 Score (Medida F1)
   - **Fecha de entrenamiento**
   - **Estado**: Activo, Entrenando, Completado

### Ordenar y Filtrar Modelos

**Opciones de ordenamiento**:
- **Por versión** (ascendente/descendente)
- **Por cantidad de datos**
- **Por cantidad de características**
- **Por métricas** (Accuracy, Precision, Recall, F1 Score)
- **Por fecha de entrenamiento**

**Para ordenar**:
1. **Seleccionar criterio** en "Ordenar por"
2. **Elegir orden** (Ascendente/Descendente)
3. **La lista se actualiza** automáticamente

### Entrenar Nuevo Modelo

⚠️ **Importante**: El entrenamiento de modelos es un proceso que puede tomar varios minutos.

1. **Hacer clic en "Entrenar nuevo modelo"**
2. **Confirmar la acción** en el modal que aparece
3. **Esperar a que complete** el entrenamiento
   - Se mostrará un indicador de progreso
   - El botón estará deshabilitado durante el proceso
4. **El nuevo modelo aparecerá** en la lista una vez completado

### Activar Modelo

1. **Localizar el modelo** deseado en la lista
2. **Hacer clic en "Activar"** (si no está activo)
3. **Confirmar la activación**
4. **El modelo se convierte** en el modelo activo para predicciones

### Comparar Rendimiento de Modelos

1. **Expandir la sección** "Comparar el rendimiento de los modelos"
2. **Ver gráfico comparativo** con:
   - Líneas de tendencia para cada métrica
   - Comparación entre versiones
   - Evolución del rendimiento
3. **Analizar métricas**:
   - **Accuracy**: % de predicciones correctas
   - **Precision**: % de predicciones positivas correctas
   - **Recall**: % de casos positivos identificados
   - **F1 Score**: Media armónica entre Precision y Recall

### Interpretación de Métricas

**Accuracy (Precisión General)**:
- Porcentaje de predicciones correctas
- Rango: 0-100%
- Mayor es mejor

**Precision (Precisión Positiva)**:
- De los estudiantes predichos como "en riesgo", qué porcentaje realmente lo está
- Importante para evitar falsas alarmas

**Recall (Sensibilidad)**:
- De los estudiantes realmente en riesgo, qué porcentaje fue identificado
- Importante para no perder casos de riesgo

**F1 Score**:
- Balance entre Precision y Recall
- Métrica más confiable para modelos con clases desbalanceadas

---

## 📊 Dashboard y Métricas

### Interpretar el Dashboard

#### Estado del Sistema
- **Verde**: Sistema funcionando correctamente
- **Amarillo**: Advertencias menores
- **Rojo**: Problemas críticos que requieren atención

#### Métricas de Usuarios
- **Total**: Cantidad absoluta de usuarios
- **Activos**: Usuarios que pueden acceder
- **Por rol**: Distribución entre administradores y supervisores

#### Rendimiento del Modelo
- **Versión actual**: Modelo en uso para predicciones
- **F1 Score**: Métrica principal de rendimiento
- **Fecha de entrenamiento**: Antigüedad del modelo

### Monitoreo del Sistema

**Indicadores a vigilar**:
1. **Estado de la API**: Debe estar "Conectado"
2. **Base de datos**: Debe estar "Operativa"
3. **Rendimiento del modelo**: F1 Score > 70% recomendado
4. **Antigüedad del modelo**: Reentrenar si es muy antiguo

**Acciones recomendadas**:
- **Reentrenar modelo** si el rendimiento baja
- **Verificar conectividad** si hay problemas de API
- **Revisar logs** si hay errores del sistema

---

## 🔧 Solución de Problemas

### Problemas Comunes y Soluciones

#### No se pueden crear usuarios
**Posibles causas**:
- Email ya registrado
- Contraseña no cumple requisitos
- Problema de conectividad

**Soluciones**:
1. **Verificar que el email** no esté en uso
2. **Usar contraseña** de 8-128 caracteres
3. **Revisar conexión** a la API

#### El entrenamiento de modelos falla
**Posibles causas**:
- Datos insuficientes
- Problema con el servidor
- Otro entrenamiento en progreso

**Soluciones**:
1. **Esperar** si hay otro entrenamiento activo
2. **Verificar que hay datos** suficientes en el sistema
3. **Revisar logs** del servidor
4. **Intentar nuevamente** después de unos minutos

#### Modelos no se activan
**Posibles causas**:
- Modelo aún entrenando
- Error en el modelo
- Problema de permisos

**Soluciones**:
1. **Esperar** a que termine el entrenamiento
2. **Verificar estado** del modelo
3. **Revisar permisos** de administrador

#### Dashboard no carga métricas
**Posibles causas**:
- Problema de conectividad
- Error en la API
- Base de datos no disponible

**Soluciones**:
1. **Refrescar la página**
2. **Verificar conexión** a internet
3. **Revistar estado** de la API y base de datos

### Mantenimiento Recomendado

#### Tareas Diarias
- **Revisar dashboard** para verificar estado del sistema
- **Monitorear usuarios activos**
- **Verificar rendimiento** del modelo actual

#### Tareas Semanales
- **Revisar métricas** de modelos
- **Analizar usuarios** nuevos y cambios de estado
- **Verificar facultades** activas

#### Tareas Mensuales
- **Evaluar reentrenamiento** de modelos
- **Revisar y actualizar** datos de facultades
- **Auditoría de usuarios** y permisos

### Contacto de Soporte

En caso de problemas técnicos que no puedan resolverse:
1. **Documentar el error** con capturas de pantalla
2. **Anotar pasos** para reproducir el problema
3. **Revisar logs** del sistema si es posible

---

## 📝 Notas Importantes

### Mejores Prácticas

1. **Seguridad**:
   - Usar contraseñas seguras
   - No compartir credenciales
   - Desactivar usuarios que ya no necesitan acceso

2. **Gestión de Modelos**:
   - Entrenar nuevos modelos regularmente
   - Comparar rendimiento antes de activar
   - Mantener historial de versiones

3. **Gestión de Datos**:
   - Mantener facultades actualizadas
   - Revisar usuarios periódicamente
   - Asegurar calidad de datos para entrenamiento
