import csv
import logging
from datetime import date

from asistencia.lectura import DIR_DATA, RUTA_REG
from asistencia.models import EscrituraError, RegistroAsistencia

logger = logging.getLogger(__name__)


def escribir_registro(fecha: date, num: int, ruta=RUTA_REG):
    if not ruta.exists():
        with open(ruta, mode="w", newline="", encoding="utf-8") as reg:
            writer = csv.DictWriter(reg, fieldnames=["fecha", "registro"])
            writer.writeheader()
        logger.info("Documento registro creado")

    with open(ruta, mode="a", newline="", encoding="utf-8") as reg:
        writer = csv.DictWriter(reg, fieldnames=["fecha", "registro"])
        writer.writerow({"fecha": str(fecha), "registro": num})


# escribir_registro(fecha = date.fromisoformat("2025-11-12"), num = 1 )


def veri_doc_asistencia(fecha: date, ruta=DIR_DATA):
    year, month, _day = str(fecha).split("-")
    ruta_doc = ruta / f"asistencia_{year}-{month}.csv"
    if not ruta_doc.is_file():
        with open(ruta_doc, "w", newline="", encoding="utf-8") as doc:
            writer = csv.DictWriter(
                doc, fieldnames=["id", "grupo_id", "alumno_id", "fecha", "estado"]
            )
            writer.writeheader()
        logger.info("Nuevo documento de asistencia creado")
    return ruta_doc


def escribir_asistencia(registro_asistencia: list[RegistroAsistencia], ruta) -> None:
    try:
        with open(ruta, "a", newline="", encoding="utf-8") as doc:
            writer = csv.DictWriter(
                doc, fieldnames=["id", "grupo_id", "alumno_id", "fecha", "estado"]
            )
            for line in registro_asistencia:
                writer.writerow(line.model_dump())
    except PermissionError:
        logger.warning("Documento abierto e inaccessible")
        raise EscrituraError
