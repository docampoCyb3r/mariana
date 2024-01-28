import os
import mysql.connector
import openai
import json
import time
import sys
import traceback
import speech_recognition as sr
from pydub import AudioSegment
import re

start_time = time.time()

def hacer_pregunta(fragmento_texto):
      openai.api_key = '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'
      completion = openai.chat.completions.create(
      model="gpt-4-0125-preview",
      messages=[
                  {"role": "system", "content": "Eres un analista de calidad experto en calificar a travez de parametros con mas de 30 años de experiencia y se te a encomentado analizar el siguiente texto"},
                  {"role": "user", "content": fragmento_texto}
      ]
      )
      respuesta = completion.choices[0].message.content
      return respuesta




# ****************** obenter calificaciones del audio (json y tabla)
def guia_set(guia):
    print("\n--------- INICIANDO PROCESO DE CALIFICAICON POR GUIA ---------\n")
    start_time = time.time()

    carpeta_archivos = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion' 
    carpeta_data = r'C:\Users\Aero\Desktop\Proceso_Clidad\calificacion'

    archivos_a_analizar = [archivo for archivo in os.listdir(carpeta_archivos) if archivo.endswith(('.txt', '.doc', '.docx'))]

    conexion = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="",
        database="audios_dana"
    )

    try:
        cursor = conexion.cursor()

        consulta = f"SELECT nombre_punto, contexto FROM {guia} WHERE nombre_punto <> 'Manejo_de_Herramientas';"
        cursor.execute(consulta)
        resultados = cursor.fetchall()

        for archivo in archivos_a_analizar:
            local_txt_path = os.path.join(carpeta_data, 'pov', f"{os.path.splitext(archivo)[0]}.txt")

            with open(local_txt_path, "w", encoding='utf-8') as archivo_txt:
                for resultado in resultados:
                    archivo_txt.write(f"'{resultado[0]}': {resultado[1]}\n")

                print(f"\nDatos guardados de {guia} en {local_txt_path}\n")

    except mysql.connector.Error as error:
        print(f"\nError: {error}\n")

    finally:
        if cursor:
            cursor.close()
        if conexion.is_connected():
            conexion.close()

    for archivo in archivos_a_analizar:
        ruta_archivo = os.path.join(carpeta_archivos, archivo)
        ruta_resultado_json = os.path.join(carpeta_data, 'pov1', f"{os.path.splitext(archivo)[0]}.txt")

        with open(ruta_archivo, 'r', encoding='utf-8') as archivo_lectura:
            texto_completo = archivo_lectura.read()

        with open(local_txt_path, 'r', encoding='utf-8') as archivo_lectura:
            contenido_txt = archivo_lectura.read()

        pregunta = f"""Tengo la siguiente transcripción de una llamada telefonica: {texto_completo} , Como EXPERTO EN CALL CENTER de telecomunicaciones EN EL AREA de calidad con mas de 25 años de experiencia, evalúa si el agente cumple lo siguientes Criterios, toma en cuenta sinonimos y los ejemplos que se describen, asigna en valor de 1 si cumple el parametro y el valor de 0 si no cumple el parametro: 

                        {contenido_txt}

                        Si no aplica O NO SE MENCIONA, NO LO ETIQUETES COMO 'N/A' o 0; asigne el valor de 1 SIEMPRE

                        Muestra los resultados en formato de json (parametro, calificaciones), sigue forzosamente este formato
                        ejemplo:

                        {{
                          "parametro": "calificacion"
                        }},

                        y ademas muestra los resultados en formato de tabla (parametro, calificaciones y justificacion)
                        ejemplo:

                        |    Parametro        |  Calificacion   |   justificacion  |
                        |nombre del parametro |     1           | justificacion    |
                       ademas dame puntos a mejorar durante la conversacion
                       ejemplo
                       
                       puntos a mejorar durante la conversacion:
                       1
                       2
                       3
                       
                    """

        respuesta = hacer_pregunta(pregunta)

        print("\n", respuesta, "\n")

        with open(ruta_resultado_json, 'w', encoding='utf-8') as archivo_txt:
            archivo_txt.write(respuesta)

        print(f"\nTranscripción del archivo '{archivo}' guardada en '{ruta_resultado_json}'\n")

    end_time = time.time()
    execution_time = end_time - start_time
    print("\nTiempo de ejecución: {:.2f} segundos".format(execution_time))




#*********************** crear json del prompt de la base de datos
def extraccion(guia):
    print("\nINICIANDO EXTRACCION DE CALIFICACIONES\n")
    start_time = time.time()

    carpeta_data = r'C:\Users\Aero\Desktop\Proceso_Clidad\calificacion'

    conexion = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="",
        database="audios_dana"
    )

    try:
        cursor = conexion.cursor()

        consulta = f"SELECT nombre_punto, puntaje FROM {guia} WHERE nombre_punto <> 'Manejo_de_Herramientas';"
        cursor.execute(consulta)
        resultados = cursor.fetchall()


        local_txt_path = os.path.join(carpeta_data, 'pov2', "tabla_puntaje.txt")

        with open(local_txt_path, "w", encoding='utf-8') as archivo_txt:
            for resultado in resultados:
                archivo_txt.write(f"'{resultado[0]}': {resultado[1]}\n")

            print(f"\nDatos guardados de {guia} en {local_txt_path}\n")

        with open(local_txt_path, 'r', encoding='utf-8') as archivo_lectura:
            contenido_archivo = archivo_lectura.read()

        pregunta2 = f"""Tengo la siguiente informacion: {contenido_archivo}

                        Muestra los resultados en formato de json (parametro, calificaciones), no me des mas contexto mas que el json, SOLO QUIERO EL JSON y no modifiques mayusculas y minuculas
                        ejemplo

                        {{
                            "parametro: calificacion"
                        }}

                    """

        respuesta2 = hacer_pregunta(pregunta2)

        print("\n", respuesta2, "\n")

        local_txt_path = os.path.join(carpeta_data, 'pov3', "tabla_puntaje_json.txt")

        with open(local_txt_path, "w", encoding='utf-8') as archivo_txt:
            archivo_txt.write(respuesta2)

    except mysql.connector.Error as error:  
        print(f"\nError: {error}\n")

    finally:
        if cursor:
            cursor.close()
        if conexion.is_connected():
            conexion.close()
            
    end_time = time.time()
    execution_time = end_time - start_time
    print("\nTiempo de ejecución: {:.2f} segundos\n".format(execution_time))
    
    
    
    

#*********************** extraccion de json del archivo 1
def extraccion_1():
    
    print("\nINICIANDO EXTRACCION DE PRIMER JSON\n")

    carpeta_entrada = r'C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\pov1'

    carpeta_salida = r'C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\json_calificacion_1'

    for nombre_archivo in os.listdir(carpeta_entrada):

        ruta_entrada = os.path.join(carpeta_entrada, nombre_archivo)

        if os.path.isfile(ruta_entrada) and nombre_archivo.endswith('.txt'):

            with open(ruta_entrada, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()

            inicio_json = texto_completo.find("{")

            json_str = texto_completo[inicio_json:]

            fin_json = json_str.rfind("}") + 1

            json_str = json_str[:fin_json]

            try:
                json_data = json.loads(json_str)

                ruta_salida = os.path.join(carpeta_salida, f"{nombre_archivo[:-4]}.json")

                with open(ruta_salida, 'w', encoding='utf-8') as archivo_salida:
                    json.dump(json_data, archivo_salida, indent=2)

                print(f"\nResultado guardado en: {ruta_salida}\n")
            except json.decoder.JSONDecodeError as e:
                print(f"\nError al cargar el JSON en el archivo {nombre_archivo}: {e}\n")




#*********************** extraccion de json del archivo 2                
def extraccion_2():
    
    print("\nINICIANDO EXTRACCION DE SEGUNDO JSON\n")

    carpeta_entrada = r'C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\pov3'
    carpeta_salida = r'C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\json_calificacion_2'

    for nombre_archivo in os.listdir(carpeta_entrada):

        ruta_entrada = os.path.join(carpeta_entrada, nombre_archivo)

        if os.path.isfile(ruta_entrada) and nombre_archivo.endswith('.txt'):

            with open(ruta_entrada, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()

            inicio_json = texto_completo.find("{")

            json_str = texto_completo[inicio_json:]

            fin_json = json_str.rfind("}") + 1

            json_str = json_str[:fin_json]

            try:
                json_data = json.loads(json_str)

                ruta_salida = os.path.join(carpeta_salida, f"{nombre_archivo[:-4]}.json")

                with open(ruta_salida, 'w', encoding='utf-8') as archivo_salida:
                    json.dump(json_data, archivo_salida, indent=2)

                print(f"\nResultado guardado en: {ruta_salida}\n")
            except json.decoder.JSONDecodeError as e:
                print(f"\nError al cargar el JSON en el archivo {nombre_archivo}: {e}\n")
                
                
                
                
#*********************** ELIMINA COMILLAS DOBLES
                
def eliminar_comillas_numeros_en_carpeta():
    ruta_carpeta = r'C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\json_calificacion_1'
    for nombre_archivo in os.listdir(ruta_carpeta):
        ruta_json = os.path.join(ruta_carpeta, nombre_archivo)

        if nombre_archivo.endswith('.json') and os.path.isfile(ruta_json):
            with open(ruta_json, 'r') as file:
                data = json.load(file)

            for key, value in data.items():
                if isinstance(value, str) and value.isdigit():
                    data[key] = int(value)

            with open(ruta_json, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
                
                
                
                

#*********************** COMPARACION DE LOS JSON
def comparacion():
    
    print("\nINICIANDO COMPARACION DE JSON\n")

    folder_path_json1 = r'C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\json_calificacion_1'
    folder_path_json2 = r'C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\json_calificacion_2'
    output_folder = r'C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\pov4'

    for filename in os.listdir(folder_path_json1):
        
        file_path_json1 = os.path.join(folder_path_json1, filename)
        file_path_json2 = os.path.join(folder_path_json2, "tabla_puntaje_json.json")

        try:
            
            with open(file_path_json1, 'r') as file:
                json1_str = file.read()

            with open(file_path_json2, 'r') as file:
                json2_str = file.read()

            json1 = json.loads(json1_str)
            json2 = json.loads(json2_str)

            for key, value in json1.items():
                if value == 1 or value == "1":
                    json1[key] = json2.get(key, value)
                
            suma_anterior = sum(json1[key] for key in json1 if key != "groserias" and key != "resultado" and key != "Manejo_de_Herramientas")
                    
            if "groserias" in json2:
                json1["resultado"] = suma_anterior


            output_file_path = os.path.join(output_folder, f"{filename}")

            with open(output_file_path, 'w') as output_file:
                json.dump(json1, output_file, indent=2)

            print(f"\nResultado para el archivo {filename} guardado en {output_file_path}\n")

        except FileNotFoundError as e:
            print(f"\nError: El archivo {filename} no se encuentra en ambas carpetas.\n")
        except json.JSONDecodeError as e:
            print(f"\nError al decodificar el JSON en el archivo {filename}: {e}\n")
            
            
# ********************** MANEJO DE TIEMPOS


def extraer_primer_numero():
    carpeta = r'C:\Users\Aero\Desktop\Proceso_Clidad\tiempos_espera'

    numeros = []

    for archivo in os.listdir(carpeta):

        ruta_archivo = os.path.join(carpeta, archivo)

        if os.path.isfile(ruta_archivo) and archivo.endswith('.txt'):
        
            with open(ruta_archivo, 'r') as f:
                for linea in f:
                    
                    match = re.search(r'\b(\d+(\.\d+)?)\b', linea)
                    if match:
                        
                        primer_numero = float(match.group(1))
                        numeros.append(primer_numero)

    if numeros:
        primer_numero_total = numeros[0]
        print("Primer número total:", primer_numero_total)
        return primer_numero_total
    else:
        print("No se encontraron números en los archivos de texto.")

def manejo_de_tiempos():
    
    valor_total_diferencia_minutos = extraer_primer_numero()
                
    umbral = 0.60
    
    if valor_total_diferencia_minutos > umbral:
        print("Excede mas de 0.60 segundos de espera")
        print(valor_total_diferencia_minutos)
        return 0
    else:
        print("Tiempos de espera totales menores a 0.60")
        print(valor_total_diferencia_minutos)
        return 10

def actualizar_valor_json(ruta_json, clave, nuevo_valor):
    with open(ruta_json, 'r') as archivo:
        datos = json.load(archivo)
        
    datos[clave] = nuevo_valor
    
    with open(ruta_json, 'w') as archivo:
        json.dump(datos, archivo, indent=2)


def manejo_info():
    carpeta_base = r"C:\Users\Aero\Desktop\Proceso_Clidad"
    carpeta_audios = os.path.join(carpeta_base, "audios")
    carpeta_calificacion = os.path.join(carpeta_base, "calificacion", "pov4")

    archivos_en_carpeta = os.listdir(carpeta_audios)

    for nombre_archivo in archivos_en_carpeta:
        ruta_completa = os.path.join(carpeta_audios, nombre_archivo)

        if "_sin_silencios" not in nombre_archivo and "_mejorado" not in nombre_archivo and "desktop.ini" not in nombre_archivo:
            
            # Obtener el nombre del archivo JSON dinámicamente
            nombre_json = os.path.splitext(nombre_archivo)[0] + ".json"
            ruta_json = os.path.join(carpeta_calificacion, nombre_json)

            resultado_umbral = manejo_de_tiempos()
            print(resultado_umbral)
            
            # Actualizar el valor en el archivo JSON
            actualizar_valor_json(ruta_json, "Atiende_la_llamada", resultado_umbral)







#*********************** ELIMINA FORMATO JSON Y DEJA SOLO TABLA DE CALIFICACIONES

def eliminar_json():
    archivo_a_analizar = r"C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\pov1"

    carpeta_salida = r"C:\Users\Aero\Desktop\Proceso_Clidad\contextos_calidad"
    
    for nombre_archivo in os.listdir(archivo_a_analizar):
        ruta_entrada = os.path.join(archivo_a_analizar, nombre_archivo)
        if os.path.isfile(ruta_entrada) and nombre_archivo.endswith('.txt'):

            with open(ruta_entrada, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()

            inicio = texto_completo.find('{')
            fin = texto_completo.rfind('}')

            if inicio != -1 and fin != -1:
                texto_completo = texto_completo[:inicio] + texto_completo[fin + 1:]
                
            inicio1 = texto_completo.find('```json')
            fin1 = texto_completo.rfind('```')

            if inicio1 != -1 and fin1 != -1:
                texto_completo = texto_completo[:inicio1] + texto_completo[fin1 + 1:]

            try:
                # Corregir la línea siguiente
                output_file = os.path.join(carpeta_salida, os.path.basename(ruta_entrada))
                with open(output_file, 'w') as file:
                    file.write(texto_completo)

                print(f"Se ha eliminado el texto entre las llaves y el resultado se ha guardado en: {output_file}")
            
            except traceback as e:
                print(f"\nError al obtener el archivo: {e}\n")



            
#*********************** CARGA DE CALIFICACIONES A LA BASE DE DATOS

def archivo_ya_subido(cursor, guia, file_name):
    # Verifica si el archivo ya existe en la base de datos
    consulta_existencia = f"SELECT COUNT(*) FROM calificaciones_{guia} WHERE filename = '{file_name}'"
    cursor.execute(consulta_existencia)
    resultado = cursor.fetchone()[0]
    return resultado > 0

def cargar_calificaciones_en_mysql(guia):
    print(f"\nINICIO DE SUBIDA DE BASE DE DATOS {guia}\n")

    conn = mysql.connector.connect(
        host='192.168.51.210',
        user='root',
        password='',
        database='audios_dana'
    )

    cursor = conn.cursor()

    json_folder = r'C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\pov4'

    for filename in os.listdir(json_folder):
        file_path = os.path.join(json_folder, filename)

        try:    
            
            with open(file_path, 'r') as file:
                json_str = file.read()

            json_data = json.loads(json_str)

            file_name_without_extension, _ = os.path.splitext(filename)

            json_data['filename'] = file_name_without_extension + '.mp3'
            
            if archivo_ya_subido(cursor, guia, json_data['filename']):
                print(f"\nEl archivo {filename} ya ha sido subido a la tabla {guia}.\n")
                continue

            cursor.execute(f"SHOW COLUMNS FROM calificaciones_{guia}")
            column_names = [column[0] for column in cursor.fetchall()]

            sql_query = f'''
                INSERT INTO calificaciones_{guia} ({', '.join(column_names)})
                VALUES ({', '.join(['%s']*len(column_names))})
            '''
            

            values = [json_data.get(column, None) for column in column_names]

            cursor.execute(sql_query, values)

            conn.commit()

            print(f"\nValores de {filename} insertados en la base de datos calificaciones_{guia}.\n")

        except FileNotFoundError as e:
            print(f"\nError: El archivo {filename} no se encuentra en la carpeta.\n")
        except json.JSONDecodeError as e:
            print(f"\nError al decodificar el JSON en el archivo {filename}: {e}\n")
        except mysql.connector.Error as e:
            print(f"\nError de MySQL: {e}\n")
        except KeyError as e:
            print(f"\nError: {e}\n")

    cursor.close()
    conn.close()

    conn = mysql.connector.connect(
        host='192.168.51.210',
        user='root',
        password='',
        database='audios_dana'
    )
    cursor = conn.cursor()

    update_query = "UPDATE audios SET status = 'Calificando' WHERE status = 'Transcribiendo'"
    cursor.execute(update_query)
    conn.commit()

    file_name_with_extension = file_name_without_extension + '.mp3'
    owner = obtener_owner(file_name_with_extension)

    if owner:
        consulta = f"UPDATE calificaciones_{guia} SET owner = '{owner}' WHERE filename = '{file_name_with_extension}'"
        cursor.execute(consulta)
        conn.commit()

    cursor.close()
    conn.close()

def obtener_owner(audio_name):
    
    conn = mysql.connector.connect(
        host='192.168.51.210',
        user='root',
        password='',
        database='audios_dana'
    )
    cursor = conn.cursor()

    consulta = f"SELECT owner FROM audios WHERE audio_name = '{audio_name}'"
    cursor.execute(consulta)
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        owner = resultado[0]
        return owner
    else:
        return None

def main_calificaciones(guia):
    guia_set(guia)
    extraccion(guia)
    extraccion_1()
    extraccion_2()
    eliminar_comillas_numeros_en_carpeta()
    comparacion()
    manejo_info()
    eliminar_json()
    cargar_calificaciones_en_mysql(guia)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        guia = sys.argv[1]
        main_calificaciones(guia)
    else:
        print("Por favor, proporciona el nombre del archivo como argumento de línea de comandos.")
    
    print("═"*30, " Calificacion terminada con exito ", "═"*30)
    
    
    


        