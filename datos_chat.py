def proteccion_chat():
    
    # ************************ Proceso de proteccion de datos ********************
    
    print("\n--------- INICIANDO PROTECCION DE DATOS ---------\n")
    import os
    import openai

    def hacer_pregunta(fragmento_texto):
        openai.api_key = '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'
        completion = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "Eres un analista de calidad con experiencia en protección de datos confidenciales con mas de 30 años de experiencia"},
                {"role": "user", "content": fragmento_texto}
            ]
        )
        respuesta = completion.choices[0].message.content
        return respuesta
        
    def descomponer_texto(texto):
            fragmentos = [texto[i:i+9000] for i in range(0, len(texto), 9000)]
            return fragmentos

    carpeta_archivos = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'
    carpeta_data = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion1'

    archivos_a_analizar = [archivo for archivo in os.listdir(carpeta_archivos) if archivo.endswith(('.txt', '.doc', '.docx'))]

    for archivo in archivos_a_analizar:
            ruta_archivo = os.path.join(carpeta_archivos, archivo)
            ruta_resultado = os.path.join(carpeta_data, archivo)

            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()

            fragmentos_texto = descomponer_texto(texto_completo)

            respuestas = []

            for fragmento in fragmentos_texto:
                pregunta = f"Reemplaza los datos confidenciales como nombres propios y numeros con variables, no modifiques la informacion ni el contexto de la transcripcion: {fragmento}"
                respuesta = hacer_pregunta(pregunta)
                respuestas.append(respuesta)

            transcripcion_completa = "".join(respuestas)

            with open(ruta_resultado, 'w', encoding='utf-8') as archivo:
                archivo.write(transcripcion_completa)

            print(f"\nTranscripción del archivo '{archivo}' guardada en '{ruta_resultado}'\n")


    #----- Proceso de transformacion de transcripcion a chat -----
    
    print("\n--------- INICIANDO PROCESO DE CHAT ---------\n")
    import os
    import openai
        
    def hacer_pregunta(fragmento_texto):
        openai.api_key = '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'
        completion = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "Eres un experto escritor y guionista con mas de 30 años de experiencia"},
                {"role": "user", "content": fragmento_texto}
            ]
        )
        respuesta = completion.choices[0].message.content
        return respuesta
        
    def descomponer_texto(texto):
            fragmentos = [texto[i:i+9000] for i in range(0, len(texto), 9000)]
            return fragmentos

    carpeta_archivos = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion1'
    carpeta_data = r'C:\Users\Aero\Desktop\Proceso_Clidad\chat'

    archivos_a_analizar = [archivo for archivo in os.listdir(carpeta_archivos) if archivo.endswith(('.txt', '.doc', '.docx'))]

    for archivo in archivos_a_analizar:
            ruta_archivo = os.path.join(carpeta_archivos, archivo)
            ruta_resultado = os.path.join(carpeta_data, archivo)

            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()

            fragmentos_texto = descomponer_texto(texto_completo)

            respuestas = []

            for fragmento in fragmentos_texto:
                pregunta = f"ajusta el siguiente texto en forma de chat, identifica al Agente Telefonico (A.T.) y al Cliente (C.), no cortes el texto, damelo completo y se rigurosamente preciso: {fragmento}"
                respuesta = hacer_pregunta(pregunta)
                respuestas.append(respuesta)

            transcripcion_completa = "".join(respuestas)
            
            with open(ruta_resultado, 'w', encoding='utf-8') as archivo:
                archivo.write(transcripcion_completa)

            print(f"\nTranscripción del archivo '{archivo}' guardada en '{ruta_resultado}'\n")
            

if __name__ == "__main__":
    proteccion_chat()
    print("\n--------- FINALIZA PROTECCION DE DATOS Y CHAT CON EXITO ---------\n")