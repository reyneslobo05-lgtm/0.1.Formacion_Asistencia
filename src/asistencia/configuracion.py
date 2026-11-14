import logging

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from asistencia.lectura import DIR_DATA
from asistencia.models import ConfigurationError, DatosNoEncontradosError
from asistencia.nodos import dict_nodos

logger = logging.getLogger(__name__)
DIR_JSON = DIR_DATA.parent / "workflow.json"


class ConfigWorkflow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre: str
    nodos: list[str] = Field(
        min_length=1,
        description="Lista de nodos a ejecutar en el workflow, en orden de ejecución",
    )

    @field_validator("nodos")
    @classmethod
    def existen(cls, valor):
        for nodo in valor:
            if nodo not in dict_nodos:
                raise ValueError(f"El nodo {nodo} no está definido en el programa.")
        return valor


def cargar_workflow(path = DIR_JSON):
    try:
        config = ConfigWorkflow.model_validate_json(
            path.read_text(encoding="utf-8")
        )
    except FileNotFoundError:
        logger.error(f"No se encontró el archivo {path}.")
        raise DatosNoEncontradosError(f"No se encontró el archivo {path}.")
    except ValidationError as e:
        for error in e.errors():
            campo = ".".join(str(parte) for parte in error["loc"]) or "JSON"
            logger.warning(f"Campo: '{campo}' Mensaje: {error['msg']}")
        raise ConfigurationError(f"Error de validación en el archivo {path}: {e}")
    lista_nodos = []
    for nodo in config.nodos:
        lista_nodos.append(dict_nodos[nodo])
    return lista_nodos
