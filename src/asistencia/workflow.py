import logging

from asistencia.models import Contexto
from asistencia.nodos import Nodo

logger = logging.getLogger(__name__)


class Workflow:
    def __init__(self, nodos: list[Nodo]):
        self.nodos = nodos

    def ejecutar(self, contexto: Contexto) -> None:
        for nodo in self.nodos:
            try:
                nodo.ejecutar(contexto)
                logger.info(f"{type(nodo).__name__} ha funcionado")
            except Exception:
                logger.exception()
                break
