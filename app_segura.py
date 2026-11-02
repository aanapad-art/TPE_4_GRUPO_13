from pathlib import Path
import sqlite3

from flask import Flask, request, jsonify

app = Flask(__name__)

CARPETA = Path(__file__).resolve().parent
BD = CARPETA / "laboratorio.db"


def iniciar_bd():
    with sqlite3.connect(BD) as conexion:
        conexion.executescript("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                usuario TEXT UNIQUE NOT NULL,
                clave TEXT NOT NULL,
                correo TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL
            );
        """)

        conexion.executemany(
            """
            INSERT OR IGNORE INTO usuarios
            (id, usuario, clave, correo)
            VALUES (?, ?, ?, ?)
            """,
            [
                (1, "admin", "Demo123", "admin@example.test"),
                (2, "ana", "Ana123", "ana@example.test"),
                (3, "luis", "Luis123", "luis@example.test"),
            ],
        )

        conexion.executemany(
            """
            INSERT OR IGNORE INTO productos
            (id, nombre, precio)
            VALUES (?, ?, ?)
            """,
            [
                (1, "Teclado", 20.0),
                (2, "Mouse", 10.0),
                (3, "Monitor", 150.0),
            ],
        )


def conectar():
    uri = BD.resolve().as_uri() + "?mode=ro"

    conexion = sqlite3.connect(
        uri,
        uri=True
    )

    conexion.row_factory = sqlite3.Row
    return conexion


@app.get("/")
def inicio():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Laboratorio SQL Injection</title>
    </head>
    <body>
        <h1>Laboratorio local de SQL Injection</h1>
        <p>Práctica académica con datos ficticios.</p>

        <h2>Inicio de sesión</h2>

        <form action="/login" method="post">
            <label>Usuario:</label>
            <input type="text" name="usuario" required>

            <br><br>

            <label>Contraseña:</label>
            <input type="password" name="clave" required>

            <br><br>

            <button type="submit">Ingresar</button>
        </form>

        <hr>

        <h2>Búsqueda de productos</h2>

        <form action="/buscar" method="get">
            <label>Nombre exacto del producto:</label>
            <input type="text" name="nombre">

            <br><br>

            <button type="submit">Buscar</button>
        </form>
    </body>
    </html>
    """


@app.post("/login")
def login():
    usuario = request.form.get("usuario", "")
    clave = request.form.get("clave", "")

    consulta = (
        "SELECT id, usuario FROM usuarios "
        "WHERE usuario = ? AND clave = ?"
    )

    conexion = conectar()

    try:
        fila = conexion.execute(
            consulta,
            (usuario, clave)
        ).fetchone()

    except sqlite3.Error:
        return jsonify(error="Consulta inválida"), 400

    finally:
        conexion.close()

    if fila:
        return jsonify(
            acceso=True,
            usuario=fila["usuario"]
        ), 200

    return jsonify(acceso=False), 401


@app.get("/buscar")
def buscar():
    nombre = request.args.get("nombre", "")

    consulta = (
        "SELECT nombre, precio FROM productos "
        "WHERE nombre = ?"
    )

    conexion = conectar()

    try:
        filas = conexion.execute(
            consulta,
            (nombre,)
        ).fetchall()

    except sqlite3.Error:
        return jsonify(error="Consulta inválida"), 400

    finally:
        conexion.close()

    return jsonify(
        [dict(fila) for fila in filas]
    ), 200


if __name__ == "__main__":
    iniciar_bd()
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )