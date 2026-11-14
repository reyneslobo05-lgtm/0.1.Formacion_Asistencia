import csv
from datetime import date

import pytest

from asistencia import lectura
from asistencia.models import Alumno, DatosNoEncontradosError

lista_alumnos = [
    Alumno(
        id=1,
        nombre="Joan",
        apellido="Reyes",
        email="jr@example.com",
        grupo_id=1,
        es_menor=True,
    ),
    Alumno(
        id=2,
        nombre="Mercedes",
        apellido="Reyes",
        email="mr@example.com",
        grupo_id=1,
        es_menor=True,
    ),
    Alumno(
        id=3,
        nombre="Noelia",
        apellido="Reyes",
        email="nr@example.com",
        grupo_id=1,
        es_menor=True,
    ),
    Alumno(
        id=4,
        nombre="Antonio",
        apellido="Reyes",
        email="ar@example.com",
        grupo_id=1,
        es_menor=True,
    ),
]


def test_detectar_ausencia(tmp_path, monkeypatch):
    monkeypatch.setattr("asistencia.lectura.DIR_DATA", tmp_path)

    archivo = tmp_path / "asistencia_2026-10.csv"

    with open(archivo, "w", newline="", encoding="utf-8") as doc:
        writer = csv.DictWriter(
            doc, fieldnames=["id", "grupo_id", "alumno_id", "fecha", "estado"]
        )
        writer.writeheader()
        for _ in range(3):
            writer.writerow(
                {
                    "id": 1,
                    "grupo_id": 1,
                    "alumno_id": 3,
                    "fecha": "2026-10-23",
                    "estado": "ausente",
                }
            )
        for j in range(4):
            writer.writerow(
                {
                    "id": 1,
                    "grupo_id": 1,
                    "alumno_id": j,
                    "fecha": "2026-10-23",
                    "estado": "presente",
                }
            )

    resultado = lectura.detectar_ausencia(
        fecha=date(2026, 10, 30), alumnos=lista_alumnos
    )

    assert resultado == ["nr@example.com"]

    # valida que si el alumno_id que ha faltado no se encuentra en la lista no envia ningún mensaje
    # valida que a un alumno con 2 faltas no se le envia mensaje.


def test_detectar_ausencia_vacia(tmp_path, monkeypatch):
    monkeypatch.setattr("asistencia.lectura.DIR_DATA", tmp_path)

    archivo = tmp_path / "asistencia_2026-10.csv"

    with open(archivo, "w", newline="", encoding="utf-8") as doc:
        writer = csv.DictWriter(
            doc, fieldnames=["id", "grupo_id", "alumno_id", "fecha", "estado"]
        )
        writer.writeheader()

        for _ in range(5):
            writer.writerow(
                {
                    "id": 5,
                    "grupo_id": 1,
                    "alumno_id": 6,
                    "fecha": "2026-10-23",
                    "estado": "ausente",
                }
            )
        for _ in range(2):
            writer.writerow(
                {
                    "id": 2,
                    "grupo_id": 1,
                    "alumno_id": 3,
                    "fecha": "2026-10-23",
                    "estado": "ausente",
                }
            )
        for j in range(4):
            writer.writerow(
                {
                    "id": 1,
                    "grupo_id": 1,
                    "alumno_id": j,
                    "fecha": "2026-10-23",
                    "estado": "presente",
                }
            )

    resultado = lectura.detectar_ausencia(
        fecha=date(2026, 10, 30), alumnos=lista_alumnos
    )

    assert resultado == []


def test_detectar_ausencia_sin_file(tmp_path, monkeypatch):
    monkeypatch.setattr("asistencia.lectura.DIR_DATA", tmp_path)

    with pytest.raises(DatosNoEncontradosError):
        lectura.detectar_ausencia(
            fecha=date(2026, 10, 30), alumnos=lista_alumnos
        )
