import logging
import os
import smtplib
from email.message import EmailMessage

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from asistencia.models import NotificacionError, VariablesError

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=1, max=5),
    retry=retry_if_exception_type((OSError, smtplib.SMTPServerDisconnected)),
    reraise=True,
)
def conectar(usuario, password):
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
    try:
        smtp.login(usuario, password)
    except Exception:
        smtp.close()
        raise
    return smtp


def enviar_notificaciones(correo_alumnos: list) -> None:
    if len(correo_alumnos) == 0:
        logger.info("No hay alumnos ausentes")
        return

    EMAIL_ADDRESS = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    if EMAIL_ADDRESS is None or EMAIL_PASSWORD is None:
        logger.warning("Error para cargar las variables de entorno")
        raise VariablesError

    try:
        smtp = conectar(EMAIL_ADDRESS, EMAIL_PASSWORD)
    except smtplib.SMTPAuthenticationError as e:
        logger.warning(
            "Login denegado: revisa contraseña de aplicación y 2 pasos: %s", e
        )
        raise NotificacionError("Login denegado") from e
    except (OSError, smtplib.SMTPException) as e:
        logger.warning("No se pudo conectar tras 3 intentos: %s", e)
        raise NotificacionError("No se pudo conectar") from e

    with smtp:
        msg = EmailMessage()
        msg["Subject"] = "Faltes repetides a l'acadèmia"
        msg["From"] = EMAIL_ADDRESS
        msg.set_content(
            "Bon dia, "
            "hem vist que durant l'últim mes heu faltat 3 o més vegades a classe de l'acadèmia."
        )

        lista_errores = []
        for alumno in correo_alumnos:
            try:
                del msg["To"]
                msg["To"] = alumno
                smtp.send_message(msg)
            except smtplib.SMTPRecipientsRefused as e:
                logger.warning("Correo de %s no válido: %s", alumno, e)
                print(
                    f"No se ha podido enviar el correo a {alumno}, su correo registrado no es válido."
                )
                lista_errores.append(e)
            except (smtplib.SMTPException, OSError) as e:
                logger.warning(
                    "Error al enviar la notificación de ausencia de alumno. %s", e
                )
                print(f"No se ha podido enviar el correo a {alumno}")
                lista_errores.append(e)
        if len(lista_errores) > 0:
            raise NotificacionError(f"{len(lista_errores)} no enviados")
