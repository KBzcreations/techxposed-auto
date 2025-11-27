# generador.py
import random
from moviepy.editor import *
from curiosidades import tech_facts

def crear_video():
    print("Iniciando creación de video...")
    texto_dato = random.choice(tech_facts)
    print(f"Dato elegido: {texto_dato}")
    
    ancho = 1080
    alto = 1920
    duracion = 8 
    
    fondo = ColorClip(size=(ancho, alto), color=(10, 10, 20), duration=duracion)
    
    try:
        txt_clip = TextClip(texto_dato, fontsize=70, color='white', 
                            method='caption', size=(ancho-200, alto), align='center')
    except Exception:
        txt_clip = TextClip(texto_dato, fontsize=70, color='white', 
                            size=(ancho-200, alto), method='caption', align='center')

    txt_clip = txt_clip.set_position('center').set_duration(duracion)
    
    marca = TextClip("@TechXposed", fontsize=50, color='green')
    marca = marca.set_position(('center', 1600)).set_duration(duracion)

    video_final = CompositeVideoClip([fondo, txt_clip, marca])
    video_final.write_videofile("video_techxposed.mp4", fps=24)
    print("¡Video creado correctamente!")

if __name__ == "__main__":
    crear_video()
