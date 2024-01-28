from flask import Flask, request, jsonify
from flask_cors import CORS

import queue
import threading

import mysql.connector

app = Flask(__name__)
task_queue = queue.Queue()
CORS(app)

@app.route('/')
def index():
    """ index function """
    return 'Respondiendo desde la mamalona 2'


import subprocess


def run(name = None, guia = None):
    
    print(name)
    print(guia)

    try:
        #**************** ELIMINA ARCHIVOS DE CARPETAS *************************

        subprocess.run(["python", "elimina_carpeta.py"])

        #****************** TRANSCRIPCION *************************************
        
        subprocess.run(["python", "transcripcion_whisper_api.py", name])

        #******************* PROBLEMATICA Y SOLUCION ***************************
        
        subprocess.run(["python", "proble_solu.py"])
        
        # ************************ PROTECCION DE DATOS Y CHAT ******************
        
        subprocess.run(["python", "datos_chat.py"])

        #******************** INICIO DE PROCESO DE CALIFICACION ****************
        
        subprocess.run(["python", "calificaciones.py", guia])
        
        #******************** INICIO DE PROCESO DE CALIFICACION ****************
        
        subprocess.run(["python", "obtencion_calificacion.py", guia])
        
        #******************** INICIO DE PROCESO DE CONFIRMACION DE SOLLUCIÓN ****************
        
        subprocess.run(["python", "SP_solucion.py", guia])

        #****************** EJECUTA VALIDACIÓN DE GROSERIAS *******************

        subprocess.run(["python", "groserias.py"])
        
        #************************ EJECUTA RESUMEN *****************************
        
        subprocess.run(["python", "resumen_general.py"])
        
        #*************** RESULTADO DE EMOCIONES ********************************

        subprocess.run(["python", "emociones.py"])
        
        #********* AQUI COMIENZA BASE DE DATOS**********************************
        
        subprocess.run(["python", "CargadeBase.py", guia])
        
        #******************* RESUMEN REINSIDENCIA INSATISFACCION ****************
        
        subprocess.run(["python", "resumen_reincidencia_inssatis.py"])

        
    except Exception as e:
        return {'status': False, 'message': f'Error al ejecutar funciones: {str(e)}'}



def task_processor():
   while True:
      task, name, guia = task_queue.get()
      if task:
         try:
            result = task(name, guia)
            print("Resultado: Analizado exitosamente")
            task_queue.task_done()
            
         except Exception as e:
            print(f'Falló el proceso de analizar {name}')
            print(e)
                
            conexion = mysql.connector.connect(
               host="192.168.51.210",
               user="root",
               password="",
               database="audios_dana"
            )
            cursor = conexion.cursor()
            consulta = f"UPDATE audios SET status = 'Error' WHERE audio_name = '{name}'"
            cursor.execute(consulta)
            conexion.commit()

            cursor.close()
            conexion.close()


processing_thread = threading.Thread(target=task_processor)
processing_thread.start()

@app.route('/submit_task', methods=['POST'])
def submit_task():
    task_type = request.json.get('type')
    try:
        if task_type == 'individual':
            name = request.json.get('name')
            guia = request.json.get('guia')
            print('Se mandó individual')
            print(name)
            print(guia)
            task_queue.put((run, name, guia))  
            return jsonify({'status': True, 'message': 'Tarea individual recibida y encolada en mm2'})
      
        if task_type == 'masivo':
            print('Modo de análisis masivo')
            names = request.json.get('names', [])
        
            for name in names:
                task_queue.put((run, name['name'], name['guia'])) 
        
            return jsonify({'status': True, 'message': 'Tarea masiva recibida y encolada en mm2'})

    except Exception as e:
      return jsonify({'message': 'Tipo de tarea no válido'})
   
@app.route('/task_queue', methods=['GET'])
def get_task_queue():
    return jsonify({'task_queue': task_queue})

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=310)

