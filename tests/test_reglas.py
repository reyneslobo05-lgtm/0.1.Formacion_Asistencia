from datetime import date

from asistencia.models import Grupo
from asistencia.reglas import seleccionar_grupos


def test_seleccionar_grupos():
    grupo1 = Grupo(
        id=1, nombre="Grupo 1", dias_semana=[0, 2, 4]
    )  # Lunes, Miércoles, Viernes
    grupo2 = Grupo(id=2, nombre="Grupo 2", dias_semana=[1])  # Martes
    grupo3 = Grupo(
        id=3, nombre="Grupo 3", dias_semana=[0, 1, 2, 5, 6]
    )  # Todos los días de la semana

    assert seleccionar_grupos([grupo1, grupo2, grupo3], date(2024, 6, 3)) == [
        grupo1,
        grupo3,
    ]  # Lunes
    assert (
        seleccionar_grupos([grupo1, grupo2, grupo3], date(2024, 6, 6)) == []
    )  # Jueves
    assert seleccionar_grupos([grupo1, grupo2, grupo3], date(2024, 6, 8)) == [
        grupo3
    ]  # Sábado
