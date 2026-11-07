import asyncio
import logging
import os
import smtplib
from email.message import EmailMessage

from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from asistencia.models import NotificacionError, VariablesError

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=1, max=5),
    retry=retry_if_exception_type(OSError)
    & retry_if_not_exception_type(smtplib.SMTPAuthenticationError),
    reraise=True,
)
async def conectar(usuario, password):
    smtp = await asyncio.to_thread(smtplib.SMTP_SSL, "smtp.gmail.com", 465, timeout=10)
    try:
        await asyncio.to_thread(smtp.login, usuario, password)
    except Exception:
        smtp.close()
        raise
    return smtp


async def enviar_lote(correos, usuario, password) -> list:
    logger.info("Empieza enviar_lote con %s correos", len(correos))
    try:
        smtp = await conectar(usuario, password)
    except smtplib.SMTPAuthenticationError as e:
        logger.warning(
            "Login denegado: revisa contraseña de aplicación y 2 pasos: %s", e
        )
        raise NotificacionError("Login denegado") from e
    except (OSError, smtplib.SMTPException) as e:
        logger.warning("No se pudo conectar tras 3 intentos: %s", e)
        raise NotificacionError("No se pudo conectar") from e
    lista_errores = []
    with smtp:
        for correo in correos:
            msg = EmailMessage()
            msg["Subject"] = "Faltes repetides a l'acadèmia"
            msg["From"] = usuario
            msg["To"] = correo
            msg.set_content(
                "Bon dia, "
                "hem vist que durant l'últim mes heu faltat 3 o més vegades a classe de l'acadèmia."
            )
            try:
                await asyncio.to_thread(smtp.send_message, msg)
            except smtplib.SMTPRecipientsRefused as e:
                logger.warning("Correo de %s no válido: %s", correo, e)
                print(
                    f"No se ha podido enviar el correo a {correo}, su correo registrado no es válido."
                )
                lista_errores.append((correo, e))
            except (smtplib.SMTPException, OSError) as e:
                logger.warning(
                    "Error al enviar la notificación de ausencia de alumno. %s", e
                )
                print(f"No se ha podido enviar el correo a {correo}")
                lista_errores.append((correo, e))
        logger.info("Termina enviar_lote con %s errores", len(lista_errores))
        return lista_errores


async def enviar_notificaciones(correo_alumnos: list) -> None:
    if len(correo_alumnos) == 0:
        logger.info("No hay alumnos ausentes")
        return

    EMAIL_ADDRESS = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        logger.warning("Error para cargar las variables de entorno")
        raise VariablesError

    n = min(5, len(correo_alumnos))
    lotes = [correo_alumnos[i::n] for i in range(n)]
    resultados = await asyncio.gather(
        *[enviar_lote(lote, EMAIL_ADDRESS, EMAIL_PASSWORD) for lote in lotes],
        return_exceptions=True,
    )
    fallidos = []
    for lote, resultado in zip(lotes, resultados):
        if isinstance(resultado, Exception):
            fallidos.extend(lote)
        else:
            fallidos.extend(resultado)
    if len(fallidos) > 0:
        logger.warning("Errores al enviar %s notificaciones", len(fallidos))
        raise NotificacionError(f"Errores al enviar {len(fallidos)} notificaciones")
