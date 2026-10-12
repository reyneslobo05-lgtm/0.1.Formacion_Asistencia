from asistencia.models import Contexto
from asistencia.nodos import Nodo


class Workflow:
    def __init__(self, nodos: list[Nodo]):
        self.nodos = nodos

    def ejecutar(self, contexto: Contexto) -> None:
        for nodo in self.nodos:
            nodo.ejecutar(contexto)
