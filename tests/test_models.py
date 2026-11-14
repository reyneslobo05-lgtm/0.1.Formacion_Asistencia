import pytest
from asistencia.models import Alumno, Contexto, RegistroAsistencia
from pydantic import ValidationError


def test_alumno():
    with pytest.raises(ValidationError):
        alumno1 = Alumno(
            id="hola",
            nombre="Juan",
            apellido="Pérez",
            grupo_id=1,
            email="juan@ejemplo.com",
        )
    with pytest.raises(ValidationError):
        alumno2 = Alumno(
            id=456,
            nombre="María",
            apellido="Gómez",
            grupo_id=2,
            email="correo_invalido",
        )


def test_RegistroAsistencia():
    with pytest.raises(ValidationError):
        registro1 = RegistroAsistencia(
            id=1, grupo_id=1, alumno_id=1, fecha="2024", estado="presente"
        )
    with pytest.raises(ValidationError):
        registro2 = RegistroAsistencia(
            id=2, grupo_id=2, alumno_id=2, fecha="2024-06-02", estado="invalido"
        )


def test_Contexto():
    with pytest.raises(ValidationError):
        contexto1 = Contexto(
            fecha="06",
            alumnos=[],
            grupos=[],
            registros_asistencia=[],
            contador=1,
            alumnos_ausentes=[],
        )
