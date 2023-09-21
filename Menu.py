import tkinter as tk
from tkinter import filedialog, messagebox
import re
import json
import graphviz

# Definir variables
entrada_error = None
errores_ingresados = []

# Funciones para las opciones del menú "Archivo"
def abrir_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
    if file_path:
        try:
            with open(file_path, 'r') as archivo:
                contenido = archivo.read()
                texto_operaciones.delete('1.0', tk.END)  # Limpiar el cuadro de texto
                texto_operaciones.insert(tk.END, contenido)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")

def guardar_archivo():
    file_path = filedialog.asksaveasfilename(filetypes=[("Archivos JSON", "*.json")])
    if file_path:
        try:
            contenido = texto_operaciones.get('1.0', tk.END)
            with open(file_path, 'w') as archivo:
                archivo.write(contenido)
                messagebox.showinfo("Guardar", f"Archivo guardado como: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

def guardar_como():
    file_path = filedialog.asksaveasfilename(filetypes=[("Archivos JSON", "*.json")])
    if file_path:
        try:
            contenido = texto_operaciones.get('1.0', tk.END)
            with open(file_path, 'w') as archivo:
                archivo.write(contenido)
                messagebox.showinfo("Guardar como", f"Archivo guardado como: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

def realizar_analisis():
    contenido = texto_operaciones.get('1.0', tk.END)
    palabras = contenido.split()
    num_palabras = len(palabras)
    
    texto_resultados = f"Análisis completo:\n\nNúmero de palabras: {num_palabras}\n"
    texto_operaciones.insert(tk.END, texto_resultados)

def mostrar_errores():
    error = entrada_error.get()
    if error:
        errores_ingresados.append(error)
        texto_operaciones.insert(tk.END, f"Error agregado: {error}\n")
        entrada_error.delete(0, tk.END)  

# Función para analizar y guardar los errores en un archivo JSON
def analizar_errores():
    contenido = texto_operaciones.get('1.0', tk.END)
    
    errores = []
    contenido_corregido = contenido

    errores_encontrados = re.findall(r'\b(errror)\b', contenido_corregido)
    for error_encontrado in errores_encontrados:
        errores.append(error_encontrado)
        contenido_corregido = contenido_corregido.replace(error_encontrado, 'error')

    datos = {
        "errores": errores,
        "contenido_corregido": contenido_corregido
    }

    # Crear un archivo de salida JSON
    archivo_salida = "salida.json"

    try:
        with open(archivo_salida, 'w') as archivo_json:
            json.dump(datos, archivo_json, indent=4)

        texto_operaciones.insert(tk.END, f"Datos analizados y guardados en {archivo_salida}\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo de salida: {str(e)}")

def generar_reporte1():
    contenido = texto_operaciones.get('1.0', tk.END)
    
    lineas = contenido.split('\n')
    
    # Crear un objeto de grafo de Graphviz
    dot = graphviz.Digraph(format='png', engine='dot', graph_attr={'rankdir': 'TB'}, node_attr={'shape': 'box', 'style': 'filled', 'fillcolor': 'lightblue1', 'fontname': 'Helvetica'})
    
    for linea in lineas:
        partes = linea.split(':')
        if len(partes) == 2:
            operacion = partes[0].strip()
            resultado = partes[1].strip()
            dot.node(operacion, operacion, color='lightblue2')
            dot.node(resultado, resultado, color='lightblue2')
            dot.edge(operacion, resultado, color='lightblue3')

    dot.render('grafo_operaciones')
    
    import os
    os.system('start grafo_operaciones.png')
    texto_operaciones.insert(tk.END, "Generando reporte...\n")

def salir():
    ventana.quit()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Menú con Interfaz Gráfica")

# Crear un menú
menu = tk.Menu(ventana)
ventana.config(menu=menu)

# Opción "Archivo" con subopciones
menu_archivo = tk.Menu(menu)
menu.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Abrir", command=abrir_archivo)
menu_archivo.add_command(label="Guardar", command=guardar_archivo)
menu_archivo.add_command(label="Guardar como", command=guardar_como)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=salir)

#Cuadro de texto en la ventana
texto_operaciones = tk.Text(ventana, wrap=tk.WORD, height=10, width=40)
texto_operaciones.pack()

# Campo de entrada para agregar errores
entrada_error = tk.Entry(ventana, width=30)
entrada_error.pack()
boton_agregar = tk.Button(ventana, text="Agregar Error", command=analizar_errores)
boton_agregar.pack()

# Opciones "Analizar", "Errores" y "Reporte"
menu.add_command(label="Analizar", command=realizar_analisis)
menu.add_command(label="Errores", command=analizar_errores)
menu.add_command(label="Reporte", command=generar_reporte1)
ventana.mainloop()