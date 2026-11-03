# Laboratorio de SQL Injection — Grupo 13

Proyecto académico de la asignatura Seguridad Informática de la
Universidad Estatal de Milagro (UNEMI).

El laboratorio utiliza Python, Flask y SQLite para comparar una
aplicación vulnerable a inyección SQL con una versión corregida
mediante consultas parametrizadas.

## Objetivo

Demostrar, en un entorno local con datos ficticios, cómo una consulta
SQL construida mediante concatenación puede permitir el bypass de
autenticación y la extracción de registros. Posteriormente, aplicar
consultas parametrizadas y comparar los resultados.

## Herramientas utilizadas
- PyCharm: IDE utilizado para desarrollar y ejecutar la práctica.
- Visual Studio Code: editor indicado en la guía docente, con instrucciones de ejecución incluidas en MANUAL_USO.md.
- Python 3.12.
- Flask.
- SQLite, mediante el módulo sqlite3 de Python.
- PyCharm.
- Git y GitHub.
- Navegador web.

La práctica se realizó en PyCharm. El proyecto también puede ejecutarse
en Visual Studio Code utilizando Python y las mismas dependencias.
El manual incluye instrucciones para ambos editores.
Las versiones de las dependencias se encuentran en requirements.txt.

## Componentes del proyecto

| Archivo | Función |
|---------|---------|
| app_vulnerable.py | Servidor con consultas SQL vulnerables en el acceso y la búsqueda. |
| app_segura.py | Versión con consultas parametrizadas para corregir la SQLi. |
| ataque_sql_i.py | Ejecuta cinco pruebas contra el servidor local activo. |
| escaneo_red.py | Comprueba conexiones TCP a determinados puertos del equipo local. |
| seguridad_bd.py | Revisa la integridad de SQLite, comprueba una conexión de solo lectura y crea un respaldo. |
| requirements.txt | Lista las dependencias y sus versiones. |
| MANUAL_USO.md | Explica la instalación, ejecución y pruebas. |
| .gitignore | Excluye el entorno virtual, las bases de datos y otros archivos locales. |

## Funcionamiento

El navegador o el script de pruebas envía peticiones al servidor Flask.
El servidor consulta la base SQLite y devuelve una respuesta.

La aplicación contiene:

- Un formulario de inicio de sesión.
- Un buscador de productos por nombre exacto.
- Una tabla de usuarios ficticios.
- Una tabla de productos ficticios.

La base laboratorio.db se crea automáticamente al ejecutar cualquiera
de las dos aplicaciones.

## Diferencia entre las versiones

En app_vulnerable.py, las entradas se incorporan directamente al texto
de las consultas SQL. Esto permite que un payload altere su estructura.

En app_segura.py, las consultas utilizan marcadores ? y reciben los
valores por separado. Así, las entradas se interpretan como datos.

## Resultados de las pruebas realizadas

| Prueba | Versión vulnerable | Versión corregida |
|--------|--------------------|-------------------|
| Credenciales válidas | HTTP 200: acceso concedido. | HTTP 200: acceso concedido. |
| Contraseña incorrecta | HTTP 401: acceso rechazado. | HTTP 401: acceso rechazado. |
| Bypass de autenticación | HTTP 200: acceso concedido indebidamente. | HTTP 401: acceso rechazado. |
| Búsqueda de Teclado | Devuelve el producto. | Devuelve el producto. |
| Extracción mediante UNION | Devuelve usuarios y correos ficticios. | HTTP 200: lista vacía. |

El código HTTP debe interpretarse junto con el contenido de la
respuesta. En la búsqueda corregida, HTTP 200 con [] significa que
no se devolvieron registros.

## Ejecución rápida en Windows

Desde la carpeta del proyecto:

    py -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    .\.venv\Scripts\python.exe app_segura.py

Abrir en el navegador:

http://127.0.0.1:5000

Si el entorno ya está creado y las dependencias están instaladas,
solo es necesario ejecutar la aplicación.

Para demostrar la vulnerabilidad, detener primero la versión corregida
y ejecutar app_vulnerable.py.

Consultar MANUAL_USO.md para el procedimiento completo.

## Alcance y limitaciones

- El laboratorio funciona en 127.0.0.1 y utiliza datos ficticios.
- Las dos aplicaciones usan el puerto 5000; se ejecuta una a la vez.
- El script de pruebas actúa sobre el servidor que esté activo.
- La respuesta de acceso no implementa una sesión persistente.
- El ejemplo mantiene contraseñas ficticias en texto plano.
- La corrección de SQLi no convierte el ejemplo en una aplicación
  preparada para producción.
- El escáner comprueba conexiones TCP; no identifica automáticamente
  servicios ni demuestra la existencia de vulnerabilidades.
- El respaldo y la comprobación de integridad no sustituyen otras
  medidas de seguridad.

## Uso académico

Las pruebas deben realizarse únicamente en el laboratorio propio
o en sistemas con autorización expresa.

## Repositorio

https://github.com/aanapad-art/TPE_4_GRUPO_13