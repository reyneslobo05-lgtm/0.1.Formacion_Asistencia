import json

import pytest
from asistencia.configuracion import ConfigWorkflow, cargar_workflow
from asistencia.models import ConfigurationError, DatosNoEncontradosError
from asistencia.nodos import dict_nodos
from pydantic import ValidationError


def test_ConfigWorkflow_valid():
    config_valid = ConfigWorkflow(
        nombre="Workflow_valid", nodos=list(dict_nodos.keys())
    )
    assert config_valid.nombre == "Workflow_valid"
    assert config_valid.nodos == list(dict_nodos.keys())


def test_ConfigWorkflow_emptynodos():
    with pytest.raises(ValidationError):  # no se cómo hacer lo del match.
        config_empty = ConfigWorkflow(nombre="Workflow_empty", nodos=[])


def test_ConfigWorkflow_invalidnodo():
    with pytest.raises(ValidationError):  # no se cómo hacer lo del match.
        config_invalid = ConfigWorkflow(
            nombre="Workflow_invalid", nodos=["nodo_inexistente"]
        )


def test_ConfigWorkflow_campo_ausente():
    with pytest.raises(ValidationError):  # no se cómo hacer lo del match.
        config_missing = ConfigWorkflow(
            nombre="Workflow_missing"
        )  # Campo 'nodos' ausente


def test_cargar_workflow_valido(tmp_path):
    nodos_reales = [
        "LeerAlumnos",
        "LeerGrupos",
        "LeerRegistro",
        "FiltrarGruposPorDia",
        "PasarLista",
        "EscribirCSV",
        "EscribirContador",
        "LeerAusentes",
        "EnviarCorreo",
    ]
    archivo = tmp_path / "workflow.json"
    archivo.write_text(
        json.dumps(
            {
                "nombre": "test_asistencia_diaria",
                "nodos": [
                    "LeerAlumnos",
                    "LeerGrupos",
                    "LeerRegistro",
                    "FiltrarGruposPorDia",
                    "PasarLista",
                    "EscribirCSV",
                    "EscribirContador",
                    "LeerAusentes",
                    "EnviarCorreo",
                ],
            }
        ),
        encoding="utf-8",
    )

    nodos = cargar_workflow(path=archivo)
    assert len(nodos) == 9
    for i, nodo in enumerate(nodos):
        assert type(nodo).__name__ == nodos_reales[i]


def test_cargar_workflow_archivo_no_encontrado(tmp_path):
    archivo_inexistente = tmp_path / "workflow_inexistente.json"
    with pytest.raises(DatosNoEncontradosError):
        cargar_workflow(path=archivo_inexistente)


def test_cargar_workflow_validacion_error(tmp_path):
    archivo = tmp_path / "workflow.json"
    archivo.write_text(
        json.dumps(
            {
                "nombre": "test_asistencia_diaria",
                "nodos": [
                    "LeerAlumnos",
                    "LeerGrupos",
                    "NodoInexistente",  # Nodo inválido
                    "FiltrarGruposPorDia",
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError):
        cargar_workflow(path=archivo)


def test_cargar_workflow_real():
    nodos = cargar_workflow()
    assert len(nodos) > 0
    assert all(nodo in dict_nodos.values() for nodo in nodos)
