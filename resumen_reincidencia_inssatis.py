print("\n--------- INICIA CARGA DE REINCIDENCIA RESUMEN E INSATISFACION ---------\n")

import openai
import os
import re
import mysql.connector

conexion = mysql.connector.connect(
    host = "192.168.51.210",
    user = "root",
    password = "",
    database = "audios_dana"
)

cursor = conexion.cursor()


# funcion de ia
def hacer_pregunta(fragmento_texto):
    openai.api_key = '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'
    completion = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "Eres un analista de calidad con mas de 30 años de experiencia y se te a encomentado analizar el siguiente texto"},
            {"role": "user", "content": fragmento_texto}
        ]
    )
    respuesta = completion.choices[0].message.content
    return respuesta

# validacion de reincidencia

def reincidencia():
    carpeta_archivos = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'
    carpeta_data = r'C:\Users\Aero\Desktop\Proceso_Clidad\reincidencia'

    archivos_a_analizar = [archivo for archivo in os.listdir(carpeta_archivos) if archivo.endswith(('.txt', '.doc', '.docx'))]

    for archivo in archivos_a_analizar:
            ruta_archivo = os.path.join(carpeta_archivos, archivo)
            ruta_resultado = os.path.join(carpeta_data, archivo)

            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()
                
            pregunta = f"""Necestio que me indiques si durante la conversacion se llega a detectar una reincidencia u omicion a la peticion del cliente, si se detecta reincidencia dale el valor de 1, sino dale el valor de 0 
                        ejemplo 
                        Valor asignado: 
                        
                        {texto_completo}"""
            respuesta = hacer_pregunta(pregunta)
            
            with open(ruta_resultado, 'w', encoding='utf-8') as archivo:
                archivo.write(respuesta)

            print(f"\nTranscripción del archivo '{archivo}' guardada en '{ruta_resultado}'\n")
    
    patron = r'(\b1\b|\b0\b)'
    resultado = re.search(patron, respuesta)
    
    if resultado:
        valor_reincidencia = resultado.group(0)
        print("El valor de reinsidencia del cliente es:", valor_reincidencia)
    else:
        print("No se encontró ninguna indicación de satisfacción del cliente en el texto.")
    
    carpeta_calificaciones = r'C:\Users\Aero\Desktop\Proceso_Clidad\reincidencia'
    archivos_calificaciones = [f for f in os.listdir(carpeta_calificaciones) if f.endswith('.txt')]
    
    conexion = mysql.connector.connect(
        host = "192.168.51.210",
        user = "root",
        password = "",
        database = "audios_dana"
    )

    cursor = conexion.cursor()

    for archivo in archivos_calificaciones:
        ruta_archivo = os.path.join(carpeta_calificaciones, archivo)
        filename = os.path.splitext(archivo)[0] + ".mp3"
    
    consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
    cursor.execute(consulta_existencia, (filename,))
    resultado_base = cursor.fetchone()

    if resultado_base[0] > 0:
        consulta = "UPDATE prueba_dana_calidad SET Reinsidencia = %s WHERE filename = %s"
        valores = (valor_reincidencia, filename)
        cursor.execute(consulta, valores)
        print("La reincidencia del archivo {} ha sido actualizado en la base de datos.".format(filename))
    else:
        print("El archivo {} no existe en la base de datos. No se puede actualizar.".format(filename))
    
    conexion.commit()
    cursor.close()
    conexion.close()


# resumen de llamada 2 renglones
def resumen_dos():
    carpeta_archivos = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'
    carpeta_data = r'C:\Users\Aero\Desktop\Proceso_Clidad\resumen_corto'

    archivos_a_analizar = [archivo for archivo in os.listdir(carpeta_archivos) if archivo.endswith(('.txt', '.doc', '.docx'))]

    for archivo in archivos_a_analizar:
            ruta_archivo = os.path.join(carpeta_archivos, archivo)
            ruta_resultado = os.path.join(carpeta_data, archivo)

            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()
                
            pregunta = f"Necestio que me des un resumen de la conversacion usando solo 2 renglones: {texto_completo}"
            respuesta = hacer_pregunta(pregunta)
            
            with open(ruta_resultado, 'w', encoding='utf-8') as archivo:
                archivo.write(respuesta)

            print(f"\nTranscripción del archivo '{archivo}' guardada en '{ruta_resultado}'\n")
            
    carpeta_calificaciones = r'C:\Users\Aero\Desktop\Proceso_Clidad\resumen_corto'
    archivos_calificaciones = [f for f in os.listdir(carpeta_calificaciones) if f.endswith('.txt')]
    
    conexion = mysql.connector.connect(
        host = "192.168.51.210",
        user = "root",
        password = "",
        database = "audios_dana"
    )

    cursor = conexion.cursor()

    for archivo in archivos_calificaciones:
        ruta_archivo = os.path.join(carpeta_calificaciones, archivo)
        filename = os.path.splitext(archivo)[0] + ".mp3"

        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            contexto_general = file.read()
    
    consulta_existencia = "SELECT COUNT(*) FROM contextos_calidad WHERE filename = %s"
    cursor.execute(consulta_existencia, (filename,))
    resultado_base = cursor.fetchone()

    if resultado_base[0] > 0:
        consulta = "UPDATE contextos_calidad SET resumen = %s WHERE filename = %s"
        valores = (contexto_general, filename)
        cursor.execute(consulta, valores)
        print("El resumen corto del archivo {} ha sido actualizado en la base de datos.".format(filename))
    else:
        print("El archivo {} no existe en la base de datos. No se puede actualizar.".format(filename))
    
    conexion.commit()
    cursor.close()
    conexion.close()

    

# validacion de cliente insatisfecho
def cliente_insatisfecho():
    carpeta_archivos = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'
    carpeta_data = r'C:\Users\Aero\Desktop\Proceso_Clidad\cliente_insatisfecho'

    archivos_a_analizar = [archivo for archivo in os.listdir(carpeta_archivos) if archivo.endswith(('.txt', '.doc', '.docx'))]

    for archivo in archivos_a_analizar:
            ruta_archivo = os.path.join(carpeta_archivos, archivo)
            ruta_resultado = os.path.join(carpeta_data, archivo)

            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()
                
            pregunta = f"""Necestio que me indiques la satisfaccion del cliente, si fue insatisfactorio dame el valor de 0, si fue satisfactorio dame el valor de 1
                            ejemplo 
                        Valor asignado: 
                        : {texto_completo}"""
            respuesta = hacer_pregunta(pregunta)
            
            with open(ruta_resultado, 'w', encoding='utf-8') as archivo:
                archivo.write(respuesta)

            print(f"\nTranscripción del archivo '{archivo}' guardada en '{ruta_resultado}'\n")

    patron = r'(\b1\b|\b0\b)'
    resultado = re.search(patron, respuesta)
    
    if resultado:
        valor_satisfaccion = resultado.group(0)
        print("El valor de satisfacción del cliente es:", valor_satisfaccion)
    else:
        print("No se encontró ninguna indicación de satisfacción del cliente en el texto.")
    
    carpeta_calificaciones = r'C:\Users\Aero\Desktop\Proceso_Clidad\cliente_insatisfecho'
    archivos_calificaciones = [f for f in os.listdir(carpeta_calificaciones) if f.endswith('.txt')]
    
    conexion = mysql.connector.connect(
        host = "192.168.51.210",
        user = "root",
        password = "",
        database = "audios_dana"
    )

    cursor = conexion.cursor()

    for archivo in archivos_calificaciones:
        ruta_archivo = os.path.join(carpeta_calificaciones, archivo)
        filename = os.path.splitext(archivo)[0] + ".mp3"
    
    consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
    cursor.execute(consulta_existencia, (filename,))
    resultado_base = cursor.fetchone()

    if resultado_base[0] > 0:
        consulta = "UPDATE prueba_dana_calidad SET Cliente_insatisfecho = %s WHERE filename = %s"
        valores = (valor_satisfaccion, filename)
        cursor.execute(consulta, valores)
        print("La insatisfaccion del archivo {} ha sido actualizado en la base de datos.".format(filename))
    else:
        print("El archivo {} no existe en la base de datos. No se puede actualizar.".format(filename))
        
    conexion.commit()
    cursor.close()
    conexion.close()




if __name__ == "__main__":
    reincidencia()
    resumen_dos()
    cliente_insatisfecho()
    print("\n--------- FINALIZA CARGA DE REINCIDENCIA RESUMEN E INSATISFACION ---------\n")
    
    
