from asistencia.escritura import (
    escribir_asistencia,
    escribir_registro,
    veri_doc_asistencia,
)
from asistencia.lectura import leer_alumnos, leer_grupos, leer_registro
from asistencia.models import Contexto
from asistencia.reglas import seleccionar_grupos
from asistencia.terminal import pasar_lista


class Nodo:
    def ejecutar(self, contexto: Contexto) -> None:
        # Lógica para ejecutar el nodo con el contexto proporcionado
        raise NotImplementedError


class LeerAlumnos(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        # Lógica para leer alumnos y actualizar el contexto
        try:
            contexto.alumnos = leer_alumnos()
        except NotImplementedError:
            print("No hay alumnos para leer.")


class LeerGrupos(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        # Lógica para leer grupos y actualizar el contexto
        try:
            contexto.grupos = leer_grupos()
        except NotImplementedError:
            print("No hay grupos para leer.")


class LeerRegistro(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        try:
            contexto.contador = leer_registro(contexto.fecha)
        except FileNotFoundError:
            print("The file was not found.")


class FiltrarGruposPorDia(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        # Lógica para filtrar grupos según el día de la semana y actualizar el contexto
        try:
            contexto.grupos_hoy = seleccionar_grupos(contexto.grupos, contexto.fecha)
        except NotImplementedError:
            print("No hay grupos para filtrar.")


class PasarLista(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        # Lógica para pasar la lista en el terminal
        contexto.registros_asistencia, contexto.contador = pasar_lista(
            contexto.grupos_hoy, contexto.alumnos, contexto.fecha, contexto.contador
        )


class EscribirContador(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        if contexto.registros_asistencia:
            escribir_registro(fecha=contexto.fecha, num=contexto.contador)


class EscribirCSV(Nodo):
    def ejecutar(self, contexto: Contexto) -> None:
        if not contexto.registros_asistencia:
            return
        escribir_asistencia(
            registro_asistencia=contexto.registros_asistencia,
            ruta=veri_doc_asistencia(fecha=contexto.fecha),
        )
