import logging

from asistencia.escritura import (
    escribir_asistencia,
    escribir_registro,
    veri_doc_asistencia,
)
from asistencia.lectura import (
    detectar_ausencia,
    leer_alumnos,
    leer_grupos,
    leer_registro,
)
from asistencia.models import Contexto
from asistencia.notificaciones import enviar_notificaciones
from asistencia.reglas import seleccionar_grupos
from asistencia.terminal import pasar_lista

logger = logging.getLogger(__name__)


class Nodo:
    def ejecutar(self, contexto: Contexto) -> None:
        # Lógica para ejecutar el nodo con el contexto proporcionado
        raise NotImplementedError


class LeerAlumnos(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        logger.info("Ejecutando Leer Alumnos")
        # Lógica para leer alumnos y actualizar el contexto
        contexto.alumnos = leer_alumnos()


class LeerGrupos(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        logger.info("Ejecutando LeerGrupos")
        # Lógica para leer grupos y actualizar el contexto
        contexto.grupos = leer_grupos()


class LeerRegistro(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        logger.info("Ejecutando LeerRegistro")
        contexto.contador = leer_registro(contexto.fecha)


class FiltrarGruposPorDia(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        logger.info("Ejecutando FiltrarGruposPorDia")
        contexto.grupos_hoy = seleccionar_grupos(contexto.grupos, contexto.fecha)


class PasarLista(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        logger.info("Ejecutando PasarLista")
        contexto.registros_asistencia, contexto.contador = pasar_lista(
            contexto.grupos_hoy, contexto.alumnos, contexto.fecha, contexto.contador
        )


class EscribirContador(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        if contexto.registros_asistencia:
            logger.info("Ejecutando EscribirContador")
            escribir_registro(fecha=contexto.fecha, num=contexto.contador)


class EscribirCSV(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:

        if not contexto.registros_asistencia:
            return
        logger.info("Ejecutando EscribirCSV")
        escribir_asistencia(
            registro_asistencia=contexto.registros_asistencia,
            ruta=veri_doc_asistencia(fecha=contexto.fecha),
        )


class LeerAusentes(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        logger.info("Ejecutando Leer Ausentes")
        if str(contexto.fecha.weekday()) != "4":
            logger.info("Solo se comprueba la asistencia los viernes.")
            return
        contexto.alumnos_ausentes = detectar_ausencia(
            fecha=contexto.fecha, alumnos=contexto.alumnos
        )


class EnviarCorreo(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        logger.info("Ejecutando Enviar Correo")
        if str(contexto.fecha.weekday()) != "4":
            logger.info("Solo se comprueba la asistencia los viernes.")
            return
        enviar_notificaciones(correo_alumnos=contexto.alumnos_ausentes)
