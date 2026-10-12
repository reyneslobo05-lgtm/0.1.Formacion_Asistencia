from datetime import date

from asistencia.models import Grupo


def seleccionar_grupos(grupos: list[Grupo], fecha: date) -> list[Grupo]:
    """
    Función para seleccionar los grupos del objeto en función del día de la semana que sea.
    """
    # Obtener el día de la semana actual (0=lunes, 1=martes, 2=miércoles, 3=jueves, 4=viernes)
    dia_semana = fecha.weekday()
    return [grupo for grupo in grupos if dia_semana in grupo.dias_semana]
