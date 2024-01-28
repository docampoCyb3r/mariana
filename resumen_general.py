print("\n****************INICIANDO OBTENCION DE RESUMEN*******************\n")

import os
import mysql.connector
import openai

def hacer_pregunta(fragmento_texto):
    openai.api_key = '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'
    completion = openai.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
                {"role": "system", "content": "Eres un experto en análisis de calidad de call center con una experiencia de 30 años en el campo. Se te ha encomendado analizar el siguiente texto."},
                {"role": "user", "content": fragmento_texto}
    ]
    )
    respuesta2 = completion.choices[0].message.content
    return respuesta2


def descomponer_texto(texto):
    fragmentos = [texto[i:i+9000] for i in range(0, len(texto), 9000)]
    return fragmentos


def generar_resumen(texto):
    # Crear una conexión
    conexion = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="",
        database="audios_dana"
    )

    # Crear un cursor
    cursor = conexion.cursor()

    # Actualizar el estado a "Contextualizando" en la base de datos
    update_query = "UPDATE audios SET status = 'Contextualizando' WHERE status = 'Calificando'"
    cursor.execute(update_query)
    conexion.commit()

    texto_resumen = ""

    fragmentos_texto = descomponer_texto(texto)

    respuestas = []

    for fragmento in fragmentos_texto:
        pregunta = f"dado el siguiente texto: {fragmento}, dame: 0.- Identifica quien es el cliente y quien es el agente telefonico, 1.- El resumen de la conversación, 2.- Objetivo de la llamada, 3.- Que solicita el cliente, 4.- Proceso que siguio el agente telefonico, 5.- Solucion proporcionada por el agente telefonico, 6.- Fortalezas durante la conversación, 7.- Debilidades durante la conversación"
        respuesta = hacer_pregunta(pregunta)
        respuestas.append(respuesta)

    transcripcion_completa = "".join(respuestas)

    respuesta_generada = transcripcion_completa

    respuesta_generada = respuesta.split("\n")

    texto_resumen =  str.join("\n", respuesta_generada)

    # Cerrar el cursor y la conexión antes del return
    cursor.close()
    conexion.close()

    return texto_resumen


def validar_archivos(carpeta_origen, carpeta_destino):
    # Crea la carpeta de destino si noo existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    for nombre_archivo in os.listdir(carpeta_origen):
        if nombre_archivo.endswith('.txt'):
            ruta_archivo_origen = os.path.join(carpeta_origen, nombre_archivo)
            
            if os.path.getsize(ruta_archivo_origen) == 0:  # Verificar si el archivo está vacío
                print("El archivo está vacío. No se encontraron palabras clave.\n")
                resultado = "No se encontraron palabras clave."
            else:
                with open(ruta_archivo_origen, 'r', encoding='utf-8') as archivo:
                    texto = archivo.read()

            resumen = generar_resumen(texto) 

            # Genera la ruta completa del archivo de resumen en la carpeta de destino
            nombre_archivo_resumen = os.path.splitext(nombre_archivo)[0]  # Elimina la extensión .txt
            ruta_archivo_resumen = os.path.join(carpeta_destino, nombre_archivo_resumen + ".txt")

            # Guarda el resumen en un archivo de texto en la carpeta de destino
            with open(ruta_archivo_resumen, 'w', encoding='utf-8') as archivo_resumen:
                archivo_resumen.write(resumen)
            
            print(f"Transcripción del archivo '{resumen}' guardada en '{ruta_archivo_resumen}'")
            
def concatenar_archivos(carpeta1, carpeta2):
    archivos1 = os.listdir(carpeta1)

    for archivo1 in archivos1:
        if archivo1.endswith(".txt"):
            with open(os.path.join(carpeta1, archivo1), "r", encoding='utf-8') as f:
                contenido1 = f.read()

            archivos2 = os.listdir(carpeta2)

            for archivo2 in archivos2:
                if archivo2.endswith(".txt"):
                    with open(os.path.join(carpeta2, archivo2), "r", encoding='utf-8') as f:
                        contenido2 = f.read()

                    contenido_concatenado = contenido1 + ("\n") + ("\n") + contenido2

                    # Obtener el nombre del archivo de la primera carpeta
                    nombre_archivo1, _ = os.path.splitext(archivo1)

                    # Guardar el resultado con el nombre del archivo de la primera carpeta
                    with open(os.path.join(carpeta1, f"{nombre_archivo1}.txt"), "w+", encoding='utf-8') as f:
                        f.write(contenido_concatenado)

                    return f"{nombre_archivo1}.txt"
def concat():
    carpeta1 = r"C:\Users\Aero\Desktop\Proceso_Clidad\resumen_llamada"
    carpeta2 = r"C:\Users\Aero\Desktop\Proceso_Clidad\tiempos_espera"

    ruta_archivo_concatenado = concatenar_archivos(carpeta1, carpeta2)

    print(ruta_archivo_concatenado)

def resumen():
    carpeta_archivos_origen = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'
    carpeta_archivos_destino = r'C:\Users\Aero\Desktop\Proceso_Clidad\resumen_llamada'
    validar_archivos(carpeta_archivos_origen, carpeta_archivos_destino)
    concat()
    
    
    

if __name__ == "__main__":
    resumen()
    print("\n****************FINALIZA RESUMEN GENERAL CON EXITO****************\n")