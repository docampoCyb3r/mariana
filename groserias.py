import os
import time
import openai


groserias1 = []

print("\n--------- INICIANDO VALIDACION DE GROSERIAS ---------\n")

os.environ['_BARD_API_KEY'] = "ZwgPHedHl-k0bi_Mf14Pk1DkPL3q_clMUyzbxw3kLcBYpijm_4o13p3KvTwnTTfEZhcF_Q."

carpeta_archivos = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'

def hacer_pregunta(texto):
      openai.api_key = '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'
      completion = openai.chat.completions.create(
         model="gpt-4-1106-preview",
         messages=[
               {"role": "system", "content": "Eres un experto en análisis de calidad de call center con una experiencia de 30 años en el campo. Se te ha encomendado analizar el siguiente texto."},
               {"role": "user", "content": texto}
         ]
      )
      respuesta1 = completion.choices[0].message.content
      return respuesta1

archivos_a_analizar = [archivo for archivo in os.listdir(carpeta_archivos) if archivo.endswith(('.txt', '.doc', '.docx'))]

for archivo in archivos_a_analizar:
    ruta_archivo = os.path.join(carpeta_archivos, archivo)

    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        texto_completo = archivo.read()
    
    pregunta = f"""Identifica las palabras inapropiadas, vulgares o altisonantes dentro del texto: {texto_completo}. si NO encuentras palabras inapropiadas, vulgares o altisonantes dentro del texto manda un mensaje de 'No se encontraron palabras altisonantes durante la conversación' . Esto ayudará a que el proceso de filtrado sea más preciso."""

    # Almacenar la respuesta en una variable en lugar de escribir en un archivo
    respuesta = hacer_pregunta(pregunta)
    
    print(respuesta)
    

    print(f"Resultado obtenido para el archivo '{archivo}':")
    
    
def groserias():
            carpeta_archivos = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'
            carpeta_groserias = r"C:\Users\Aero\Desktop\Proceso_Clidad\groserias"

            archivos_a_analizar = [archivo for archivo in os.listdir(carpeta_archivos) if archivo.endswith('.txt')]

            for archivo in archivos_a_analizar:
                ruta_archivo = os.path.join(carpeta_archivos, archivo)
                nombre_archivo_sin_extension = os.path.splitext(archivo)[0]  # Obtiene el nombre sin extensión
                ruta_groserias = os.path.join(carpeta_groserias, f"{nombre_archivo_sin_extension}.txt")  # Agrega ".txt" al nombre

                with open(ruta_groserias, 'w', encoding='utf-8') as dato:
                    dato.write(respuesta)
                
                global groserias1
                groserias1.append(respuesta)
                
                print(f"Transcripción del archivo '{archivo}' guardada en '{ruta_groserias}'")

if __name__ == "__main__":
      groserias()
      print("\n--------- FINALIZA OBTENCION DE GROSERIAS CON EXITO ---------\n")
    

    
    
