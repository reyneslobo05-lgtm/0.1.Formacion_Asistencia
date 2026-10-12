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
