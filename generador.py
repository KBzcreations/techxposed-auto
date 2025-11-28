import random
import requests
import os
import re
import feedparser
from gtts import gTTS
from moviepy.editor import *
from moviepy.video.fx.all import resize # Para el zoom

# URL Xataka
RSS_URL = "http://feeds.weblogssl.com/xataka2"

def limpiar_html(texto_sucio):
    limpio = re.sub(r'<.*?>', '', texto_sucio)
    return limpio

def obtener_noticia_random():
    print(f"📡 Buscando noticias...")
    feed = feedparser.parse(RSS_URL)
    if len(feed.entries) > 0:
        # Cogemos una de las 5 últimas para que sea fresca
        noticia = random.choice(feed.entries[:5])
        titulo = noticia.title
        resumen = limpiar_html(noticia.description)
        # Limitar resumen
        if len(resumen) > 300: resumen = resumen[:300] + "..."
        print(f"📰 Noticia: {titulo}")
        return titulo, resumen
    return "Tecnología", "Sin novedades hoy."

def buscar_imagen_relacionada(titulo):
    # Truco: Cogemos las palabras clave del título para buscar la foto
    # Ejemplo: "El nuevo iPhone 15..." -> busca "iPhone"
    palabras = titulo.split()
    busqueda = "technology" # Por defecto
    
    # Intentamos coger palabras significativas (más de 4 letras)
    palabras_clave = [p for p in palabras if len(p) > 4]
    if palabras_clave:
        busqueda = palabras_clave[0] # Usamos la primera palabra larga
    
    print(f"📷 Buscando foto sobre: {busqueda}")
    
    # Usamos la API pública de Unsplash (source) para buscar
    url_imagen = f"https://source.unsplash.com/1080x1920/?{busqueda},technology"
    
    # NOTA: Como source.unsplash a veces falla, usamos un fallback manual
    # Intentamos descargar, si falla, usamos una genérica
    try:
        response = requests.get(url_imagen, allow_redirects=True, timeout=10)
        # Si la URL final es la de "imagen no encontrada", usamos backup
        if response.status_code == 200:
            with open("fondo_temp.jpg", "wb") as f:
                f.write(response.content)
            return True
    except:
        print("⚠️ Fallo buscando imagen específica, usando genérica.")
    
    return False

def efecto_zoom(clip, zoom_ratio=0.04):
    # Efecto Ken Burns (Zoom lento hacia adentro)
    def effect(get_frame, t):
        img = get_frame(t)
        h, w = img.shape[:2]
        # Zoom progresivo
        scale = 1 + zoom_ratio * (t / clip.duration)
        # Aquí simplificamos usando resize de moviepy directamente abajo
        return img
    return clip.resize(lambda t : 1 + 0.02*t) 

def crear_video():
    print("🎬 Producción v4.0 (Visual Upgrade)...")
    
    # 1. Noticia
    titulo, resumen = obtener_noticia_random()
    
    # 2. Audio
    texto_leible = f"Atención. {titulo}. {resumen}"
    tts = gTTS(text=texto_leible, lang='es')
    tts.save("voz.mp3")
    
    clip_voz = AudioFileClip("voz.mp3")
    duracion = clip_voz.duration + 1.0
    
    # 3. Imagen Inteligente
    exito_foto = buscar_imagen_relacionada(titulo)
    
    if not exito_foto or not os.path.exists("fondo_temp.jpg"):
        # Descargar genérica si falló la búsqueda
        print("Descargando fondo backup...")
        r = requests.get("https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1080&fit=crop")
        with open("fondo_temp.jpg", "wb") as f: f.write(r.content)

    # Procesar Imagen con ZOOM
    fondo_img = ImageClip("fondo_temp.jpg").resize(height=1920)
    # Recorte central
    fondo_img = fondo_img.crop(x1=fondo_img.w/2 - 1080/2, y1=0, width=1080, height=1920)
    fondo_img = fondo_img.set_duration(duracion)
    
    # APLICAR MOVIMIENTO (Zoom lento) - Esto le da vida
    # Nota: El resize puede ser lento, si falla el render, quita esta línea
    fondo_animado = fondo_img.resize(lambda t : 1 + 0.04*t)  
    # Al hacer zoom, la imagen crece, hay que mantenerla centrada
    fondo_animado = fondo_animado.set_position(('center', 'center'))

    # 4. Texto Profesional (Caja oscura)
    # Caja negra semitransparente detrás del texto
    caja_color = ColorClip(size=(950, 800), color=(0,0,0)).set_opacity(0.6)
    caja_color = caja_color.set_position('center').set_duration(duracion)

    try:
        txt_clip = TextClip(titulo, fontsize=55, color='white', font='Arial-Bold',
                            method='caption', size=(900, 750), align='center')
    except:
        txt_clip = TextClip(titulo, fontsize=55, color='white',
                            method='caption', size=(900, 750), align='center')
    
    txt_clip = txt_clip.set_position('center').set_duration(duracion)

    # 5. Música de fondo
    audios = [clip_voz]
    if os.path.exists("musica.mp3"):
        musica = AudioFileClip("musica.mp3")
        if musica.duration < duracion:
            musica = afx.audio_loop(musica, duration=duracion)
        else:
            musica = musica.subclip(0, duracion)
        musica = musica.volumex(0.15)
        audios.append(musica)

    # 6. Composición Final
    # Capas: Fondo Animado -> Caja Negra -> Texto -> Marca de agua
    video_final = CompositeVideoClip([
        fondo_animado, 
        caja_color, 
        txt_clip,
        TextClip("@TechXposed", fontsize=30, color='yellow').set_position(('center', 1600)).set_duration(duracion)
    ], size=(1080,1920)).set_audio(CompositeAudioClip(audios))

    video_final.write_videofile("video_techxposed.mp4", fps=24)
    print("✅ Video v4 Generado")

if __name__ == "__main__":
    crear_video()
