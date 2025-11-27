import random
import requests
import os
from moviepy.editor import *
from curiosidades import tech_facts

def descargar_imagen_fondo():
    # Lista de imagenes de stock de tecnologia (Verticales o alta calidad)
    urls = [
        "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1531297461136-8208b50b6667?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1550009158-9ebf69173e03?q=80&w=1080&auto=format&fit=crop"
    ]
    url_elegida = random.choice(urls)
    print(f"Descargando fondo: {url_elegida}")
    
    response = requests.get(url_elegida)
    with open("fondo_temp.jpg", "wb") as f:
        f.write(response.content)

def crear_video():
    print("🎬 Iniciando producción de video avanzado...")
    
    # 1. Preparar recursos
    texto_dato = random.choice(tech_facts)
    descargar_imagen_fondo()
    
    # Configuración
    ancho = 1080
    alto = 1920
    duracion = 10 # Segundos
    
    # 2. Crear Fondo (Imagen descargada)
    fondo = ImageClip("fondo_temp.jpg").resize(height=alto)
    # Recortar al centro para que sea 1080 de ancho exacto
    fondo = fondo.crop(x1=fondo.w/2 - ancho/2, y1=0, width=ancho, height=alto)
    fondo = fondo.set_duration(duracion)

    # 3. Añadir Música (Si existe el archivo)
    if os.path.exists("musica.mp3"):
        print("🎵 Añadiendo música de fondo...")
        musica = AudioFileClip("musica.mp3")
        # Cortar la música a la duración del video
        musica = musica.subclip(0, duracion)
        # Bajar volumen al 50%
        musica = musica.volumex(0.5)
        fondo = fondo.set_audio(musica)
    else:
        print("⚠️ No encontré musica.mp3, el video será mudo.")

    # 4. Crear Texto con Caja (Para que se lea bien sobre la imagen)
    # Usamos un try/except para fuentes
    try:
        txt_clip = TextClip(texto_dato, fontsize=65, color='white', font='Courier',
                            method='caption', size=(ancho-150, alto), align='center')
    except:
        txt_clip = TextClip(texto_dato, fontsize=65, color='white',
                            method='caption', size=(ancho-150, alto), align='center')
    
    txt_clip = txt_clip.set_position('center').set_duration(duracion)
    
    # Caja semitransparente detrás del texto (Color negro, opacidad 0.6)
    # Opcional: Si da error, quitamos esta parte, pero le da toque pro.
    
    # 5. Marca de agua
    marca = TextClip("@TechXposed", fontsize=40, color='yellow', font='Arial')
    marca = marca.set_position(('center', 1600)).set_duration(duracion)

    # 6. Componer final
    video_final = CompositeVideoClip([fondo, txt_clip, marca])
    
    # 7. Renderizar
    video_final.write_videofile("video_techxposed.mp4", fps=24, codec='libx264', audio_codec='aac')
    print("✅ ¡Video PRO creado correctamente!")

if __name__ == "__main__":
    crear_video()
