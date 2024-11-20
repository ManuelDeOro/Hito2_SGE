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

        # Botones CRUD con estilo
        self.crear_boton(self.frame_crud, "Crear Registro", self.crear_registro, "#ff7f50", "#ffffff")
        self.crear_boton(self.frame_crud, "Actualizar Registro", self.actualizar_registro, "#98fb98", "#000000")
        self.crear_boton(self.frame_crud, "Eliminar Registro", self.eliminar_registro, "#ff6347", "#ffffff")
        self.crear_boton(self.frame_crud, "Generar Gráfico", self.visualizar_graficos, "#dda0dd", "#000000")
        self.crear_boton(self.frame_crud, "Exportar a Excel", self.exportar_a_excel, "#6495ed", "#ffffff")
        self.crear_boton(self.frame_crud, "Filtrar Registros", self.filtrar_registros, "#f0e68c", "#000000")
        self.crear_boton(self.frame_crud, "Ver Todo", self.ver_todo, "#20b2aa", "#ffffff")

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

    def crear_boton(self, frame, texto, comando, color_fondo, color_texto):
        boton = tk.Button(frame, text=texto, command=comando, bg=color_fondo, fg=color_texto, font=("Helvetica", 12, "bold"))
        boton.pack(side="left", padx=5)

    # Crear un nuevo registro
    def crear_registro(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Registro")
        ventana.configure(bg="#f0f8ff")  # Fondo color suave

        # Obtener el siguiente idEncuesta
        cursor = self.conexion.cursor()
        cursor.execute("SELECT MAX(idEncuesta) FROM encuesta")
        resultado = cursor.fetchone()
        siguiente_id = resultado[0] + 1 if resultado[0] is not None else 1
        cursor.close()

        # Mostrar el siguiente ID automáticamente
        label_id = tk.Label(ventana, text=f"idEncuesta: {siguiente_id}", bg="#f0f8ff", font=("Helvetica", 12))
        label_id.pack(pady=10)

        # Campos de entrada
        campos = ["Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana",
                  "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]
        entradas = {}

        for campo in campos:
            label = tk.Label(ventana, text=campo, bg="#f0f8ff", font=("Helvetica", 10))
            label.pack(pady=5)
            entrada = tk.Entry(ventana, font=("Helvetica", 12))
            entrada.pack(pady=5)
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
        boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_registro, bg="#ff7f50", fg="#ffffff", font=("Helvetica", 12, "bold"))
        boton_guardar.pack(pady=10)

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
                      "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos",
                      "TensionAlta", "DolorCabeza"]
            entradas = {}

            for i, campo in enumerate(campos):
                label = tk.Label(ventana_actualizar, text=campo)
                label.pack()
                entrada = tk.Entry(ventana_actualizar)
                entrada.insert(0, registro[i + 1])  # Insertar valor actual
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

    # Función para filtrar registros
    def filtrar_registros(self):
        ventana_filtro = tk.Toplevel(self.root)
        ventana_filtro.title("Filtrar Registros")
        ventana_filtro.configure(bg="#f0f8ff")  # Fondo color suave

        # Crear una lista de campos para filtrar
        campos = ["idEncuesta", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana",
                  "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]

        # Lista para almacenar las opciones seleccionadas
        self.filtros_seleccionados = {}

        # Crear campos de filtro
        for campo in campos:
            frame = tk.Frame(ventana_filtro, bg="#f0f8ff")
            frame.pack(fill="x", padx=10, pady=5)

            label = tk.Label(frame, text=f"Filtrar por {campo}: ", bg="#f0f8ff", font=("Helvetica", 10))
            label.pack(side="left", padx=5)

            # Entrada para cada filtro
            entrada = tk.Entry(frame, font=("Helvetica", 12))
            entrada.pack(side="left", padx=5)
            self.filtros_seleccionados[campo] = entrada

        # Función para aplicar filtros
        def aplicar_filtro():
            filtros = []
            for campo, entrada in self.filtros_seleccionados.items():
                valor = entrada.get()
                if valor:
                    filtros.append(f"{campo} LIKE '%{valor}%'")

            query_filtro = "SELECT * FROM encuesta"
            if filtros:
                query_filtro += " WHERE " + " AND ".join(filtros)

            self.leer_registros(query_filtro)  # Aplicar filtro a la tabla
            ventana_filtro.destroy()

        # Botón para aplicar filtro
        boton_aplicar_filtro = tk.Button(ventana_filtro, text="Aplicar Filtro", command=aplicar_filtro, bg="#98fb98", fg="#000000", font=("Helvetica", 12, "bold"))
        boton_aplicar_filtro.pack(pady=10)

    # Función para ver todos los registros
    def ver_todo(self):
        self.leer_registros()  # Leer todos los registros

    # Función para generar gráficos
    def visualizar_graficos(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM encuesta")
        registros = cursor.fetchall()
        cursor.close()

        # Crear un gráfico de barras con los datos de "Edad"
        edades = [registro[1] for registro in registros]  # Suponiendo que "Edad" es el segundo campo
        plt.figure(figsize=(10, 6))
        plt.hist(edades, bins=10, color='skyblue', edgecolor='black')
        plt.title("Distribución de Edades")
        plt.xlabel("Edad")
        plt.ylabel("Frecuencia")
        plt.show()

    def exportar_a_excel(self):
        try:
            # Usa la última consulta para exportar los datos filtrados
            df = pd.read_sql(self.ultima_consulta, self.conexion)

            # Exportar a un archivo Excel
            df.to_excel("encuestas.xlsx", index=False)
            messagebox.showinfo("Éxito", "Los datos se han exportado correctamente a 'encuestas.xlsx'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a Excel: {e}")

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
                      "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", "ProblemasDigestivos",
                      "TensionAlta", "DolorCabeza"]
            entradas = {}

            for i, campo in enumerate(campos):
                label = tk.Label(ventana_actualizar, text=campo)
                label.pack()
                entrada = tk.Entry(ventana_actualizar)
                entrada.insert(0, registro[i + 1])  # Insertar valor actual
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
            if messagebox.askyesno("Confirmar",
                                   f"¿Estás seguro de que deseas eliminar el registro con id {id_registro}?"):
                cursor = self.conexion.cursor()
                try:
                    cursor.execute("DELETE FROM encuesta WHERE idEncuesta = %s", (id_registro,))
                    self.conexion.commit()
                    messagebox.showinfo("Éxito", "Registro eliminado con éxito.")
                    self.leer_registros()  # Actualizar la tabla después de eliminar
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el registro: {e}")
                cursor.close()


# ----------------------------------------
# Ejecución de la aplicación
# ----------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()