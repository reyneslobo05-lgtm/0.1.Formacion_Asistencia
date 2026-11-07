import asyncio
import logging
from datetime import date, datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

from asistencia.configuracion import cargar_workflow
from asistencia.lectura import DIR_DATA
from asistencia.models import AsistenciaError, Contexto, DatosNoEncontradosError
from asistencia.workflow import Workflow

logger = logging.getLogger(__name__)
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
    try:
        nodos = cargar_workflow()
    except AsistenciaError as e:
        logger.error(f"Error al inicializar los nodos: {e}")
        print(f"Error al inicializar los nodos: {e}")
        return
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

    asyncio.run(Workflow(nodos).ejecutar(contexto))
