from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Alumno(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    es_menor: bool = True
    grupo_id: int


class Grupo(BaseModel):
    id: int
    nombre: str
    dias_semana: list[int]  # 0: lunes, 1: martes, 2: miércoles, 3: jueves, 4: viernes


class RegistroAsistencia(BaseModel):
    id: int
    grupo_id: int
    alumno_id: int
    fecha: date
    estado: Literal["presente", "ausente", "tarde"]


class Contexto(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    fecha: date
    alumnos: list[Alumno] = Field(default_factory=list)
    grupos: list[Grupo] = Field(default_factory=list)
    grupos_hoy: list[Grupo] = Field(default_factory=list)
    registros_asistencia: list[RegistroAsistencia] = Field(default_factory=list)
    alertas: list[str] = Field(default_factory=list)
    contador: int = 0
    alumnos_ausentes: list[str] = Field(default_factory=list)


class AsistenciaError(Exception):
    def __init__(self, value="Ha habido un error generando la asistencia"):
        super().__init__(value)


class VariablesError(AsistenciaError):
    def __init__(self, value="No se han cargado las variables de entorno"):
        super().__init__(value)


class DatosNoEncontradosError(AsistenciaError):
    def __init__(self, value="Ha habido un error buscando los datos"):
        super().__init__(value)


class DatosVaciosError(AsistenciaError):
    def __init__(self, value="El documento de datos está vacío"):
        super().__init__(value)


class EscrituraError(AsistenciaError):
    def __init__(self, value="Ha habido un error escribiendo los datos"):
        super().__init__(value)


class NotificacionError(AsistenciaError):
    def __init__(self, value="Ha habido un error notificando las ausencias"):
        super().__init__(value)
