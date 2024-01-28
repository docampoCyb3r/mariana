print("\n--------- INICIA CARGA MASIVA DE BASE DE DATOS ---------\n")

import sys

def carga_de_base(guia):
    
    # ****************************** TABLA PRUEBA_DANA_CALIDAD
    import os
    import mysql.connector
    
    def guardar_transcripcion(filename, emociones):
        conexion = mysql.connector.connect(
            host = "192.168.51.210",
            user = "root",
            password = "",
            database = "audios_dana"
        )

        cursor = conexion.cursor()

        
        consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            
            consulta = "UPDATE prueba_dana_calidad SET transcripcion = %s WHERE filename = %s"
            valores = (emociones, filename)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            
            consulta = "INSERT INTO prueba_dana_calidad (filename, transcripcion) VALUES (%s, %s)"
            valores = (filename, emociones)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido agregado a la base de datos.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":
    
        carpeta_transcripciones = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion1'

        archivos_emociones = [f for f in os.listdir(carpeta_transcripciones) if f.endswith('.txt')]

        for archivo in archivos_emociones:
            ruta_archivo = os.path.join(carpeta_transcripciones, archivo)

            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                emociones = file.read()

            guardar_transcripcion(filename, emociones)



    #**************************************************************

    #BASE DE DATOS EMOCIONES
    import os
    import mysql.connector

    def guardar_emociones(filename, emociones):
        conexion = mysql.connector.connect(
            host = "192.168.51.210",
            user = "root",
            password = "",
            database = "audios_dana"
        )

        cursor = conexion.cursor()
        
        consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            consulta = "UPDATE prueba_dana_calidad SET emociones = %s WHERE filename = %s"
            valores = (emociones, filename)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            consulta = "INSERT INTO prueba_dana_calidad (filename, emociones) VALUES (%s, %s)"
            valores = (filename, emociones)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido agregado a la base de datos.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":

        carpeta_emociones = r'C:\Users\Aero\Desktop\Proceso_Clidad\resultados_emociones'

        archivos_emociones = [f for f in os.listdir(carpeta_emociones) if f.endswith('.txt')]

        for archivo in archivos_emociones:
            ruta_archivo = os.path.join(carpeta_emociones, archivo)

            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r') as file:
                emociones = file.read()

            guardar_emociones(filename, emociones)

    #************************************ BASE DE DATOS CHAT
    import os
    import mysql.connector

    def guardar_chat(filename, chat):
        conexion = mysql.connector.connect(
            host = "192.168.51.210",
            user = "root",
            password = "",
            database = "audios_dana"
        )

        cursor = conexion.cursor()

        consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            
            consulta = "UPDATE prueba_dana_calidad SET chat = %s WHERE filename = %s"
            valores = (chat, filename)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            
            consulta = "INSERT INTO prueba_dana_calidad (filename, chat) VALUES (%s, %s)"
            valores = (filename, chat)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido agregado a la base de datos.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":
        
        carpeta_chat = r'C:\Users\Aero\Desktop\Proceso_Clidad\chat'

        archivos_chat = [f for f in os.listdir(carpeta_chat) if f.endswith('.txt')]

        for archivo in archivos_chat:
            ruta_archivo = os.path.join(carpeta_chat, archivo)
            
            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                chat = file.read()

            guardar_chat(filename, chat)
            
    #************************************ BASE TRANSCRIPCION ORIGINAL
    import os
    import mysql.connector

    def guardar_trans(filename, tra):
        conexion = mysql.connector.connect(
            host = "192.168.51.210",
            user = "root",
            password = "",
            database = "audios_dana"
        )

        cursor = conexion.cursor()

        
        consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            
            consulta = "UPDATE prueba_dana_calidad SET transcripcion_original = %s WHERE filename = %s"
            valores = (tra, filename)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            
            consulta = "INSERT INTO prueba_dana_calidad (filename, transcripcion_original) VALUES (%s, %s)"
            valores = (filename, tra)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido agregado a la base de datos.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":
    
        carpeta_tra = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'

        archivos_tra = [f for f in os.listdir(carpeta_tra) if f.endswith('.txt')]

        for archivo in archivos_tra:
            ruta_archivo = os.path.join(carpeta_tra, archivo)

            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                tra = file.read()

            guardar_trans(filename, tra)
    
    # ************************************ BASE EMOCIONES POR SEPARADO
    
    def guardar_resumen():
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="",
            database="audios_dana"
        )

        cursor = conexion.cursor()

        carpeta_local = r"C:\Users\Aero\Desktop\Proceso_Clidad\resultados_emociones"

        try:
            
            cursor = conexion.cursor()

            for archivo in os.listdir(carpeta_local):
                if archivo.endswith(".txt"):
                    ruta_archivo = os.path.join(carpeta_local, archivo)

                    with open(ruta_archivo, "r") as file:
                        contenido = file.read()

                    nombre_archivo = os.path.splitext(archivo)[0] + ".mp3"
                    negatividad = float(contenido.split("Puntuación de negatividad: ")[1].split("\n")[0])
                    neutralidad = float(contenido.split("Puntuación de neutralidad: ")[1].split("\n")[0])
                    positividad = float(contenido.split("Puntuación de positividad: ")[1].split("\n")[0])
                    puntuacion_total = float(contenido.split("Puntuación de sentimiento general: ")[1].split("\n")[0])

                    consulta = "UPDATE prueba_dana_calidad SET Negatividad = %s, Neutralidad = %s, Positividad = %s, Puntuacion_general_sentimientos = %s WHERE filename = %s"
                    valores = (negatividad, neutralidad, positividad, puntuacion_total, f"{nombre_archivo}")

                    cursor.execute(consulta, valores)

                    conexion.commit()

        except mysql.connector.Error as error:
            print(f"Error: {error}")

        finally:

            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()
                print("Conexión cerrada.")


    if __name__ == "__main__":
        guardar_resumen()

    # ************************************ TABLA CONTEXTOS_CALIDAD

    #************************************* BASE DE DATOS PARA SUBIR RESUMEN
    import os
    import os.path
    import mysql.connector

    def guardar_resumen():
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="",
            database="audios_dana"
        )

        cursor = conexion.cursor()

        ruta_resumen = r'C:\Users\Aero\Desktop\Proceso_Clidad\resumen_llamada'

        archivos_resumen = os.listdir(ruta_resumen)

        cursor.execute("SELECT filename FROM contextos_calidad")
        nombres_archivo_existente = [registro[0] for registro in cursor.fetchall()]

        for archivo in archivos_resumen:
            ruta_archivo = os.path.join(ruta_resumen, archivo)  

            nombre_archivo = os.path.splitext(archivo)[0] + ".mp3"
            
            consulta_existente = "SELECT filename FROM contextos_calidad WHERE filename = %s"
            cursor.execute(consulta_existente, (nombre_archivo,))
            resultado = cursor.fetchone()

            if nombre_archivo in nombres_archivo_existente:
                print(f"El archivo {nombre_archivo} ya fue subido. Saltando...")
                continue

            with open(ruta_archivo, "r", encoding='utf-8') as archivo_txt:
                linea = archivo_txt.read().strip()

            consulta = "INSERT INTO contextos_calidad (filename, resumen_llamada) VALUES (%s, %s)"
            valores = (nombre_archivo, linea)
            cursor.execute(consulta, valores)

        conexion.commit()

        cursor.close()
        conexion.close()


    if __name__ == "__main__":
        guardar_resumen()


    #************************************* BASE DE DATOS PARA SUBIR CONTEXO GENERAL


    import os
    import mysql.connector

    def actualizar_contexto(filename, contexto_general):
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="",
            database="audios_dana"
        )

        cursor = conexion.cursor()

        consulta_existencia = "SELECT COUNT(*) FROM contextos_calidad WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            consulta = "UPDATE contextos_calidad SET contexto_general = %s WHERE filename = %s"
            valores = (contexto_general, filename)
            cursor.execute(consulta, valores)
            print("El contexto general del archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            print("El archivo {} no existe en la base de datos. No se puede actualizar.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":
        carpeta_calificaciones = r'C:\Users\Aero\Desktop\Proceso_Clidad\contextos_calidad'
        archivos_calificaciones = [f for f in os.listdir(carpeta_calificaciones) if f.endswith('.txt')]

        for archivo in archivos_calificaciones:
            ruta_archivo = os.path.join(carpeta_calificaciones, archivo)
            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r', encoding='latin-1') as file:
                contexto_general = file.read()

            actualizar_contexto(filename, contexto_general)
            
    # ******************** subida de status de groseria ***************

    print("Iniciando subida de valor de palabra antisonante")
    import os
    import mysql.connector

    def actualizar_contextos(filename, groserias):
            conexion = mysql.connector.connect(
                host="192.168.51.210",
                user="root",
                password="",
                database="audios_dana"
            )

            cursor = conexion.cursor()

            consulta_existencia = "SELECT COUNT(*) FROM audios WHERE audio_name = %s"
            cursor.execute(consulta_existencia, (filename,))
            resultado = cursor.fetchone()

            if resultado[0] > 0:
                consulta = "UPDATE audios SET groserias = %s WHERE audio_name = %s"
                valores = (groserias, filename)
                cursor.execute(consulta, valores)
                print("El contexto general del archivo {} ha sido actualizado en la base de datos.".format(filename))
            else:
                print("El archivo {} no existe en la base de datos. No se puede actualizar.".format(filename))

            conexion.commit()
            cursor.close()
            conexion.close()

    if __name__ == "__main__":
            carpeta_groseria = r'C:\Users\Aero\Desktop\Proceso_Clidad\groserias'
            archivos_gros = [f for f in os.listdir(carpeta_groseria) if f.endswith('.txt')]

            for archivo in archivos_gros:
                ruta_archivo = os.path.join(carpeta_groseria, archivo)
                
                filename = os.path.splitext(archivo)[0] + ".mp3"

                with open(ruta_archivo, 'r', encoding='utf-8') as file:
                    contexto_groseria = file.read()

                if '*' in contexto_groseria:
                    valor_groserias = 1
                else:
                    valor_groserias = 0
                    
                actualizar_contextos(filename, valor_groserias)




    #************************************************************** estatus a completado

    import mysql.connector
    import os

    def actualizar_estado(conexion):
        cursor = conexion.cursor()

        cursor.execute("SELECT audio_name, status FROM audios")
        registros_audios = cursor.fetchall()

        nombres_archivo_existente = {registro[0]: registro[1] for registro in registros_audios}

        carpeta_transcripcion = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'

        for archivo in os.listdir(carpeta_transcripcion):
            nombre_archivo = os.path.splitext(archivo)[0] + ".mp3"

            if nombre_archivo in nombres_archivo_existente:
                estado_actual = nombres_archivo_existente[nombre_archivo]
                if estado_actual != 'Audio de baja calidad':
                    consulta = "UPDATE audios SET analyzed = 1, status = 'Completado' WHERE audio_name = %s"
                    cursor.execute(consulta, (nombre_archivo,))

        conexion.commit()
        cursor.close()

    conexion = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="",
        database="audios_dana"
    )

    actualizar_estado(conexion)
    conexion.close()


        # *********************** BASE DE DATOS PROBLEMATICA ************************

    import os
    import mysql.connector

    def actualizar_contexto(filename, problema):
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="",
            database="audios_dana"
        )

        cursor = conexion.cursor()

        consulta_existencia = "SELECT COUNT(*) FROM audios WHERE audio_name = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            
            consulta = "UPDATE audios SET problematica = %s WHERE audio_name = %s"
            valores = (problema, filename)
            cursor.execute(consulta, valores)
            print("El problema del archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            print("El archivo {} no existe en la base de datos. No se puede actualizar.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":
        carpeta_problematica = r'C:\Users\Aero\Desktop\Proceso_Clidad\problematica'
        archivos_problematica = [f for f in os.listdir(carpeta_problematica) if f.endswith('.txt')]

        for archivo in archivos_problematica:
            ruta_archivo = os.path.join(carpeta_problematica, archivo)
            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                problema = file.read()

            actualizar_contexto(filename, problema)
            
    # *********************** BASE DE DATOS SOLUCION ************************

    import os
    import mysql.connector

    def actualizar_contexto(filename, solucion):
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="",
            database="audios_dana"
        )

        cursor = conexion.cursor()

        consulta_existencia = "SELECT COUNT(*) FROM audios WHERE audio_name = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            
            consulta = "UPDATE audios SET solucion = %s WHERE audio_name = %s"
            valores = (solucion, filename)
            cursor.execute(consulta, valores)
            print("La solucion del archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            print("El archivo {} no existe en la base de datos. No se puede actualizar.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":
        carpeta_solucion = r'C:\Users\Aero\Desktop\Proceso_Clidad\solucion'
        archivos_solucion = [f for f in os.listdir(carpeta_solucion) if f.endswith('.txt')]

        for archivo in archivos_solucion:
            ruta_archivo = os.path.join(carpeta_solucion, archivo)
            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                solucion = file.read()

            actualizar_contexto(filename, solucion)

    # *********************** BASE DE DATOS PROBLEMATICA calificaciones ************************

    import os
    import mysql.connector

    def actualizar_contexto(filename, problema, guia):
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="",
            database="audios_dana"
        )

        cursor = conexion.cursor()
        
        consulta_existencia = f"SELECT COUNT(*) FROM calificaciones_{guia} WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
        
            consulta = f"UPDATE calificaciones_{guia} SET problematica = %s WHERE filename = %s"
            valores = (problema, filename)
            cursor.execute(consulta, valores)
            print(f"El problema del archivo {filename} ha sido actualizado en la base de datos calificaciones_{guia}.")
        else:
            print(f"El archivo {filename} no existe en la base de datos. No se puede actualizar.")

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":
        carpeta_problematica = r'C:\Users\Aero\Desktop\Proceso_Clidad\problematica'
        archivos_problematica = [f for f in os.listdir(carpeta_problematica) if f.endswith('.txt')]

        for archivo in archivos_problematica:
            ruta_archivo = os.path.join(carpeta_problematica, archivo)
            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                problema = file.read()

            actualizar_contexto(filename, problema, guia)
            
    # *********************** BASE DE DATOS SOLUCION calificaciones************************

    import os
    import mysql.connector

    def actualizar_solucion(filename, solucion, guia):
        print("Subiendo solucion")
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="",
            database="audios_dana"
        )

        cursor = conexion.cursor()
        
        consulta_existencia = f"SELECT COUNT(*) FROM calificaciones_{guia} WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            
            consulta = f"UPDATE calificaciones_{guia} SET solucion = %s WHERE filename = %s"
            valores = (solucion, filename)
            cursor.execute(consulta, valores)
            print(f"La solucion del archivo {filename} ha sido actualizada en la base de datos calificaciones_{guia}")
        else:
            print(f"El archivo {filename} no existe en la base de datos. No se puede actualizar.")

        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar_punto_de_vista(filename, punto_de_vista, guia):
        print("Subiendo punto de vista")
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="",
            database="audios_dana"
        )

        cursor = conexion.cursor()

        consulta_existencia = f"SELECT COUNT(*) FROM calificaciones_{guia} WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            consulta = f"UPDATE calificaciones_{guia} SET punto_de_vista = %s WHERE filename = %s"
            valores = (punto_de_vista, filename)
            cursor.execute(consulta, valores)
            print(f"El punto de vista del archivo {filename} ha sido actualizado en la base de datos calificaciones_{guia}")
        else:
            print(f"El archivo {filename} no existe en la base de datos. No se puede actualizar.")

        conexion.commit()
        cursor.close()
        conexion.close()

    if __name__ == "__main__":
        carpeta_solucion = r'C:\Users\Aero\Desktop\Proceso_Clidad\solucion'
        archivos_solucion = [f for f in os.listdir(carpeta_solucion) if f.endswith('.txt')]

        for archivo in archivos_solucion:
            ruta_archivo_solucion = os.path.join(carpeta_solucion, archivo)
            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo_solucion, 'r', encoding='utf-8') as file:
                solucion = file.read()

            actualizar_solucion(filename, solucion, guia)

        carpeta_pov = r'C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\pov1'
        archivos_pov = [f for f in os.listdir(carpeta_pov) if f.endswith('.txt')]

        for archivo in archivos_pov:
            ruta_archivo_pov = os.path.join(carpeta_pov, archivo)
            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo_pov, 'r', encoding='utf-8') as file:
                punto_de_vista = file.read()

            actualizar_punto_de_vista(filename, punto_de_vista, guia)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        guia = sys.argv[1]
        carga_de_base(guia)
    else:
        print("Por favor, proporciona el nombre del archivo como argumento de línea de comandos.")
    
    print("═"*30, " CARGA DE BASE DE DATOS MASIVA FINALIZADA CON EXITO ", "═"*30)
    