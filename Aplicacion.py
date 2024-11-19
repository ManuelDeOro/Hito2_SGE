import pymysql
import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------------------------------
# Conexión a la Base de Datos
# ----------------------------------------
def conectar_base_datos():
    try:
        conexion = pymysql.connect(
            host='localhost',
            user='root',      # Ajusta esto a tus credenciales
            password='curso', # Ajusta esto a tus credenciales
            database='encuestas'
        )
        print("Conexión exitosa a la base de datos.")
        return conexion
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None

# ----------------------------------------
# Clase de Aplicación Principal
# ----------------------------------------
class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Encuestas de Consumo de Alcohol")
        self.root.geometry("900x650")
        self.conexion = conectar_base_datos()
        self.ultima_consulta = "SELECT * FROM encuesta"  # Nueva línea para almacenar la consulta
        self.crear_interfaz()

    # Crear la interfaz de usuario
    def crear_interfaz(self):
        # Frame de opciones CRUD y exportar
        self.frame_crud = tk.Frame(self.root)
        self.frame_crud.pack(fill="x", padx=10, pady=10)

        # Botones CRUD
        tk.Button(self.frame_crud, text="Crear Registro", command=self.crear_registro).pack(side="left", padx=5)
        tk.Button(self.frame_crud, text="Actualizar Registro", command=self.actualizar_registro).pack(side="left", padx=5)
        tk.Button(self.frame_crud, text="Eliminar Registro", command=self.eliminar_registro).pack(side="left", padx=5)
        tk.Button(self.frame_crud, text="Generar Gráfico", command=self.visualizar_graficos).pack(side="left", padx=5)
        tk.Button(self.frame_crud, text="Exportar a Excel", command=self.exportar_a_excel).pack(side="left", padx=5)
        tk.Button(self.frame_crud, text="Filtrar Registros", command=self.filtrar_registros).pack(side="left", padx=5)
        tk.Button(self.frame_crud, text="Ver Todo", command=self.ver_todo).pack(side="left", padx=5)

        # Tabla para mostrar datos
        self.tabla_datos = ttk.Treeview(self.root, columns=("idEncuesta", "Edad", "Sexo", "BebidasSemana", "CervezasSemana",
                                                            "BebidasFinSemana", "BebidasDestiladasSemana",
                                                            "VinosSemana", "PerdidasControl",
                                                            "DiversionDependenciaAlcohol", "ProblemasDigestivos",
                                                            "TensionAlta", "DolorCabeza"), show='headings')
        self.tabla_datos.pack(fill="both", expand=True, padx=10, pady=10)

        # Configuración de las columnas
        columnas = ["idEncuesta", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana",
                    "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]
        for col in columnas:
            self.tabla_datos.heading(col, text=col)
            self.tabla_datos.column(col, width=100)

        # Cargar registros al iniciar
        self.leer_registros()

    # Crear un nuevo registro
    def crear_registro(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Registro")

        # Obtener el siguiente idEncuesta
        cursor = self.conexion.cursor()
        cursor.execute("SELECT MAX(idEncuesta) FROM encuesta")
        resultado = cursor.fetchone()
        siguiente_id = resultado[0] + 1 if resultado[0] is not None else 1
        cursor.close()

        # Mostrar el siguiente ID automáticamente
        label_id = tk.Label(ventana, text=f"idEncuesta: {siguiente_id}")
        label_id.pack()

        # Campos de entrada
        campos = ["Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana",
                  "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]
        entradas = {}

        for campo in campos:
            label = tk.Label(ventana, text=campo)
            label.pack()
            entrada = tk.Entry(ventana)
            entrada.pack()
            entradas[campo] = entrada

        # Función para guardar en la base de datos
        def guardar_registro():
            datos = {campo: entradas[campo].get() for campo in campos}

            # Validar que no haya campos vacíos
            for campo, valor in datos.items():
                if not valor:
                    messagebox.showwarning("Advertencia", f"El campo {campo} no puede estar vacío.")
                    return

            # Insertar el nuevo registro
            cursor = self.conexion.cursor()
            try:
                cursor.execute("""
                    INSERT INTO encuesta (idEncuesta, edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, 
                                          BebidasDestiladasSemana, VinosSemana, PerdidasControl, 
                                          DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (siguiente_id, datos["Edad"], datos["Sexo"], datos["BebidasSemana"], datos["CervezasSemana"],
                      datos["BebidasFinSemana"], datos["BebidasDestiladasSemana"], datos["VinosSemana"],
                      datos["PerdidasControl"], datos["DiversionDependenciaAlcohol"], datos["ProblemasDigestivos"],
                      datos["TensionAlta"], datos["DolorCabeza"]))
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Registro creado con éxito.")
                ventana.destroy()
                self.leer_registros()  # Actualizar la tabla después de crear
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el registro: {e}")
            cursor.close()

        # Botón para guardar
        boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_registro)
        boton_guardar.pack()

    # Leer registros y mostrarlos en la tabla
    def leer_registros(self, query="SELECT * FROM encuesta"):
        self.ultima_consulta = query  # Guardar la última consulta
        cursor = self.conexion.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()

        # Limpiar tabla
        for row in self.tabla_datos.get_children():
            self.tabla_datos.delete(row)

        # Insertar datos en la tabla
        for resultado in resultados:
            self.tabla_datos.insert("", "end", values=resultado)

    # Función para filtrar registros
    def filtrar_registros(self):
        ventana_filtro = tk.Toplevel(self.root)
        ventana_filtro.title("Filtrar Registros")

        # Crear una lista de campos para filtrar
        campos = ["idEncuesta", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana",
                  "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]

        # Lista para almacenar las opciones seleccionadas
        self.filtros_seleccionados = {}

        # Crear campos de filtro
        for campo in campos:
            frame = tk.Frame(ventana_filtro)
            frame.pack(fill="x", padx=10, pady=5)

            label = tk.Label(frame, text=f"Filtrar por {campo}:")
            label.pack(side="left")

            entrada = tk.Entry(frame)
            entrada.pack(side="left")
            self.filtros_seleccionados[campo] = entrada

        # Botón para aplicar filtro
        def aplicar_filtro():
            filtros = {campo: self.filtros_seleccionados[campo].get() for campo in self.filtros_seleccionados}
            query = "SELECT * FROM encuesta WHERE 1=1"

            # Crear filtros dinámicos
            for campo, valor in filtros.items():
                if valor:
                    query += f" AND {campo} LIKE '%{valor}%'"

            self.leer_registros(query)
            ventana_filtro.destroy()

        boton_aplicar = tk.Button(ventana_filtro, text="Aplicar Filtro", command=aplicar_filtro)
        boton_aplicar.pack(pady=10)

    # Ver todos los registros (sin filtros)
    def ver_todo(self):
        self.leer_registros()  # Llamamos a leer_registros sin filtro para ver todos los registros

    # Actualizar un registro
    def actualizar_registro(self):
        item_seleccionado = self.tabla_datos.selection()
        if not item_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un registro para actualizar.")
            return

        # Obtener el ID del registro seleccionado
        id_registro = self.tabla_datos.item(item_seleccionado)["values"][0]
        ventana_actualizar = tk.Toplevel(self.root)
        ventana_actualizar.title("Actualizar Registro")

        # Mostrar ID de encuesta
        label_id = tk.Label(ventana_actualizar, text=f"idEncuesta: {id_registro}")
        label_id.pack()

        # Campos de entrada con los datos actuales
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM encuesta WHERE idEncuesta = %s", (id_registro,))
        registro = cursor.fetchone()
        cursor.close()

        campos = ["Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana",
                  "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]
        entradas = {}

        for i, campo in enumerate(campos):
            label = tk.Label(ventana_actualizar, text=campo)
            label.pack()
            entrada = tk.Entry(ventana_actualizar)
            entrada.insert(0, registro[i+1])  # Insertar valor actual
            entrada.pack()
            entradas[campo] = entrada

        # Función para guardar los cambios
        def guardar_cambios():
            datos = {campo: entradas[campo].get() for campo in campos}

            # Validar que no haya campos vacíos
            for campo, valor in datos.items():
                if not valor:
                    messagebox.showwarning("Advertencia", f"El campo {campo} no puede estar vacío.")
                    return

            # Actualizar el registro en la base de datos
            cursor = self.conexion.cursor()
            try:
                cursor.execute("""
                    UPDATE encuesta 
                    SET Edad=%s, Sexo=%s, BebidasSemana=%s, CervezasSemana=%s, BebidasFinSemana=%s, 
                        BebidasDestiladasSemana=%s, VinosSemana=%s, PerdidasControl=%s, 
                        DiversionDependenciaAlcohol=%s, ProblemasDigestivos=%s, TensionAlta=%s, DolorCabeza=%s
                    WHERE idEncuesta=%s
                """, (datos["Edad"], datos["Sexo"], datos["BebidasSemana"], datos["CervezasSemana"],
                      datos["BebidasFinSemana"], datos["BebidasDestiladasSemana"], datos["VinosSemana"],
                      datos["PerdidasControl"], datos["DiversionDependenciaAlcohol"], datos["ProblemasDigestivos"],
                      datos["TensionAlta"], datos["DolorCabeza"], id_registro))
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Registro actualizado con éxito.")
                ventana_actualizar.destroy()
                self.leer_registros()  # Actualizar la tabla después de la actualización
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el registro: {e}")
            cursor.close()

        # Botón para guardar cambios
        boton_guardar = tk.Button(ventana_actualizar, text="Guardar Cambios", command=guardar_cambios)
        boton_guardar.pack()

    # Eliminar un registro
    def eliminar_registro(self):
        item_seleccionado = self.tabla_datos.selection()
        if not item_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un registro para eliminar.")
            return

        # Obtener el ID del registro seleccionado
        id_registro = self.tabla_datos.item(item_seleccionado)["values"][0]

        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el registro con id {id_registro}?"):
            cursor = self.conexion.cursor()
            try:
                cursor.execute("DELETE FROM encuesta WHERE idEncuesta = %s", (id_registro,))
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Registro eliminado con éxito.")
                self.leer_registros()  # Actualizar la tabla después de eliminar
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el registro: {e}")
            cursor.close()

    # Exportar registros a un archivo Excel
    def exportar_a_excel(self):
        cursor = self.conexion.cursor()
        cursor.execute(self.ultima_consulta)  # Usar la última consulta para obtener los datos
        registros = cursor.fetchall()
        cursor.close()

        # Convertir los datos a un DataFrame
        columnas = ["idEncuesta", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
                    "BebidasDestiladasSemana",
                    "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos",
                    "TensionAlta", "DolorCabeza"]
        df = pd.DataFrame(registros, columns=columnas)

        # Guardar como archivo Excel
        try:
            df.to_excel("registros_encuesta.xlsx", index=False)
            messagebox.showinfo("Éxito", "Datos exportados a Excel con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a Excel: {e}")

    # Visualizar gráficos
    def visualizar_graficos(self):
        # Función para seleccionar tipo de gráfico
        def tipo_grafico():
            tipo = askstring("Tipo de Gráfico", "¿Qué tipo de gráfico deseas? (barras/pastel)")
            if tipo == "barras":
                self.grafico_barras()
            elif tipo == "pastel":
                self.grafico_pastel()
            else:
                messagebox.showerror("Error", "Tipo de gráfico no válido.")

        tipo_grafico()

    # Gráfico de barras
    def grafico_barras(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT Edad, AVG(BebidasSemana) FROM encuesta GROUP BY Edad")
        datos = cursor.fetchall()
        cursor.close()

        edades = [dato[0] for dato in datos]
        consumo = [dato[1] for dato in datos]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(edades, consumo, color='skyblue')
        ax.set_title("Consumo Promedio de Bebidas por Edad")
        ax.set_xlabel("Edad")
        ax.set_ylabel("Consumo Promedio Semanal (Bebidas)")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # Gráfico de pastel
    def grafico_pastel(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT Sexo, COUNT(*) FROM encuesta GROUP BY Sexo")
        datos = cursor.fetchall()
        cursor.close()

        etiquetas = [dato[0] for dato in datos]
        valores = [dato[1] for dato in datos]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'lightgreen'])
        ax.set_title("Distribución por Sexo")

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

# ----------------------------------------
# Ejecución de la aplicación
# ----------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
