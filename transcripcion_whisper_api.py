import os    
import openai
import time
import mysql.connector
import ftplib
import numpy as np
from pydub import AudioSegment
from scipy.signal import butter, filtfilt
from pydub.silence import detect_silence
import sys
import subprocess

print("\n--------- INICIANDO PROCESO DE TRANSCRIPCION CON WHISPER API ---------\n")

tiempos = []

total_diferencia_minutos = 0

def descargar_archivo_ftp(direccion_servidor, nombre_usuario, contraseña, ruta_remota, ruta_local):
    try:
        with ftplib.FTP(direccion_servidor) as ftp:
            ftp.login(user=nombre_usuario, passwd=contraseña)
            with open(ruta_local, 'wb') as archivo_local:
                ftp.retrbinary('RETR ' + ruta_remota, archivo_local.write)
    except Exception as e:
        print(f"\nError al descargar el archivo desde el servidor FTP: {str(e)}\n")
        raise

def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyquist = 1 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def aplicar_filtro_y_aumentar_volumen(audio_file, ruta_exportacion):
    audio = AudioSegment.from_file(audio_file)

    # Convertir el AudioSegment a un array numpy en formato flotante
    audio_array = np.array(audio.get_array_of_samples(), dtype=np.float32) / 32768.0  # Normalizar entre -1 y 1

    # Frecuencia de corte del filtro para reducir el ruido (ajusta según tus necesidades)
    cutoff_frequency = 7000  # Hz

    # Aplicar filtro de paso bajo para reducir el ruido
    audio_array_filtered = butter_lowpass_filter(audio_array, cutoff_frequency, audio.frame_rate)

    # Escalar el audio filtrado para que esté en el rango de valores permitidos para el ancho de muestra
    scaled_audio_array_filtered = np.int16(audio_array_filtered * 32767)

    # Convertir el array filtrado de vuelta a un AudioSegment
    audio_filtered = AudioSegment(
        scaled_audio_array_filtered.tobytes(),
        frame_rate=audio.frame_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )

    # Subir el volumen de la voz (ajusta el valor de ganancia según tus necesidades)
    ganancia_voz = 15  # Aumentar el volumen en 10 dB
    audio_voz_aumentado = audio_filtered + ganancia_voz

    # Exportar el audio filtrado y mejorado
    audio_voz_aumentado.export(ruta_exportacion, format="wav")

    print("\nMejora de calidad de audio completada. El audio mejorado se ha guardado en:", ruta_exportacion)

def quitar_silencios(audio_file, ruta_exportacion):
    
    global tiempos
    global total_diferencia_minutos
    
    audio = AudioSegment.from_file(audio_file)

    # Definir los parámetros para quitar silencios
    umbral_silencio = -45 #45 # Umbral de volumen para considerar el silencio (en dBFS, ajusta según tus necesidades)
    duracion_minima_silencio = 1000  # Duración mínima de silencio para ser considerado (en milisegundos, ajusta según tus necesidades)
    
    intervalos_silencio = detect_silence(audio, min_silence_len=duracion_minima_silencio, silence_thresh=umbral_silencio)
    
    
    for inicio, fin in intervalos_silencio:
        diferencia = fin - inicio
        if diferencia > 10000:
            inicio_minutos = inicio / 60000
            fin_minutos = fin / 60000
            diferencia_minutos = diferencia / 60000
            tiempos.append(f"Silencio desde {inicio_minutos:.2f} min hasta {fin_minutos:.2f} min, Diferencia: {diferencia_minutos:.2f} min")
            total_diferencia_minutos += diferencia_minutos
            

    # Quitar los silencios del audio
    audio_sin_silencios = audio.strip_silence(silence_thresh=umbral_silencio, silence_len=duracion_minima_silencio)
    
    carpeta_local_tiempos = r'C:\Users\Aero\Desktop\Proceso_Clidad\tiempos_espera'

    with open(carpeta_local_tiempos + '\\tiempos_espera.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(f"Total tiempo de espera en minutos: {total_diferencia_minutos:.2f}\n")
        archivo.write("\n".join(tiempos))

    # Exportar el audio sin silencios
    audio_sin_silencios.export(ruta_exportacion, format="wav")
    print(f"\nEl resultado total de minutos es: {total_diferencia_minutos:.2f}\n")
    print(tiempos)

    
def convertir_wav_a_mp3(ruta_entrada, ruta_salida, bitrate='192k'):
    archivo_wav = AudioSegment.from_wav(ruta_entrada)
    archivo_mp3 = archivo_wav.export(ruta_salida, format='mp3', bitrate=bitrate)
    print(f"Conversión completada. Archivo MP3 guardado en: {ruta_salida}")


def encontrar_repeticiones(texto):

    palabras = texto.split()
    repeticiones = {}

    for palabra in palabras:
        repeticiones[palabra] = repeticiones.get(palabra, 0) + 1

    repeticiones = {palabra: count for palabra, count in repeticiones.items() if count > 50}

    if repeticiones:
        print("\nPalabras o frases repetidas encontradas (más de 50 veces):")
        for palabra, count in repeticiones.items():
            print(f"\n'{palabra}': {count} veces\n")
        return True
    else:
        print("No se encontraron palabras o frases repetidas más de 50 veces.")
        return False
    
    
#***************** PORCESO DE TRANSCRIPCION POR API

def transcripcion_api(audio_path, transcript_folder, audio_file, nombre_archivo):
    
    nombre_audio = nombre_archivo
    
    openai.api_key = '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'

    file_name = os.path.splitext(os.path.basename(audio_path))[0]

    with open(audio_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            temperature=0.0,
            prompt="Esta es una coversacion entre un agente telefonico de la compañia de telecomunicaciones de IZZI y un cliente, no inlcuir este promt en la transcripcion",
            language="es"
        )
    
    print(transcript.text)
    
    if hasattr(transcript, 'text') and isinstance(transcript.text, str):
        if encontrar_repeticiones(transcript.text):
            print("\nSe encontró una palabra repetida más de dos veces seguidas, se ejecuta whisper local.\n")
            subprocess.run(["python", "transcripcion_whisper_local.py", nombre_audio])
        else:
            print("\nNo se encontraron repeticiones de palabras más de dos veces seguidas.\n")
        
        file_name = file_name.replace("_sin_silencios", "")

        transcript_path = os.path.join(transcript_folder, f"{file_name}.txt")
        with open(transcript_path, "w", encoding="utf-8") as transcript_file:
            transcript_file.write(transcript.text)

        print(f"Transcripción {transcript_file} guardada en {transcript_path}")
    else:
        print("Error: No se pudo obtener el texto de la transcripción.")
    
    
#********************* FINALIZA EL PROCESO DE TRANSCRIPCION    


def limpiar_audio(ruta_audio, carpeta_audios, carpeta_transcripciones, nombre_archivo):
    
    try:
        nombre_base = os.path.splitext(os.path.basename(ruta_audio))[0]
    
        ruta_mejorada = os.path.join(carpeta_audios, nombre_base + '_mejorado.wav')
        aplicar_filtro_y_aumentar_volumen(ruta_audio, ruta_mejorada)

        audio_file_mejorado = ruta_mejorada
        ruta_sin_silencios = os.path.join(carpeta_audios, nombre_base + '_sin_silencios.wav')
        quitar_silencios(audio_file_mejorado, ruta_sin_silencios)
        
        ruta_sin_silencios_mp3 = os.path.join(carpeta_audios, nombre_base + '_sin_silencios.mp3')
        convertir_wav_a_mp3(ruta_sin_silencios, ruta_sin_silencios_mp3)

        ruta_transcripcion = os.path.join(carpeta_transcripciones, f"{nombre_base}.txt")

        if os.path.isfile(ruta_transcripcion):
            print(f"\nLa transcripción para el archivo '{nombre_base}' ya existe. Saltando...\n")
            return

        print("▀"*20, " Iniciando transcripción ", "▀"*20)
        start_time = time.time()

        print("\nIniciando transcripcion\n")

        cnx = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="",
            database="audios_dana"
        )

        cursor = cnx.cursor()

        consulta = f"UPDATE audios SET status = 'Transcribiendo' WHERE audio_name = '{nombre_base}'"
        cursor.execute(consulta)
        cnx.commit()

        cursor.close()
        cnx.close()

        transcripcion_api(ruta_sin_silencios_mp3, carpeta_transcripciones, ruta_sin_silencios_mp3, nombre_archivo)

        end_time = time.time()
        execution_time = end_time - start_time 
        print("\nTiempo de ejecución: {:.2f} segundos\n".format(execution_time))

        print(f"\nTranscripción para el archivo '{nombre_base}' guardada en '{ruta_transcripcion}'\n")


    except Exception as e:
        print(f"\n!!! Error al procesar el archivo '{nombre_base}': {str(e)}\n")
        subprocess.run(["python", "transcripcion_whisper_local.py", nombre_archivo])
        raise


def limpiar_archivo(name, carpeta_audios, carpeta_transcripciones, direccion_servidor_ftp, nombre_usuario_ftp, contraseña_ftp):

    nombre_archivo = name

    if nombre_archivo:
        ruta_audio = os.path.join(carpeta_audios, nombre_archivo)
        ruta_transcripcion = os.path.join(carpeta_transcripciones, os.path.splitext(nombre_archivo)[0] + '.txt')

        if os.path.isfile(ruta_audio) and ruta_audio.lower().endswith(('.wav', '.mp3')):
            print(f"\nEl archivo '{nombre_archivo}' ya existe en la carpeta de audios. Saltando la descarga.\n")
        else:
            print(f"\nDescargando el archivo '{nombre_archivo}' desde el servidor FTP...\n")
            print("Ruta remota:", nombre_archivo)
            descargar_archivo_ftp(direccion_servidor_ftp, nombre_usuario_ftp, contraseña_ftp, nombre_archivo, ruta_audio)   

        limpiar_audio(ruta_audio, carpeta_audios, carpeta_transcripciones, nombre_archivo)
    else: 
        print("No se encontró un nombre de archivo en la respuesta JSON.")


def transcripcion_main(name):
    
    carpeta_audios = r'C:\Users\Aero\Desktop\Proceso_Clidad\audios'
    carpeta_transcripciones = r'C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion'
    direccion_servidor_ftp = '192.168.50.37'
    nombre_usuario_ftp = 'rpaback1'
    contraseña_ftp = 'Cyber123'

    conteo = 1

    cnx = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="",
        database="audios_dana"
    )

    cursor = cnx.cursor()

    while True:

        nombre_archivo = name

        if nombre_archivo:
            ruta_remota = f'/Audios/{nombre_archivo}'
            ruta_local = os.path.join(carpeta_audios, nombre_archivo)
            print(f"\nDescargando el archivo '{nombre_archivo}' desde el servidor FTP...\n")
            descargar_archivo_ftp(direccion_servidor_ftp, nombre_usuario_ftp, contraseña_ftp, ruta_remota, ruta_local)
            limpiar_archivo(name, carpeta_audios, carpeta_transcripciones, direccion_servidor_ftp, nombre_usuario_ftp, contraseña_ftp)

        
            cnx = mysql.connector.connect(
                host="192.168.51.210",
                user="root",
                password="",
                database="audios_dana"
            )
            cursor = cnx.cursor()
            consulta = f"UPDATE audios SET status = 'Transcribiendo' WHERE audio_name = '{nombre_archivo}'"
            cursor.execute(consulta)
            cnx.commit()
            cursor.close()
            cnx.close()

            break


        print(f"Esperando análisis de audio {conteo}...")
        conteo += 1

    print("▀"*20, " Finalizando transcripción ", "▀"*20)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
        transcripcion_main(name)
    else:
        print("Por favor, proporciona el nombre del archivo como argumento de línea de comandos.")