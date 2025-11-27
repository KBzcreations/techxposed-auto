import random
import requests
import os
import asyncio
import edge_tts
from moviepy.editor import *
from curiosidades import tech_facts

# Configuración de voz (Puedes cambiar a 'es-ES-ElviraNeural' si prefieres mujer)
VOZ_ROBOT = "es-ES-AlvaroNeural" 

async def texto_a_voz(texto, archivo_salida):
    print(f"🗣️ Generando voz: {texto}")
    comunicate = edge_tts.Communicate(texto, VOZ_ROBOT)
    await comunicate.save(archivo_salida)

def descargar_imagen_fondo():
    # Fondos Tech verticales
    urls = [
        "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1531297461136-8208b50b6667?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1080&auto=format&fit=crop"
    ]
    try:
        url_elegida = random.choice(urls)
        print(f"Descargando fondo: {url_elegida}")
        response = requests.get(url_elegida)
        with open("fondo_temp.jpg", "wb") as f:
            f.write(response.content)
    except:
        print("⚠️ Error descargando fondo, se usará negro.")

def crear_video():
    print("🎬 Iniciando producción con VOZ...")
    
    # 1. Preparar el dato y la voz
    texto_dato = random.choice(tech_facts)
    
    # Generar el archivo de audio con la voz (Async wrapper)
    asyncio.run(texto_a_voz(texto_dato, "voz.mp3"))
    
    # Cargar el audio de la voz para saber cuánto dura
    clip_voz = AudioFileClip("voz.mp3")
    duracion = clip_voz.duration + 1.5 # Añadimos 1.5 seg de margen
    print(f"⏱️ Duración calculada: {duracion} segundos")

    # 2. Preparar fondo
    descargar_imagen_fondo()
    if os.path.exists("fondo_temp.jpg"):
        fondo = ImageClip("fondo_temp.jpg").resize(height=1920)
        fondo = fondo.crop(x1=fondo.w/2 - 1080/2, y1=0, width=1080, height=1920)
    else:
        fondo = ColorClip(size=(1080, 1920), color=(0,0,0))
    
    fondo = fondo.set_duration(duracion)

    # 3. Preparar Audio Final (Mezcla Voz + Música)
    audios = [clip_voz] # Empezamos con la voz
    
    if os.path.exists("musica.mp3"):
        print("🎵 Mezclando música de fondo...")
        musica = AudioFileClip("musica.mp3")
        
        # Si la música es más corta que el video, hacer bucle
        if musica.duration < duracion:
            musica = afx.audio_loop(musica, duration=duracion)
        else:
            musica = musica.subclip(0, duracion)
            
        # Bajar volumen de música al 20% para que se oiga la voz
        musica = musica.volumex(0.20) 
        audios.append(musica) # Añadimos la música a la mezcla
    
    # Mezclar todo el audio
    audio_final = CompositeAudioClip(audios)
    fondo = fondo.set_audio(audio_final)

    # 4. Texto visual (Centrado)
    try:
        txt_clip = TextClip(texto_dato, fontsize=60, color='white', font='Arial',
                            method='caption', size=(1080-150, 1920), align='center')
    except:
        txt_clip = TextClip(texto_dato, fontsize=60, color='white',
                            method='caption', size=(1080-150, 1920), align='center')
    
    txt_clip = txt_clip.set_position('center').set_duration(duracion)

    # 5. Marca de agua
    marca = TextClip("@TechXposed", fontsize=40, color='yellow')
    marca = marca.set_position(('center', 1600)).set_duration(duracion)

    # 6. Renderizar
    video_final = CompositeVideoClip([fondo, txt_clip, marca])
    video_final.write_videofile("video_techxposed.mp4", fps=24, codec='libx264', audio_codec='aac')
    print("✅ ¡Video PARLANTE creado!")

if __name__ == "__main__":
    crear_video()
