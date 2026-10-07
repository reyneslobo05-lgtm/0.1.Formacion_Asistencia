from datetime import date
from typing import Literal

from pydantic import BaseModel, EmailStr


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
    estado: Literal['presente', 'ausente', 'tarde']

class Nodo:
    def ejecutar(self, valores):
        raise NotImplementedError("El método ejecutar debe ser implementado por la subclase.")

