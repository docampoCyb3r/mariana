print("\n--------- INICIANDO PROCESO DE CARGA DE RESULTADO DE CALIFICACIONES ---------\n")

import mysql.connector
import os
import sys

# Obtiene los valores de la tabla de guia
def obtener_valores(guia):
    config = {
        'user': 'root',
        'password': '',
        'host': '192.168.51.210',
        'database': 'audios_dana',
    }

    conexion = mysql.connector.connect(**config)

    cursor = conexion.cursor()

    tabla = f'{guia}'
    columnas = ['id_subcategoria', 'nombre_punto']

    consulta = f"SELECT {', '.join(columnas)} FROM {tabla} WHERE nombre_punto <> 'Manejo de Herramientas' and nombre_punto <> 'groserias';"

    cursor.execute(consulta)

    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()
    return resultados


#obtiene el valor de las calificaciones
def obtener_fila_por_nombre(guia):
    config = {
        'user': 'root',
        'password': '',
        'host': '192.168.51.210',
        'database': 'audios_dana',
    }

    conexion = mysql.connector.connect(**config)

    cursor = conexion.cursor()

    tabla = f'calificaciones_{guia}'
    nombre_columna = 'filename'
    carpeta_transcripciones = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'

    archivo_Calificaciones = [f for f in os.listdir(carpeta_transcripciones) if f.endswith('.txt')]

    for archivo in archivo_Calificaciones:
        ruta_archivo = os.path.join(carpeta_transcripciones, archivo)

        filename = os.path.splitext(archivo)[0] + ".mp3"
            
            
    columnas_excluir = ['id_audio', 'filename', 'groserias', 'resultado', 'owner', 'tipo', 'problematica', 'solucion', 'punto_de_vista', 'solucion_prob']

    columnas = [columna for columna in obtener_nombres_columnas(cursor, tabla) if columna not in columnas_excluir]

    consulta = f"SELECT {', '.join(columnas)} FROM {tabla} WHERE {nombre_columna} = %s"

    cursor.execute(consulta, (filename,))

    resultados_fila = cursor.fetchall()

    if resultados_fila:
        print(f"\nValores de la fila con {nombre_columna} = '{filename}':")
        for resultado in resultados_fila:
            print(resultado)
    else:
        print(f"No se encontró ninguna fila con {nombre_columna} = '{filename}'")

    cursor.close()
    conexion.close()
    return resultados_fila



#obtiene el nombre de las columnas 
def obtener_nombres_columnas(cursor, tabla):
    consulta = f"SHOW COLUMNS FROM {tabla}"
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    return [resultado[0] for resultado in resultados]


#obtiene el inicio de la suma

def obtener_sumas(resultados_emparejados):
    sumas = {}
    
    for resultado in resultados_emparejados:
        clave = resultado[0]
        valor = resultado[2]

        if clave not in sumas:
            sumas[clave] = []

        sumas[clave].append(valor)
    
    return sumas


#obtiene el total de la suma
# def imprimir_resultados_emparejados(resultados_emparejados):
#     sumas = obtener_sumas(resultados_emparejados)
#     suma_cali = 0.0
#     diez = 10.0
#     cinco = 5.0
    
#     suma_actual = None
#     for resultado in resultados_emparejados:
#         if suma_actual is None or suma_actual[0] != resultado[0]:
#             if suma_actual is not None:
#                 if any(val == 0 for val in sumas[suma_actual[0]]):
#                     print(f"suma = 0.0\n")
#                 else:
#                     suma = sum(sumas[suma_actual[0]])
#                     if suma > 0:
#                         if suma_actual[0] == '8' and all(val > 0 for val in sumas[suma_actual[0]]):
#                             print(f"suma = {cinco}\n")
#                             suma_cali += 5
#                         else:
#                             suma_cali += 10
#                             print(f"suma = {diez}\n")
                    
#             suma_actual = (resultado[0], sumas[resultado[0]])
#         else:
#             suma_actual[1].append(resultado[2])
            
#         if resultado != ('0', 'groserias', 1):
#             print(resultado)

#     return suma_cali

def imprimir_resultados_emparejados(resultados_emparejados):
    sumas = obtener_sumas(resultados_emparejados)
    suma_cali = 0.0
    diez = 10.0
    cinco = 5.0
    
    for clave, valores in sumas.items():
        if any(val == 0 for val in valores):
            print(f"suma para clave {clave} = 0.0\n")
        else:
            if clave == '8' and all(val > 0 for val in valores):
                print(f"suma para clave {clave} = {cinco}\n")
                suma_cali += 5
            elif clave != '10':
                suma_cali += 10
                print(f"suma para clave {clave} = {diez}\n")
    
    suma_cali = suma_cali + 15
          
    return suma_cali


#actualiza el valor de la calificacion por medio del nombre de la columna
def actualizar_resultado(resultado, valor_columna, guia):
    config = {
        'user': 'root',
        'password': '',
        'host': '192.168.51.210',
        'database': 'audios_dana',
    }

    conexion = mysql.connector.connect(**config)

    cursor = conexion.cursor()

    tabla = f'calificaciones_{guia}'
    columna_resultado = 'resultado'
    nombre_columna = 'filename'

    consulta = f"UPDATE {tabla} SET {columna_resultado} = %s WHERE {nombre_columna} = %s"
    cursor.execute(consulta, (resultado, valor_columna))

    conexion.commit()

    cursor.close()
    conexion.close()


def main(guia):
    resultados_valores = obtener_valores(guia)
    resultados_fila = obtener_fila_por_nombre(guia)

    if resultados_fila:
        resultados_emparejados = [(str(valores[0]), str(valores[1]), resultados_fila[0][i]) for i, valores in enumerate(resultados_valores)]
        
        print("Resultados emparejados:")
        suma_cali = imprimir_resultados_emparejados(resultados_emparejados)

        carpeta_transcripciones = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'
        archivo_Calificaciones = [f for f in os.listdir(carpeta_transcripciones) if f.endswith('.txt')]

        for archivo in archivo_Calificaciones:
            ruta_archivo = os.path.join(carpeta_transcripciones, archivo)
            filename = os.path.splitext(archivo)[0] + ".mp3"
            
            actualizar_resultado(suma_cali, filename, guia)

        print(f"Suma total de calificaciones: {suma_cali}")
    else:
        print(f"No se encontró ninguna fila para el archivo en la base de datos.")

  

if __name__ == "__main__":
    if len(sys.argv) > 1:
        guia = sys.argv[1]
        main(guia)
    else:
        print("Por favor, proporciona el nombre del archivo como argumento de línea de comandos.")
    
    print("═"*30, " Calificacion terminada con exito ", "═"*30)
    
    