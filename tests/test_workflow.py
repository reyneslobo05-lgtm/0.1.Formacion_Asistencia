import asyncio

import pytest

from asistencia.models import Contexto, NodeError
from asistencia.nodos import Nodo
from asistencia.workflow import Workflow


class NodoFalso(Nodo):
    def __init__(self, nombre):
        self.nombre = nombre

    async def ejecutar(self, contexto: Contexto):
        contexto.alertas.append(f"Nodo {self.nombre}")


class NodoFallo(Nodo):
    def __init__(self, nombre):
        self.nombre = nombre

    async def ejecutar(self, contexto: Contexto):
        contexto.alertas.append(f"Nodo {self.nombre}")
        raise NodeError(f"Nodo {self.nombre} ha fallado")


@pytest.fixture
def contexto():
    return Contexto(fecha="2026-11-13")


def test_workflow_orden(contexto):
    nodos = [NodoFalso("A"), NodoFalso("B"), NodoFalso("C")]
    workflow_orden = Workflow(nodos)
    asyncio.run(workflow_orden.ejecutar(contexto))
    assert contexto.alertas == ["Nodo A", "Nodo B", "Nodo C"]


def test_workflow_fallo(contexto):
    nodos_uso = [NodoFalso("A"), NodoFallo("B"), NodoFalso("C")]
    worflow_fallo = Workflow(nodos_uso)
    asyncio.run(worflow_fallo.ejecutar(contexto))
    assert contexto.alertas == ["Nodo A", "Nodo B"]


def test_workflow_log(caplog, contexto):
    nodos_log = [NodoFalso("A"), NodoFallo("B"), NodoFalso("C")]
    workflow_log = Workflow(nodos_log)
    asyncio.run(workflow_log.ejecutar(contexto))

    assert "NodoFallo ha fallado" in caplog.text


def test_worflow_vacio(contexto):
    workflow_sin_nodos = Workflow([])
    asyncio.run(workflow_sin_nodos.ejecutar(contexto))

    assert contexto.alertas == []
