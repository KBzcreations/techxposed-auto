import random
import requests
import os
import feedparser # Librería para leer noticias
from gtts import gTTS
from moviepy.editor import *

# FUENTE DE NOTICIAS (Xataka - Tecnología en Español)
RSS_URL = "http://feeds.weblogssl.com/xataka2"

def obtener_noticia_hoy():
    print(f"📡 Conectando a {RSS_URL}...")
    feed = feedparser.parse(RSS_URL)
    
    if len(feed.entries) > 0:
        # Cogemos la noticia más nueva (la primera)
        noticia = feed.entries[0]
        titulo = noticia.title
        # Limpiamos un poco el texto para que la voz lo lea bien
        print(f"📰 Noticia encontrada: {titulo}")
        return titulo
    else:
        return "Hoy no hay noticias de tecnología disponibles."

def texto_a_voz(texto, archivo_salida):
    texto_leible = f"Noticia Tech de hoy: {texto}"
    print(f"🗣️ Generando locución: {texto_leible}")
    tts = gTTS(text=texto_leible, lang='es')
    tts.save(archivo_salida)

def descargar_imagen_fondo():
    # Buscamos fondos más abstractos/tecnológicos para que peguen con cualquier noticia
    urls = [
        "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1535223289827-42f1e9919769?q=80&w=1080&auto=format&fit=crop"
    ]
    try:
        url_elegida = random.choice(urls)
        response = requests.get(url_elegida)
        with open("fondo_temp.jpg", "wb") as f:
            f.write(response.content)
    except:
        print("⚠️ Error fondo.")

def crear_video():
    print("🎬 Iniciando Noticiero Automático...")
    
    # 1. Obtener la noticia REAL de hoy
    texto_noticia = obtener_noticia_hoy()
    
    # 2. Voz
    texto_a_voz(texto_noticia, "voz.mp3")
    clip_voz = AudioFileClip("voz.mp3")
    duracion = clip_voz.duration + 1.5
    
    # 3. Fondo
    descargar_imagen_fondo()
    if os.path.exists("fondo_temp.jpg"):
        fondo = ImageClip("fondo_temp.jpg").resize(height=1920)
        fondo = fondo.crop(x1=fondo.w/2 - 1080/2, y1=0, width=1080, height=1920)
    else:
        fondo = ColorClip(size=(1080, 1920), color=(0,0,100))
    
    fondo = fondo.set_duration(duracion)

    # 4. Audio Mezcla
    audios = [clip_voz]
    if os.path.exists("musica.mp3"):
        musica = AudioFileClip("musica.mp3")
        if musica.duration < duracion:
            musica = afx.audio_loop(musica, duration=duracion)
        else:
            musica = musica.subclip(0, duracion)
        musica = musica.volumex(0.15) 
        audios.append(musica)
    
    fondo = fondo.set_audio(CompositeAudioClip(audios))

    # 5. Texto en pantalla (Dividimos el título si es muy largo para que entre)
    # Creamos una caja negra semitransparente para que se lea mejor
    try:
        txt_clip = TextClip(texto_noticia, fontsize=55, color='white', font='Arial',
                            method='caption', size=(900, 1600), align='center', stroke_color='black', stroke_width=2)
    except:
        txt_clip = TextClip(texto_noticia, fontsize=55, color='white',
                            method='caption', size=(900, 1600), align='center')
    
    txt_clip = txt_clip.set_position('center').set_duration(duracion)

    # 6. Marca de agua "BREAKING NEWS"
    marca = TextClip("ÚLTIMA HORA • TECH", fontsize=45, color='red', font='Arial', bg_color='white')
    marca = marca.set_position(('center', 200)).set_duration(duracion)

    # 7. Renderizar
    video_final = CompositeVideoClip([fondo, txt_clip, marca])
    video_final.write_videofile("video_techxposed.mp4", fps=24, codec='libx264', audio_codec='aac')
    print("✅ ¡Noticia generada!")

if __name__ == "__main__":
    crear_video()
