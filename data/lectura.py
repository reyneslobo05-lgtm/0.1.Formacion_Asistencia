import csv
from pathlib import Path
from models import Alumno
from pydantic import ValidationError
RUTA = Path(__file__).parent / 'alumnos.csv'

def leer_alumnos(ruta = RUTA):
    lista_alumnos = []
    with open(ruta, mode='r', newline="", encoding='utf-8') as data:
        reader = csv.DictReader(data)
        for numero_fila, row in enumerate(reader, start=2):
            try:
                alumno = Alumno(**row)
                lista_alumnos.append(alumno)
            except ValidationError as e:
                for error in e.errors():
                    print(f"Fila {numero_fila}: campo '{error['loc'][0]}' - {error['msg']}")
    return lista_alumnos
