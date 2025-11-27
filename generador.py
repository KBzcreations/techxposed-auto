import random
import requests
import os
import re # Para limpiar texto sucio
import feedparser
from gtts import gTTS
from moviepy.editor import *

# URL DEL FEED (Xataka)
RSS_URL = "http://feeds.weblogssl.com/xataka2"

def limpiar_html(texto_sucio):
    # Esta función elimina etiquetas tipo <p>, <br>, etc.
    limpio = re.sub(r'<.*?>', '', texto_sucio)
    return limpio

def obtener_noticia_random():
    print(f"📡 Buscando noticias en {RSS_URL}...")
    feed = feedparser.parse(RSS_URL)
    
    if len(feed.entries) > 0:
        # TRUCO ANTI-REPETICIÓN:
        # Cogemos las 10 noticias más recientes y elegimos una al azar
        cantidad = min(len(feed.entries), 10)
        noticia = random.choice(feed.entries[:cantidad])
        
        titulo = noticia.title
        # Cogemos el resumen/descripción
        resumen = limpiar_html(noticia.description)
        
        # Cortamos el resumen si es ETERNO (máximo 250 caracteres para un Short)
        if len(resumen) > 250:
            resumen = resumen[:250] + "..."
            
        print(f"📰 Noticia elegida: {titulo}")
        return titulo, resumen
    else:
        return "Sin noticias", "No hemos encontrado actualizaciones hoy."

def texto_a_voz(titulo, resumen, archivo_salida):
    # El guion que leerá el robot
    guion = f"Noticia Tech. {titulo}. {resumen}"
    print(f"🗣️ Locutando: {guion}")
    tts = gTTS(text=guion, lang='es')
    tts.save(archivo_salida)

def descargar_imagen_fondo():
    urls = [
        "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1535223289827-42f1e9919769?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=1080&auto=format&fit=crop"
    ]
    try:
        url_elegida = random.choice(urls)
        response = requests.get(url_elegida)
        with open("fondo_temp.jpg", "wb") as f:
            f.write(response.content)
    except:
        print("⚠️ Error descargando fondo.")

def crear_video():
    print("🎬 Iniciando Noticiero v3.0...")
    
    # 1. Obtener Noticia + Resumen
    titulo, resumen = obtener_noticia_random()
    
    # 2. Generar Voz Completa
    texto_a_voz(titulo, resumen, "voz.mp3")
    clip_voz = AudioFileClip("voz.mp3")
    duracion = clip_voz.duration + 1.0
    print(f"⏱️ Duración del video: {duracion} segundos")
    
    # 3. Fondo
    descargar_imagen_fondo()
    if os.path.exists("fondo_temp.jpg"):
        fondo = ImageClip("fondo_temp.jpg").resize(height=1920)
        fondo = fondo.crop(x1=fondo.w/2 - 1080/2, y1=0, width=1080, height=1920)
    else:
        fondo = ColorClip(size=(1080, 1920), color=(0,0,50))
    
    fondo = fondo.set_duration(duracion)

    # 4. Audio (Voz alta, música baja)
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

    # 5. Texto en pantalla (SOLO EL TÍTULO para que se lea grande)
    # El resumen solo se escucha, no se lee (para no tapar todo)
    try:
        txt_clip = TextClip(titulo, fontsize=50, color='white', font='Arial',
                            method='caption', size=(900, 1500), align='center', stroke_color='black', stroke_width=2)
    except:
        txt_clip = TextClip(titulo, fontsize=50, color='white',
                            method='caption', size=(900, 1500), align='center')
    
    txt_clip = txt_clip.set_position('center').set_duration(duracion)

    # 6. Marca de agua "NOTICIA DEL DÍA"
    marca = TextClip("• TECH NEWS •", fontsize=40, color='white', bg_color='red')
    marca = marca.set_position(('center', 200)).set_duration(duracion)

    # 7. Renderizar
    video_final = CompositeVideoClip([fondo, txt_clip, marca])
    video_final.write_videofile("video_techxposed.mp4", fps=24, codec='libx264', audio_codec='aac')
    print("✅ ¡Noticia completa generada!")

if __name__ == "__main__":
    crear_video()
