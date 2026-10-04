from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Literal, Optional

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

class RegistroAsistencia(BaseModel):
    id: int
    grupo_id: int
    alumno_id: int
    fecha: date
    estado: Literal['presente', 'ausente', 'tarde']


