import logging
from datetime import date

from asistencia.models import Alumno, Grupo, RegistroAsistencia

logger = logging.getLogger(__name__)


def pasar_lista(
    grupos_seleccionados: list[Grupo], alumnos: list[Alumno], fecha: date, num_reg: int
) -> tuple:
    if not grupos_seleccionados:
        logger.info("Ningún grupo tiene clase hoy")
        return [], num_reg
    ids_grupos_seleccionados = [grupo.id for grupo in grupos_seleccionados]
    alumnos_registrados = []
    estado = {"p": "presente", "a": "ausente", "t": "tarde"}
    num_reg += 1
    for grupo in ids_grupos_seleccionados:
        for alumno in alumnos:
            if alumno.grupo_id == grupo:
                while True:
                    respuesta = (
                        input(
                            f"¿Está el alumno {alumno.nombre} {alumno.apellido}? (p/a/t): "
                        )
                        .strip()
                        .lower()
                    )
                    if respuesta in ["p", "a", "t"]:
                        respuesta = estado[respuesta]
                        break
                    else:
                        print(
                            "Respuesta inválida. Por favor, ingrese 'p' para presente, 'a' para ausente o 't' para tarde."
                        )
                id_registro = int(f"{fecha:%Y%m%d}{num_reg}")
                alumnos_registrados.append(
                    RegistroAsistencia(
                        id=id_registro,
                        grupo_id=alumno.grupo_id,
                        alumno_id=alumno.id,
                        fecha=fecha,
                        estado=respuesta,
                    )
                )
    return alumnos_registrados, num_reg
