print("\n--------- INICIANDO OBTENCION DE EMOCIONES ---------\n")

import os
import glob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import openai


def emociones_dato():
    nltk.download('vader_lexicon')

    # Método para transcribir el texto
    def transcribe_text(text_path):
        with open(text_path, 'r', encoding='utf-8') as file:
            text = file.read()

        return text

    # Configurar la API de OpenAI con tu clave de API
    openai.api_key = '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'

    # Carpeta de origen de los archivos de texto
    folder_path = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'

    # Carpeta para guardar los resultados
    results_folder = r'C:\Users\Aero\Desktop\Proceso_Clidad\resultados_emociones'
    os.makedirs(results_folder, exist_ok=True)

    # Obtener la lista de archivos de texto en la carpeta
    text_paths = glob.glob(folder_path + '/*.txt')

    sia = SentimentIntensityAnalyzer()

    for text_path in text_paths:
        # Obtener el nombre del archivo sin la extensión
        file_name = os.path.splitext(os.path.basename(text_path))[0]

        # Verificar si el archivo ya ha sido analizado
        result_file = os.path.join(results_folder, file_name + '.txt')
        if os.path.exists(result_file):
            print("El archivo {} ya ha sido analizado.".format(file_name))
            continue

        # Realizar el análisis de sentimientos en el archivo de texto
        text = transcribe_text(text_path)

        # Descomponer el texto en secciones
        secciones = descomponer_prompt(text, 4090)

        # Realizar el análisis de sentimientos para cada sección
        scores = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}
        for seccion in secciones:
            response = openai.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=seccion + "\nSentiment:",
                max_tokens=1,
                temperature=0,
                n=1,
                stop=None
            )
            sentiment = response.choices[0].text.strip().lower()
            sentiment_scores = sia.polarity_scores(sentiment)

            scores['neg'] += sentiment_scores['neg']
            scores['neu'] += sentiment_scores['neu']
            scores['pos'] += sentiment_scores['pos']
            scores['compound'] += sentiment_scores['compound']

        # Calcular los promedios de los puntajes de sentimiento
        num_secciones = len(secciones)
        scores['neg'] /= num_secciones
        scores['neu'] /= num_secciones
        scores['pos'] /= num_secciones
        scores['compound'] /= num_secciones

        print("Análisis de sentimientos del archivo de texto:", file_name)
        print(f"Puntuación de negatividad: {scores['neg']}")
        print(f"Puntuación de neutralidad: {scores['neu']}")
        print(f"Puntuación de positividad: {scores['pos']}")
        print(f"Puntuación de sentimiento general: {scores['compound']}")
        print()

        # Guardar los resultados en un archivo separado
        with open(result_file, 'w') as file:
            file.write("Análisis de sentimientos del archivo de texto: {}\n".format(file_name))
            file.write("Puntuación de negatividad: {}\n".format(scores['neg']))
            file.write("Puntuación de neutralidad: {}\n".format(scores['neu']))
            file.write("Puntuación de positividad: {}\n".format(scores['pos']))
            file.write("Puntuación de sentimiento general: {}\n".format(scores['compound']))
            file.write("\n")


def descomponer_prompt(texto, longitud_maxima):
    secciones = []

    while len(texto) > longitud_maxima:
        # Encontrar el último punto antes de la longitud máxima
        indice_punto = texto.rfind('.', 0, longitud_maxima)

        # Verificar si se encontró un punto dentro del rango
        if indice_punto != -1:
            # Agregar la sección al resultado y eliminarla del texto original
            seccion = texto[:indice_punto + 1]
            secciones.append(seccion)
            texto = texto[indice_punto + 1:].lstrip()
        else:
            # No se encontró un punto dentro del rango, dividir en la longitud máxima
            seccion = texto[:longitud_maxima]
            secciones.append(seccion)
            texto = texto[longitud_maxima:].lstrip()

    # Agregar la última sección
    secciones.append(texto)

    return secciones


if __name__ == "__main__":
    emociones_dato()
    print("\n--------- FINALIZA OBTENCION DE EMOCIONES CON EXITO ---------\n")