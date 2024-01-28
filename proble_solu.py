def proble_solucio():    

    # ******************* Problematica 
    print("\n--------- OBTENIENDO PROBLEMATICA ---------\n")
    import os
    import openai

        # Función para enviar un fragmento de texto al modelo y obtener una respuesta
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
        
    # Directorio de la carpeta de archivos a analizar y carpeta de resultados
    carpeta_archivos = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'
    carpeta_data = r'C:\Users\Aero\Desktop\Proceso_Clidad\problematica'

        # Obtener la lista de archivos en la carpeta de transcripción
    archivos_a_analizar = [archivo for archivo in os.listdir(carpeta_archivos) if archivo.endswith(('.txt', '.doc', '.docx'))]

        # Realizar el análisis para cada archivo
    for archivo in archivos_a_analizar:
            ruta_archivo = os.path.join(carpeta_archivos, archivo)
            ruta_resultado = os.path.join(carpeta_data, archivo)

            # Leer el archivo de texto local
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()
                
            # Enviar cada fragmento al modelo y obtener las respuestas
            pregunta = f"necesito que resumas la problematica presentada en la conversación en un maximo de 30 palabras: {texto_completo}"
            respuesta = hacer_pregunta(pregunta)
            
            # Guardar la transcripción completa en un archivo de texto en la carpeta de chat
            with open(ruta_resultado, 'w', encoding='utf-8') as archivo:
                archivo.write(respuesta)

            print(f"\nTranscripción del archivo '{archivo}' guardada en '{ruta_resultado}'\n")
            
    # ******************* Solución
    print("\n--------- OBTENIENDO SOLUCION ---------\n")
    import os
    import openai

        # Función para enviar un fragmento de texto al modelo y obtener una respuesta
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
        
    # Directorio de la carpeta de archivos a analizar y carpeta de resultados 
    carpeta_archivos = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'
    carpeta_data = r'C:\Users\Aero\Desktop\Proceso_Clidad\solucion'

        # Obtener la lista de archivos en la carpeta de transcripción
    archivos_a_analizar = [archivo for archivo in os.listdir(carpeta_archivos) if archivo.endswith(('.txt', '.doc', '.docx'))]

        # Realizar el análisis para cada archivo
    for archivo in archivos_a_analizar:
            ruta_archivo = os.path.join(carpeta_archivos, archivo)
            ruta_resultado = os.path.join(carpeta_data, archivo)

            # Leer el archivo de texto local
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()
                
            # Enviar cada fragmento al modelo y obtener las respuestas
            pregunta = f"necesito que resumas la solucion otorgada al cliente en un maximo de 30 palabras: {texto_completo}"
            respuesta = hacer_pregunta(pregunta)
            
            # Guardar la transcripción completa en un archivo de texto en la carpeta de chat
            with open(ruta_resultado, 'w', encoding='utf-8') as archivo:
                archivo.write(respuesta)

            print(f"\nTranscripción del archivo '{archivo}' guardada en '{ruta_resultado}'\n")


if __name__ == "__main__":
    proble_solucio()
    print("\n--------- FINALIZA PROBLEMATICA Y SOLUCION CON EXITO ---------\n")
