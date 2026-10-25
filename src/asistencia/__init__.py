import logging
from datetime import date, datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

from asistencia.lectura import DIR_DATA
from asistencia.models import Contexto, DatosNoEncontradosError
from asistencia.nodos import (
    EnviarCorreo,
    EscribirContador,
    EscribirCSV,
    FiltrarGruposPorDia,
    LeerAlumnos,
    LeerAusentes,
    LeerGrupos,
    LeerRegistro,
    PasarLista,
)
from asistencia.workflow import Workflow

logging.basicConfig(
    filename=DIR_DATA / "logging.txt",
    level="INFO",
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


def main() -> None:
    try:
        load_dotenv(DIR_DATA.parent / ".env")
    except FileNotFoundError:
        raise DatosNoEncontradosError
    nodos = [
        LeerAlumnos(),
        LeerGrupos(),
        LeerRegistro(),
        FiltrarGruposPorDia(),
        PasarLista(),
        EscribirCSV(),
        EscribirContador(),
        LeerAusentes(),
        EnviarCorreo(),
    ]

    while True:
        dia = (
            input(
                "De qué día quieres pasar la lista, de hoy (responde h) o de un día concreto (responde AAAA-MM-DD)? "
            )
            .lower()
            .strip()
        )
        if dia == "h":
            contexto = Contexto(fecha=datetime.now(tz=ZoneInfo("Europe/Madrid")).date())
            break
        try:
            contexto = Contexto(fecha=date.fromisoformat(dia))
            break
        except ValueError:
            print("Formato no válido!")

    Workflow(nodos).ejecutar(contexto)
