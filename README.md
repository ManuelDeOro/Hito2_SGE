# Hito2_SGE

Descripción
Este proyecto es una aplicación de escritorio que utiliza Tkinter para la interfaz de usuario y MySQL para gestionar una base de datos relacionada con encuestas sobre consumo de alcohol y salud. La aplicación permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) y visualización de gráficos generados a partir de los datos almacenados en la base de datos.

##Requisitos

Antes de ejecutar la aplicación, asegúrate de tener instalado lo siguiente:

1. Python
Este proyecto está desarrollado en Python 3. Asegúrate de tener Python 3.x instalado. Puedes verificarlo con el siguiente comando:

python --version

2. Instalar Tkinter
Tkinter es la biblioteca estándar de Python para crear interfaces gráficas. Debería estar preinstalada con Python. Si no es así, puedes instalarla mediante:

En Windows: Tkinter debería venir incluido con la instalación de Python. Si no es así, puedes descargarlo desde la página oficial de Python.

3. Instalar MySQL
Si no tienes MySQL instalado, puedes descargarlo e instalarlo desde la página oficial: MySQL Downloads.
Una vez instalado, asegúrate de tener un servidor MySQL en funcionamiento. Puedes verificarlo usando el siguiente comando:

mysql -u root -p

4. Instalar Bibliotecas de Python
Este proyecto utiliza varias bibliotecas externas. Puedes instalarlas utilizando pip. Crea un entorno virtual y ejecuta el siguiente comando en la terminal:

pip install -r requirements.txt

El archivo requirements.txt debe contener las siguientes bibliotecas:

pymysql
pandas
matplotlib
openpyxl

Si prefieres instalar cada librería individualmente, puedes hacerlo con los siguientes comandos:

pip install pymysql
pip install pandas
pip install matplotlib
pip install openpyxl

##Conexión a MySQL
Para conectar la aplicación con MySQL, sigue estos pasos:

Configura tu base de datos MySQL
Asegúrate de tener una base de datos creada. Puedes crear una base de datos llamada encuestas con la siguiente consulta SQL en MySQL:

CREATE DATABASE encuestas;
Crear la tabla de encuestas
Crea una tabla dentro de la base de datos con la siguiente estructura SQL:

CREATE TABLE encuesta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    edad INT,
    genero VARCHAR(10),
    alcohol_consumido FLOAT
);

##Configurar la conexión en el código
En el archivo de código, debes configurar los parámetros de conexión a la base de datos MySQL. Modifica los siguientes valores dentro del código de la aplicación:

## Parámetros de conexión a la base de datos MySQL
self.conexion = pymysql.connect(
    host="localhost",  # Cambia por la IP de tu servidor MySQL si es necesario
    user="root",       # Nombre de usuario de MySQL
    password="tu_contraseña",  # Contraseña de MySQL
    database="encuestas"
)

##Ejecución del Proyecto
1. Ejecutar la aplicación
Para ejecutar el programa, abre una terminal, navega hasta el directorio donde se encuentra el archivo main_window.py, y ejecuta el siguiente comando:

python main_window.py
Esto abrirá la interfaz gráfica de la aplicación, donde podrás interactuar con ella.

2. Operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
Dentro de la aplicación, puedes realizar las siguientes operaciones:

Crear: Agregar nuevos registros de encuestas (nombre, edad, género, cantidad de alcohol consumido).
Leer: Ver los registros existentes en la base de datos.
Actualizar: Modificar los datos de una encuesta ya existente.
Eliminar: Eliminar un registro de encuesta de la base de datos.
Cada una de estas operaciones se puede ejecutar desde los botones en la interfaz gráfica.

3. Visualización de Gráficos
La aplicación permite visualizar gráficos de los datos de la base de datos. Para ello:

La consulta SQL en la base de datos selecciona los datos para ser graficados.
Los gráficos se generan usando matplotlib y se muestran en la interfaz mediante una ventana secundaria.
Puedes ver gráficos de barras, líneas, o cualquier otro tipo de gráfico, dependiendo de cómo se configure la consulta y el gráfico en el código.
4. Exportación a Excel
Para exportar los datos a un archivo Excel:

Se generan los datos a partir de la base de datos.

Se exportan a un archivo Excel utilizando la librería pandas con el siguiente comando:

df.to_excel("encuestas.xlsx", index=False)
El archivo Excel contendrá todos los registros de la base de datos. Si hay filtros aplicados, asegúrate de que solo los datos filtrados sean exportados.

Contribuciones
Si deseas contribuir a este proyecto, por favor abre un issue o crea una pull request en el repositorio de GitHub. Asegúrate de probar el código antes de realizar cualquier cambio.

Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
