# Manual de Instalación - Sistema de Predicción de Deserción Estudiantil

Este manual proporciona instrucciones completas para instalar y configurar todo el sistema de predicción de deserción estudiantil, incluyendo el procesamiento de datos, la API backend y la aplicación cliente frontend.

## 📋 Índice

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Configuración del Entorno de Datos (Notebook)](#configuración-del-entorno-de-datos-notebook)
3. [Configuración de la API Backend](#configuración-de-la-api-backend)
4. [Configuración del Cliente Frontend](#configuración-del-cliente-frontend)
5. [Ejecución Completa del Sistema](#ejecución-completa-del-sistema)
6. [Verificación de la Instalación](#verificación-de-la-instalación)

## 🔧 Requisitos del Sistema

### Software Base Requerido

- **Python 3.10** (para API y procesamiento de datos)
- **Node.js 21** (para cliente frontend)
- **PostgreSQL** (base de datos)
- **Git** (control de versiones)

### Herramientas Adicionales

- **nvm** (Node Version Manager)
- **pnpm** (Package Manager para Node.js)
- **Jupyter Lab/Notebook** (para procesamiento de datos)

---

## 📊 Configuración del Entorno de Datos (Notebook)

### 1. Navegar al Directorio

```bash
cd notebook/
```

### 2. Crear Entorno Virtual de Python

```bash
python3 -m venv venv
```

### 3. Activar Entorno Virtual

```bash
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Preparar Datos

Asegúrate de tener el archivo `datos.xlsx` en el directorio `notebook/` con las siguientes columnas:

- `estado` (estado del estudiante: A=Abandonado, V=Activo, E=Graduado)
- `facultad` (facultad)
- `fecha_nac` (fecha de nacimiento)
- `estado_civil` (estado civil)
- `nro_hijos` (número de hijos)
- `anio_egreso` (año de egreso)
- `cuantos_colegios_secundaria` (cantidad de colegios de secundaria)
- `sustento_economico` (sustento económico)
- `promedio_secundaria` (promedio de secundaria)
- `vive_con` (con quién vive)
- `formacion_academica_padre` (formación académica del padre)
- `formacion_academica_madre` (formación académica de la madre)
- `formacion_academica_hermanos` (formación académica de hermanos)
- `situacion_ocupacional` (situación ocupacional)
- `posee_enfermedad` (posee enfermedad)

### 6. Ejecutar Procesamiento de Datos

```bash
# Iniciar Jupyter Lab
jupyter lab

# O alternativamente Jupyter Notebook
jupyter notebook
```

1. Abrir `process_data.ipynb` en Jupyter
2. Ejecutar todas las celdas secuencialmente
3. Verificar que se generen los archivos:
   - `model.pkl` (modelo entrenado)
   - `model_columns.pkl` (nombres de columnas)

---

## 🚀 Configuración de la API Backend

### 1. Navegar al Directorio

```bash
cd ../api/
```

### 2. Crear Entorno Virtual de Python

```bash
python3 -m venv venv
```

### 3. Activar Entorno Virtual

```bash
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Instalar PostgreSQL

Seguir la guía de instalación:
[Instalación PostgreSQL Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-22-04-quickstart)

### 6. Configurar Variables de Entorno

Crear archivo `.env` en el directorio `api/`:

```bash
# Generar SECRET_KEY
openssl rand -hex 32
```

Agregar las variables necesarias al archivo `.env` (ajustar según tu configuración):

```env
SECRET_KEY=tu_secret_key_generado
DATABASE_URL=postgresql://usuario:contraseña@localhost/nombre_base_datos
ENVIRONMENT=development
```

### 7. Configurar Base de Datos

```bash
# Ejecutar migraciones
alembic upgrade head
```

### 8. Copiar Modelos Entrenados

Copiar los archivos generados en el notebook al directorio de la API:

```bash
cp ../notebook/model.pkl ./
cp ../notebook/model_columns.pkl ./
```

### 9. Ejecutar la API

```bash
ENVIRONMENT=development uvicorn app.main:app --reload --timeout-keep-alive 30
```

La API estará disponible en: `http://localhost:8000`

---

## 🎨 Configuración del Cliente Frontend

### 1. Navegar al Directorio

```bash
cd ../client/
```

### 2. Instalar Node Version Manager (nvm)

Si no tienes nvm instalado:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
```

### 3. Instalar Node.js

```bash
nvm install 21
nvm use 21
```

### 4. Instalar pnpm

```bash
npm install -g pnpm
```

### 5. Instalar Dependencias

```bash
pnpm install
```

### 6. Configuración de VS Code (Opcional)

Si usas VS Code, instalar las siguientes extensiones:

- **Vue.volar**
- **dbaeumer.vscode-eslint**
- **esbenp.prettier-vscode**

Configuraciones recomendadas en `settings.json`:

```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit"
  },
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

### 7. Ejecutar en Modo Desarrollo

```bash
pnpm dev
```

La aplicación estará disponible en: `http://localhost:5173` (o el puerto que indique Vite)

---

## 🔄 Ejecución Completa del Sistema

### Orden de Ejecución

1. **Procesamiento de Datos** (una vez, para generar modelos):
   ```bash
   cd notebook/
   source venv/bin/activate
   jupyter lab
   # Ejecutar process_data.ipynb
   ```

2. **API Backend**:
   ```bash
   cd api/
   source venv/bin/activate
   ENVIRONMENT=development uvicorn app.main:app --reload --timeout-keep-alive 30
   ```

3. **Cliente Frontend**:
   ```bash
   cd client/
   pnpm dev
   ```

### URLs del Sistema

- **Frontend**: `http://localhost:5173`
- **API Backend**: `http://localhost:8000`
- **Documentación API**: `http://localhost:8000/docs`
- **Jupyter Lab**: `http://localhost:8888`

---

## ✅ Verificación de la Instalación

### 1. Verificar Notebook

- [ ] Jupyter Lab se ejecuta correctamente
- [ ] El notebook `process_data.ipynb` ejecuta sin errores
- [ ] Se generan los archivos `model.pkl` y `model_columns.pkl`

### 2. Verificar API

- [ ] La API inicia sin errores
- [ ] Acceso a `http://localhost:8000/docs` muestra la documentación
- [ ] Base de datos PostgreSQL conectada correctamente
- [ ] Migraciones aplicadas exitosamente

### 3. Verificar Frontend

- [ ] La aplicación Vue 3 se ejecuta correctamente
- [ ] No hay errores en la consola del navegador
- [ ] La interfaz carga correctamente en `http://localhost:5173`

### 4. Verificar Integración

- [ ] El frontend puede comunicarse con la API
- [ ] Las predicciones funcionan correctamente
- [ ] Los datos se procesan y almacenan adecuadamente

---

## 🛠️ Comandos Útiles de Desarrollo

### API Backend

```bash
# Ejecutar tests
pytest

# Crear nueva migración
alembic revision --autogenerate -m "descripcion_cambio"

# Aplicar migraciones
alembic upgrade head

# Lint del código
./lint.sh
```

### Cliente Frontend

```bash
# Construir para producción
pnpm build

# Ejecutar tests unitarios
pnpm test:unit

# Lint del código
pnpm lint

# Vista previa de build de producción
pnpm preview
```

---

## 🔧 Solución de Problemas Comunes

### Problemas de Python/API

- **Error de versión Python**: Asegurar que se usa Python 3.10
- **Error de base de datos**: Verificar que PostgreSQL esté ejecutándose
- **Error de migraciones**: Ejecutar `alembic upgrade head`

### Problemas de Node.js/Frontend

- **Error de versión Node**: Usar `nvm use 21`
- **Error de dependencias**: Ejecutar `pnpm install` nuevamente
- **Error de puerto**: Verificar que el puerto 5173 esté disponible

### Problemas de Jupyter

- **Kernel no encontrado**: Reinstalar jupyter en el entorno virtual
- **Error de datos**: Verificar que `datos.xlsx` esté en el directorio correcto

---

## 📚 Recursos Adicionales

- **Vue 3**: [Documentación oficial](https://vuejs.org/)
- **Vite**: [Configuración](https://vitejs.dev/config/)
- **FastAPI**: [Documentación](https://fastapi.tiangolo.com/)
- **Pinia**: [State Management](https://pinia.vuejs.org/)
- **Vue Router**: [Routing](https://router.vuejs.org/)
- **Alembic**: [Migraciones](https://alembic.sqlalchemy.org/)

---

## 📞 Soporte

Para problemas o preguntas adicionales, consultar la documentación específica en cada directorio:

- `notebook/README.md` - Procesamiento de datos y modelos
- `api/README.md` - Configuración de la API
- `client/README.md` - Configuración del frontend