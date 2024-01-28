import os
import spacy
import mysql.connector
import sys

def detectar_solucion_satisfactoria(texto):
    nlp = spacy.load("es_core_news_lg")
    
    palabras_clave = ["resuelto", "solucionado", "hay algo mas en lo que le pueda apoyar"]
    
    doc = nlp(texto)
    
    for palabra_clave in palabras_clave:
        if palabra_clave in [token.text.lower() for token in doc]:
            return 0
    
    return 1

def subir_resultado_a_mysql(filename, resultado, guia):
    try:

        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password = '',
            database="audios_dana"
        )

        cursor = conexion.cursor()
        
        query = f"UPDATE calificaciones_{guia} SET solucion_prob = {resultado} WHERE filename = '{filename}';"
        cursor.execute(query)

        conexion.commit()

        print("Actualización exitosa en MySQL.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def analizar_archivos_en_carpeta(carpeta, guia):
    for nombre_archivo in os.listdir(carpeta):
        if nombre_archivo.endswith(".txt"):
            ruta_archivo = os.path.join(carpeta, nombre_archivo)
            filename = os.path.splitext(nombre_archivo)[0] + ".mp3"  # Corregir aquí
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                resultado = detectar_solucion_satisfactoria(contenido)
                subir_resultado_a_mysql(filename, resultado, guia)

def solu_1(guia):
    ruta_de_la_carpeta = r"C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion"
    analizar_archivos_en_carpeta(ruta_de_la_carpeta, guia)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        guia = sys.argv[1]
        solu_1(guia)
    else:
        print("Por favor, proporciona el nombre del archivo como argumento de línea de comandos.")