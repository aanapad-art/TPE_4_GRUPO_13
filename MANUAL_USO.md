# Manual de uso — Laboratorio SQL Injection

## 1. Descripción

Este laboratorio permite comparar una aplicación vulnerable a inyección
SQL con una versión corregida mediante consultas parametrizadas.
Incluye un formulario de acceso, un buscador de productos, pruebas
automatizadas, un escáner de puertos y comprobaciones de SQLite.

La práctica se desarrolló en PyCharm. También se puede utilizar
Visual Studio Code, herramienta mencionada en la guía docente.

Todas las pruebas se realizan en el equipo local con datos ficticios.

## 2. Requisitos

- Windows, sistema utilizado para los comandos de este manual.
- Python 3.12, versión utilizada en la práctica.
- PyCharm o Visual Studio Code.
- Navegador web.
- Internet para descargar el proyecto y sus dependencias.
- Git, si se descarga el repositorio mediante comandos.

SQLite viene incluido en Python y no necesita un servidor adicional.

## 3. Obtener el proyecto e instalar dependencias

Si ya tienes el proyecto configurado, continúa con el apartado 4.

Para descargarlo mediante Git, ejecuta:

    git clone https://github.com/aanapad-art/TPE_4_GRUPO_13.git
    cd TPE_4_GRUPO_13

También puedes descargar el ZIP desde GitHub y descomprimirlo.

Abre la carpeta del proyecto en el editor elegido. En una terminal
ubicada dentro de esa carpeta, crea el entorno virtual:

    py -m venv .venv

Instala las dependencias:

    .\.venv\Scripts\python.exe -m pip install -r requirements.txt

Si el entorno y las dependencias ya están preparados, no repitas
la instalación.

## 4. Configurar el editor

### En PyCharm

1. Selecciona Open y abre la carpeta del proyecto.
2. Configura como intérprete el archivo .venv\Scripts\python.exe.
3. Abre el archivo Python que deseas ejecutar.
4. Haz clic derecho dentro del código y selecciona Run.
5. Para detener el servidor, presiona Stop.

### En Visual Studio Code

1. Selecciona File → Open Folder y abre la carpeta del proyecto.
2. Instala la extensión Python de Microsoft si todavía no la tienes.
3. Presiona Ctrl + Shift + P y busca Python: Select Interpreter.
4. Selecciona .venv\Scripts\python.exe dentro del proyecto.
5. Abre Terminal → New Terminal para ejecutar los comandos del manual.
6. Para detener el servidor, presiona Ctrl + C en su terminal.

Los comandos siguientes pueden utilizarse en la terminal de cualquiera
de los dos editores.

## 5. Iniciar la aplicación vulnerable

Ejecuta:

    .\.venv\Scripts\python.exe app_vulnerable.py

Cuando aparezca el mensaje del servidor, abre en el navegador:

    http://127.0.0.1:5000

La aplicación crea automáticamente laboratorio.db con usuarios
y productos ficticios si la base todavía no existe.

Mantén el servidor funcionando durante las pruebas.

## 6. Realizar las pruebas manuales

Regresa a http://127.0.0.1:5000 antes de cada prueba.

### Acceso válido

Introduce en el formulario:

- Usuario: admin
- Contraseña: Demo123

Resultado esperado: acceso concedido.

### Contraseña incorrecta

Introduce:

- Usuario: admin
- Contraseña: incorrecta

Resultado esperado: acceso rechazado.

### Búsqueda normal

Escribe el nombre exacto del producto:

    Teclado

Resultado esperado: producto Teclado con precio 20.0.

### Bypass de autenticación

En el campo usuario escribe:

    admin' -- 

En la contraseña escribe:

    incorrecta

Utiliza un espacio después de los dos guiones del payload.

En la versión vulnerable, el acceso se concede porque el comentario
SQL anula la comprobación de la contraseña.

### Extracción de registros

En el buscador de productos escribe:

    ' UNION SELECT usuario, correo FROM usuarios -- 

En la versión vulnerable aparecen usuarios y correos ficticios.
Los correos se muestran bajo la clave precio porque la respuesta
conserva los nombres de las columnas de la consulta original.

Guarda capturas de las entradas y de las respuestas obtenidas.

## 7. Ejecutar las pruebas automáticas

Con el servidor activo, abre una segunda terminal y ejecuta:

    .\.venv\Scripts\python.exe ataque_sql_i.py

En PyCharm también puedes abrir ataque_sql_i.py y seleccionar Run.

El script realiza las cinco pruebas anteriores y muestra el código
HTTP y el contenido de cada respuesta.

El script prueba el servidor activo en el puerto 5000; no selecciona
automáticamente entre la versión vulnerable y la corregida.

## 8. Comprobar la versión corregida

Detén app_vulnerable.py e inicia:

    .\.venv\Scripts\python.exe app_segura.py

Ejecuta solamente un servidor a la vez, porque ambas versiones
utilizan el puerto 5000.

Repite las pruebas con el mismo script y las mismas entradas:

    .\.venv\Scripts\python.exe ataque_sql_i.py

| Prueba | Resultado esperado en la versión corregida |
|--------|-------------------------------------------|
| Acceso válido | HTTP 200 y acceso concedido. |
| Contraseña incorrecta | HTTP 401 y acceso rechazado. |
| Bypass | HTTP 401 y acceso rechazado. |
| Búsqueda normal | Devuelve el producto Teclado. |
| Extracción | HTTP 200 y lista vacía []. |

En la última prueba, HTTP 200 no significa que el ataque funcionó:
la lista vacía indica que no se extrajeron registros.

Guarda las capturas y compara los resultados de ambas versiones.

## 9. Ejecutar el escaneo de puertos

Con Flask funcionando, ejecuta:

    .\.venv\Scripts\python.exe escaneo_red.py

El script comprueba los puertos TCP 22, 80, 443, 5000, 8000 y 8080
de 127.0.0.1.

El puerto 5000 debe aparecer abierto mientras el servidor esté activo.
Detén Flask y repite el escaneo para observar el cambio.

Otros puertos pueden estar abiertos por servicios de tu computadora.
Un puerto abierto indica que acepta conexiones; no demuestra por
sí solo una vulnerabilidad ni identifica automáticamente el servicio.

## 10. Ejecutar las comprobaciones de SQLite

Primero ejecuta alguna de las aplicaciones para crear la base.
Después ejecuta:

    .\.venv\Scripts\python.exe seguridad_bd.py

El script realiza estas operaciones:

1. Revisa la integridad de SQLite; se espera el resultado ok.
2. Intenta escribir mediante una conexión de solo lectura;
   se espera que la escritura sea rechazada.
3. Crea respaldo_laboratorio.db junto a los archivos Python.

La restricción de lectura corresponde a la conexión del script;
no cambia permanentemente los permisos del archivo de la base.

El respaldo utiliza el mismo nombre en cada ejecución y no mantiene
un historial de copias. Guarda una captura de los resultados.

## 11. Solución de problemas

### No module named flask

Comprueba que el editor utilice .venv\Scripts\python.exe como
intérprete y que las dependencias estén instaladas en ese entorno.

### No se abre la página o el script no puede conectarse

Comprueba que el servidor esté ejecutándose y utiliza la dirección
http://127.0.0.1:5000.

### Puerto 5000 ocupado

Detén la otra ejecución de Flask antes de iniciar el servidor.

### El bypass funciona al probar la versión corregida

Verifica que app_vulnerable.py esté detenido y que hayas ejecutado
app_segura.py con las consultas de acceso y búsqueda parametrizadas.

### PermissionError relacionado con sslkeylog.log

Durante la práctica se resolvió agregando al inicio de ataque_sql_i.py:

    import os
    os.environ.pop("SSLKEYLOGFILE", None)

Este cambio desactiva el registro de claves SSL para ese proceso.
No desactiva la comprobación de certificados.

### Los cambios no aparecen en la aplicación

Guarda el código, detén el servidor y vuelve a ejecutarlo.
La aplicación utiliza debug=False.

## 12. Finalizar y volver a utilizar el laboratorio

1. Guarda los archivos y las evidencias.
2. Detén el servidor con Stop o Ctrl + C.
3. Cierra el editor.

Para utilizar el laboratorio otro día, abre el proyecto y ejecuta
la aplicación. No necesitas reinstalar las dependencias si conservas
el entorno virtual.

GitHub almacena el código. La página local funciona mientras el
servidor esté activo en tu computadora.

## 13. Alcance del laboratorio

Utiliza únicamente datos ficticios y sistemas propios o autorizados.

La versión corregida aborda la inyección SQL de las consultas
mostradas. El ejemplo conserva contraseñas ficticias en texto plano
y no implementa sesiones persistentes, por lo que no es una
aplicación preparada para producción.

Repositorio:
https://github.com/aanapad-art/TPE_4_GRUPO_13