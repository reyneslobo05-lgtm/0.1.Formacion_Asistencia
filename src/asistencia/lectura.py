import csv
import logging
from datetime import date
from pathlib import Path

from pydantic import ValidationError

from asistencia.models import Alumno, DatosNoEncontradosError, DatosVaciosError, Grupo

DIR_DATA = Path(__file__).parent.parent.parent / "data"
RUTA_ALU = DIR_DATA / "alumnos.csv"

logger = logging.getLogger(__name__)


def leer_alumnos(ruta=RUTA_ALU):
    lista_alumnos = []
    try:
        with open(ruta, mode="r", newline="", encoding="utf-8") as data:
            reader = csv.DictReader(data)
            for numero_fila, row in enumerate(reader, start=2):
                try:
                    alumno = Alumno(**row)
                    lista_alumnos.append(alumno)
                except ValidationError as e:
                    for error in e.errors():
                        logger.warning(
                            f"Fila {numero_fila}: campo '{error['loc'][0]}' - {error['msg']}"
                        )
            if len(lista_alumnos) == 0:
                logger.warning("No hay datos de alumnos")
                raise DatosVaciosError
        return lista_alumnos
    except FileNotFoundError as fnfe:
        logger.warning(f"No se encuentra el documento de alumnos, {fnfe}")
        raise DatosNoEncontradosError


RUTA_GRU = DIR_DATA / "grupos.csv"


def leer_grupos(ruta=RUTA_GRU):
    lista_grupos = []
    try:
        with open(ruta, mode="r", newline="", encoding="utf-8") as data:
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
                        logger.warning(
                            f"Fila {numero_fila}: campo '{error['loc'][0]}' - {error['msg']}"
                        )
            if len(lista_grupos) == 0:
                logger.warning("No hay grupos para leer")
                raise DatosVaciosError
            return lista_grupos
    except FileNotFoundError:
        logger.warning("No se encuentra el documento para leer grupos")
        raise DatosNoEncontradosError


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


def detectar_ausencia(fecha: date, alumnos: list[Alumno]):

    year, month, _day = str(fecha).split("-")
    REGISTRO_ALUMNOS = DIR_DATA / f"asistencia_{year}-{month}.csv"

    ausente = {}

    try:
        with open(REGISTRO_ALUMNOS, mode="r", newline="", encoding="utf-8") as reg:
            reader = csv.DictReader(reg)
            for line in reader:
                if line["estado"] == "ausente":
                    alumno_id = line["alumno_id"]
                    ausente[alumno_id] = ausente.get(alumno_id, 0) + 1
    except FileNotFoundError:
        logger.warning("No hay registro de alumnos este mes")
        raise DatosNoEncontradosError

    id_ausentes = []

    for alumno in ausente:
        if ausente[alumno] > 2:
            id_ausentes.append(alumno)

    correo_ausentes = []

    for alumno in alumnos:
        if str(alumno.id) in id_ausentes:
            correo_ausentes.append(alumno.email)

    return correo_ausentes
