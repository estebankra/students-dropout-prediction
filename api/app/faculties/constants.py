from enum import Enum

FACULTIES = [
    {
        "long_name": "Facultad de Ciencias y Tecnologías Innovadoras",
        "short_name": "FCTI",
    },
    {
        "long_name": "Facultad de Ciencias Químicas y Farmacología",
        "short_name": "FCQF",
    },
    {
        "long_name": "Facultad de Ciencias del Derecho y Humanidades",
        "short_name": "FCDH",
    },
    {
        "long_name": "Facultad de Gestión Empresarial y Administración",
        "short_name": "FGEA",
    },
    {
        "long_name": "Facultad de Ciencias Agropecuarias y Veterinarias",
        "short_name": "FCAV",
    },
    {
        "long_name": "Facultad de Ciencias de la Salud",
        "short_name": "FCS",
    },
]


class FacultiesOptions(Enum):
    FCTI = "FCTI"
    FCQF = "FCQF"
    FCDH = "FCDH"
    FGEA = "FGEA"
    FCAV = "FCAV"
    FCS = "FCS"
