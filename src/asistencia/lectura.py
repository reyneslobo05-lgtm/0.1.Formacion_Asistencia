import csv

from pathlib import Path
from asistencia.models import Alumno, Grupo
from pydantic import ValidationError

RUTA_ALU = Path(__file__).parent.parent.parent / "data" / "alumnos.csv"


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

RUTA_GRU = Path(__file__).parent.parent.parent / "data" / "grupos.csv"
def leer_grupos(ruta=RUTA_GRU):
    with open(ruta, mode="r", newline="", encoding="utf-8") as data:
        lista_grupos = []
        reader = csv.DictReader(data)
        for numero_fila, row in enumerate(reader, start=2):
            try:
                row['dias_semana'] = list(map(int, row['dias_semana'].strip('[]').split(',')))  # Convertir la cadena a lista de enteros
                grupo = Grupo(**row)
                lista_grupos.append(grupo)
            except ValidationError as e:
                for error in e.errors():
                    print(
                        f"Fila {numero_fila}: campo '{error['loc'][0]}' - {error['msg']}"
                    )
        
    return lista_grupos


if __name__ == "__main__":
    leer_grupos()
    leer_alumnos()