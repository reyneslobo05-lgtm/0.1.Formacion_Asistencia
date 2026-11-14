import asyncio
import smtplib

import pytest
from tenacity import wait_none

from asistencia.models import NotificacionError, VariablesError
from asistencia.notificaciones import conectar, enviar_notificaciones


@pytest.fixture
def install_fake_class(monkeypatch):
    monkeypatch.setattr(smtplib, "SMTP_SSL", SMTPFake)
    monkeypatch.setattr(SMTPFake, "lista_rechazo", [])
    monkeypatch.setattr(SMTPFake, "destinatarios_enviados", [])
    monkeypatch.setattr(SMTPFake, "cont_login", 0)
    monkeypatch.setattr(SMTPFake, "cont_conexion", 0)
    return SMTPFake


@pytest.fixture
def environment(monkeypatch):
    monkeypatch.setenv("EMAIL_USER", "joanreynes@ejemplo.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "contraseña123")
    return SMTPFake


@pytest.fixture
def anular_esperas(monkeypatch):
    monkeypatch.setattr(conectar.retry, "wait", wait_none())


class SMTPFake:
    lista_rechazo = []
    cont_login = 0
    cont_conexion = 0
    destinatarios_enviados = []
    fallos_conexion = 0
    fallar_login = False

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

        SMTPFake.cont_conexion += 1
        if SMTPFake.cont_conexion <= SMTPFake.fallos_conexion:
            raise OSError("Ha habido fallos de conexión")

    def login(self, usuario, password):
        SMTPFake.cont_login += 1
        if SMTPFake.fallar_login:
            raise smtplib.SMTPAuthenticationError(
                535, b"Error"
            )  # no se qué mensaje de error poner.

    def send_message(self, msg):
        destinatario = msg["To"]
        if destinatario in self.lista_rechazo:
            raise smtplib.SMTPRecipientsRefused({destinatario: (550, b"User unknown")})
        else:
            SMTPFake.destinatarios_enviados.append(destinatario)

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


def test_notificaciones_lista_vacia(install_fake_class):
    resultado = enviar_notificaciones(correo_alumnos=[])
    asyncio.run(resultado)
    assert SMTPFake.cont_conexion == 0
    assert SMTPFake.destinatarios_enviados == []


lista_correos = [
    "alumno0@example.com",
    "alumno1@example.com",
    "alumno2@example.com",
    "alumno3@example.com",
    "alumno4@example.com",
    "alumno5@example.com",
    "alumno6@example.com",
    "alumno7@example.com",
    "alumno8@example.com",
    "alumno9@example.com",
]


def test_notificaciones_lista_diez(install_fake_class, environment):

    resultado = enviar_notificaciones(correo_alumnos=lista_correos)
    asyncio.run(resultado)
    assert SMTPFake.cont_conexion == 5
    assert sorted(SMTPFake.destinatarios_enviados) == sorted(lista_correos)


lista_correos_3 = ["alumno0@example.com", "alumno1@example.com", "alumno2@example.com"]


def test_notificaciones_tres_conex(install_fake_class, environment):
    resultado = enviar_notificaciones(lista_correos_3)
    asyncio.run(resultado)
    assert SMTPFake.cont_conexion == 3
    assert sorted(lista_correos_3) == sorted(SMTPFake.destinatarios_enviados)


def test_notificaciones_sin_venv(install_fake_class, monkeypatch):
    monkeypatch.delenv("EMAIL_USER", raising=False)
    monkeypatch.delenv("EMAIL_PASSWORD", raising=False)
    with pytest.raises(VariablesError):
        asyncio.run(enviar_notificaciones(lista_correos_3))

    assert SMTPFake.cont_conexion == 0


def test_notificaciones_correo_malo(install_fake_class, environment):
    SMTPFake.lista_rechazo.append("alumno10@example.com")
    lista_correos_malo = lista_correos_3 + ["alumno10@example.com"]
    with pytest.raises(NotificacionError):
        asyncio.run(enviar_notificaciones(lista_correos_malo))

    assert sorted(SMTPFake.destinatarios_enviados) == sorted(lista_correos_3)


def test_notificacioens_login_denegado(install_fake_class, environment, monkeypatch):
    monkeypatch.setattr(SMTPFake, "fallar_login", True)
    with pytest.raises(NotificacionError, match="Errores al enviar 10 notificaciones"):
        asyncio.run(enviar_notificaciones(lista_correos))

    assert SMTPFake.destinatarios_enviados == []
    assert SMTPFake.cont_login == 5


def test_notificaciones_no_red(install_fake_class, environment, anular_esperas):
    SMTPFake.fallos_conexion = 100

    with pytest.raises(NotificacionError):
        asyncio.run(enviar_notificaciones(["alumno1@example.com"]))

    assert SMTPFake.cont_login == 0
    assert SMTPFake.cont_conexion == 3


def test_notificaciones_un_fallo_red(install_fake_class, environment, anular_esperas):
    SMTPFake.fallos_conexion = 1

    asyncio.run(enviar_notificaciones(["alumno1@example.com"]))

    assert SMTPFake.cont_login == 1
    assert SMTPFake.destinatarios_enviados == ["alumno1@example.com"]
