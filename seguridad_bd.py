from pathlib import Path
import sqlite3

CARPETA = Path(__file__).resolve().parent

BD = CARPETA / "laboratorio.db"
RESPALDO = CARPETA / "respaldo_laboratorio.db"

if not BD.exists():
    raise SystemExit(
        "Primero ejecuta la aplicación para crear la base."
    )

uri = BD.resolve().as_uri() + "?mode=ro"

origen = sqlite3.connect(
    uri,
    uri=True
)

try:
    resultado = origen.execute(
        "PRAGMA integrity_check"
    ).fetchone()[0]

    print("Resultado de integridad:", resultado)

    print("\nComprobando restricción de escritura...")

    try:
        origen.execute(
            "UPDATE productos "
            "SET precio = precio "
            "WHERE id = 1"
        )

    except sqlite3.OperationalError as error:
        print("Escritura rechazada:", error)

    else:
        origen.rollback()
        raise RuntimeError(
            "La escritura no fue bloqueada."
        )

    destino = sqlite3.connect(RESPALDO)

    try:
        origen.backup(destino)
    finally:
        destino.close()

    print("\nRespaldo creado:", RESPALDO.name)

finally:
    origen.close()