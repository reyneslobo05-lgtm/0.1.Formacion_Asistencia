import csv
from datetime import date
from pathlib import Path

from pydantic import ValidationError

from asistencia.models import Alumno, Grupo

DIR_DATA = Path(__file__).parent.parent.parent / "data"
RUTA_ALU = DIR_DATA / "alumnos.csv"


def leer_alumnos(ruta=RUTA_ALU):
    lista_alumnos = []
    with open(ruta, mode="r", newline="", encoding="utf-8") as data:
        reader = csv.DictReader(data)
        for numero_fila, row in enumerate(reader, start=2):
            try:
                alumno = Alumno(**row)
                lista_alumnos.append(alumno)
            except ValidationError as e:
                for error in e.errors():
                    print(
                        f"Fila {numero_fila}: campo '{error['loc'][0]}' - {error['msg']}"
                    )

    return lista_alumnos


RUTA_GRU = DIR_DATA / "grupos.csv"


def leer_grupos(ruta=RUTA_GRU):
    with open(ruta, mode="r", newline="", encoding="utf-8") as data:
        lista_grupos = []
        reader = csv.DictReader(data)
        for numero_fila, row in enumerate(reader, start=2):
            try:
                row["dias_semana"] = list(
                    map(int, row["dias_semana"].strip("[]").split(","))
                )  # Convertir la cadena a lista de enteros
                grupo = Grupo(**row)
                lista_grupos.append(grupo)
            except ValidationError as e:
                for error in e.errors():
                    print(
                        f"Fila {numero_fila}: campo '{error['loc'][0]}' - {error['msg']}"
                    )
    return lista_grupos


RUTA_REG = DIR_DATA / "registros.csv"


def leer_registro(fecha: date, ruta=RUTA_REG):
    # Buscar los registros que hay para este día.
    if not ruta.exists():
        return 0
    num_reg = 0
    with open(ruta, mode="r", newline="", encoding="utf-8") as reg:
        reader = csv.DictReader(reg)
        for line in reader:
            if line["fecha"] == str(fecha):
                num_reg = max(num_reg, int(line["registro"]))
        return num_reg


