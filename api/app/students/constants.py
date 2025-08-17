from enum import Enum


class EstadoEnum(str, Enum):
    EGRESADO = "E"
    ABANDONO = "A"
    VIGENTE = "V"


class EstadoCivilEnum(str, Enum):
    SOLTERO = "S"
    CASADO = "C"
    DIVORCIADO = "D"


class PromedioEnum(str, Enum):
    RANGO_4_5 = "4 a 5"
    RANGO_3_399 = "3 a 3,99"
    RANGO_25_299 = "2,5 a 2,99"
    RANGO_2_249 = "2 a 2,49"


class EnfermedadEnum(str, Enum):
    NO = "No"
    LEVE = "Leve"
    COMPLEJA = "Compleja"


class ViveConEnum(str, Enum):
    SOLO = "Solo"
    FAMILIA_NUCLEAR = "Familia nuclear"
    FAMILIA_EXTENSA = "Familia extensa"
    COMPANEROS = "Companeros"


class SituacionOcupacionalEnum(str, Enum):
    SOLO_ESTUDIO = "Solo Estudio"
    TRABAJO_COMPLETO = "Trab Todo el dia"
    TRABAJO_MEDIO = "Trab 1/2 dia"
    TRABAJO_TURNOS = "Trab con cambio de turno"


class SustentoEconomicoEnum(str, Enum):
    FAMILIA = "Familia"
    TRABAJO = "Trabajo"
    BECAS = "Becas"
    BECA_PARCIAL = "Beca parcial"


class FormacionEnum(str, Enum):
    BASICA = "Basica"
    MEDIA = "Media"
    UNIVERSITARIA = "Universitaria"
    SUPERIOR = "Superior"
    NINGUNA = "Ninguna"
