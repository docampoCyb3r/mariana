import os

def eliminar_archivos_en_carpetas(carpetas):
    for carpeta in carpetas:
        
        archivos = os.listdir(carpeta)

        for archivo in archivos:
            ruta_completa = os.path.join(carpeta, archivo)
            if os.path.isfile(ruta_completa):
                try:
                    os.remove(ruta_completa)
                    print(f"Se ha eliminado el archivo: {ruta_completa}")
                except Exception as e:
                    print(f"No se pudo eliminar {ruta_completa}: {e}")

def elim():
    carpetas = [
        r"C:\Users\Aero\Desktop\Proceso_Clidad\audios",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\calificacion",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\chat",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\groserias",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\problematica",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\resultados_emociones",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\resumen_llamada",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\solucion",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\transcripcion1",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\pov",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\pov1",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\pov2",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\pov3",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\pov4",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\json_calificacion_1",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\calificacion\json_calificacion_2",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\contextos_calidad",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\tiempos_espera",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\cliente_insatisfecho",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\resumen_corto",
        r"C:\Users\Aero\Desktop\Proceso_Clidad\reincidencia"
    ]

    eliminar_archivos_en_carpetas(carpetas)

if __name__ == "__main__":
    print("\n--------- INICIANDO ELIMINACION DE ARCHIVOS ALMACENADOS ---------\n")
    elim()
    print("\n--------- FINALIZA ELIMINACION CON EXITO ---------\n")