import socket

OBJETIVO = "127.0.0.1"
PUERTOS = [22, 80, 443, 5000, 8000, 8080]

print(f"Escaneo TCP local: {OBJETIVO}")

for puerto in PUERTOS:
    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as cliente:
        cliente.settimeout(0.5)

        resultado = cliente.connect_ex(
            (OBJETIVO, puerto)
        )

    if resultado == 0:
        print(f"Puerto {puerto}: ABIERTO")
    else:
        print(f"Puerto {puerto}: SIN CONEXIÓN")