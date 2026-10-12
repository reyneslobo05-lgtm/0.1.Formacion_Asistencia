from datetime import date, datetime
from zoneinfo import ZoneInfo

from asistencia.models import Contexto
from asistencia.nodos import (
    EscribirContador,
    EscribirCSV,
    FiltrarGruposPorDia,
    LeerAlumnos,
    LeerGrupos,
    LeerRegistro,
    PasarLista,
)
from asistencia.workflow import Workflow


def main() -> None:
    nodos = [
        LeerAlumnos(),
        LeerGrupos(),
        LeerRegistro(),
        FiltrarGruposPorDia(),
        PasarLista(),
        EscribirCSV(),
        EscribirContador(),
    ]
    dia = (
        input(
            "De qué día quieres pasar la lista, de hoy (responde h) o de un día concreto (responde AAAA-MM-DD)? "
        )
        .lower()
        .strip()
    )

    if dia == "h":
        contexto = Contexto(fecha= datetime.now(tz=ZoneInfo("Europe/Madrid")).date())
    else:
        while True:
            try:
                contexto = Contexto(fecha=date.fromisoformat(dia))
                break
            except ValueError:
                print("Formato no válido!")
                dia = (
                    input(
                        "De qué día quieres pasar la lista, de hoy (responde h) o de un día concreto (responde AAAA-MM-DD)? "
                    )
                    .lower()
                    .strip()
                )

    Workflow(nodos).ejecutar(contexto)
