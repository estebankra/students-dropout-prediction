// validationSchema.js
import * as yup from 'yup'

const currentYear = new Date().getFullYear()
const minDate = new Date('1950-01-01')
const maxDate = new Date('2010-01-01') // fecha actual

export const formacionOptions = [
  { value: 'Basica', label: 'Básica' },
  { value: 'Media', label: 'Media' },
  { value: 'Universitaria', label: 'Universitaria' },
  { value: 'Superior', label: 'Superior' },
  { value: 'Ninguna', label: 'Ninguna' }
]

export const studentSchema = yup.object().shape({
  archived: yup.bool().default(false).label('Archivado'),

  estado: yup
    .string()
    .required('Campo requerido')
    .default('V')
    .oneOf(['V', 'E', 'A'])
    .label('Estado'),

  first_name: yup
    .string()
    .required('Campo requerido')
    .min(2, 'Debe tener al menos dos caracteres')
    .max(200, 'Debe tener como máximo 200 caracteres')
    .label('Nombre'),

  last_name: yup
    .string()
    .required('Campo requerido')
    .min(2, 'Debe tener al menos dos caracteres')
    .max(200, 'Debe tener como máximo 200 caracteres')
    .label('Apellido'),

  faculty_short_name: yup.string().required('Campo requerido').label('Facultad'),

  estado_civil: yup
    .string()
    .required('Campo requerido')
    .oneOf(['S', 'C', 'D'])
    .label('Estado Civil'),

  fecha_nac: yup
    .date()
    .required('Campo requerido')
    .min(minDate, 'La fecha debe ser posterior a 1950')
    .max(maxDate, 'La fecha debe ser menor a 2010')
    .typeError('Ingrese una fecha válida')
    .label('Fecha de Nacimiento'),

  ultimo_semestre_cursado: yup
    .number()
    .required('Campo requerido')
    .min(1, 'Debe ser mayor o igual a 1 (uno)')
    .integer()
    .default(1)
    .label('Último semestre cursado'),

  nro_hijos: yup
    .number()
    .required('Campo requerido')
    .min(0, 'Debe ser mayor o igual a 0 (cero)')
    .integer()
    .label('Número de hijos'),

  anio_egreso: yup
    .string()
    .required('Campo requerido')
    .matches(/^[0-9]{4}$/, 'Debe ser un año válido')
    .test('valid-year', 'Año inválido', (value) => {
      const year = parseInt(value)
      return year >= 1970 && year <= currentYear
    })
    .label('Año de egreso de secundaria'),

  promedio_secundaria: yup
    .string()
    .required('Campo requerido')
    .oneOf(['4 a 5', '3 a 3,99', '2,5 a 2,99', '2 a 2,49'])
    .label('Promedio en secundaria'),

  cuantos_colegios_secundaria: yup
    .number()
    .required('Campo requerido')
    .min(1, 'Debe ser mayor o igual a 1 (uno)')
    .integer()
    .label('Colegios asistidos'),

  posee_enfermedad: yup
    .string()
    .required('Campo requerido')
    .oneOf(['No', 'Leve', 'Compleja'])
    .label('Posee enfermedad'),

  vive_con: yup
    .string()
    .required('Campo requerido')
    .oneOf(['Familia nuclear', 'Solo', 'Familia extensa', 'Companeros'])
    .label('Vive con'),

  situacion_ocupacional: yup
    .string()
    .required('Campo requerido')
    .oneOf(['Solo Estudio', 'Trab Todo el dia', 'Trab 1/2 dia', 'Trab con cambio de turno'])
    .label('Situación Ocupacional'),

  sustento_economico: yup
    .string()
    .required('Campo requerido')
    .oneOf(['Familia', 'Trabajo', 'Becas', 'Beca parcial'])
    .label('Sustento Económico'),

  formacion_academica_padre: yup
    .string()
    .required('Campo requerido')
    .oneOf(['Basica', 'Media', 'Universitaria', 'Superior', 'Ninguna'])
    .label('Formación del Padre'),

  formacion_academica_madre: yup
    .string()
    .required('Campo requerido')
    .oneOf(['Basica', 'Media', 'Universitaria', 'Superior', 'Ninguna'])
    .label('Formación de la Madre'),

  formacion_academica_hermanos: yup
    .string()
    .required('Campo requerido')
    .oneOf(['Basica', 'Media', 'Universitaria', 'Superior', 'Ninguna'])
    .label('Formación de Hermanos')
})
