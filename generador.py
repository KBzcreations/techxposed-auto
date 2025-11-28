import random
import requests
import os
import re
import feedparser
from gtts import gTTS
from moviepy.editor import *
# Importamos resize explícitamente para evitar conflictos
from moviepy.video.fx.resize import resize

# URL Xataka
RSS_URL = "http://feeds.weblogssl.com/xataka2"

def limpiar_html(texto_sucio):
    limpio = re.sub(r'<.*?>', '', texto_sucio)
    return limpio

def obtener_noticia_random():
    print(f"📡 Buscando noticias...")
    feed = feedparser.parse(RSS_URL)
    if len(feed.entries) > 0:
        # Cogemos una de las 5 últimas
        noticia = random.choice(feed.entries[:5])
        titulo = noticia.title
        resumen = limpiar_html(noticia.description)
        if len(resumen) > 300: resumen = resumen[:300] + "..."
        print(f"📰 Noticia: {titulo}")
        return titulo, resumen
    return "Tecnología", "Sin novedades hoy."

def extraer_palabra_clave(titulo):
    # Intento de buscar nombres propios (palabras en mayúscula que no sean la primera)
    palabras = titulo.split()
    nombres_propios = []
    for i, palabra in enumerate(palabras):
        # Limpiamos signos de puntuación
        palabra_limpia = re.sub(r'[^\w\s]', '', palabra)
        # Si empieza por mayúscula y tiene longitud decente
        if len(palabra_limpia) > 3 and palabra_limpia[0].isupper():
             nombres_propios.append(palabra_limpia)
    
    if nombres_propios:
        # Usamos el nombre propio más largo encontrado (ej: "Elon Musk" -> Musk)
        busqueda = max(nombres_propios, key=len)
    else:
        # Si no hay nombres propios, usamos la palabra más larga del título
        busqueda = max(palabras, key=len)
        
    busqueda = re.sub(r'[^\w\s]', '', busqueda) # Limpieza final
    print(f"🔍 Palabra clave detectada: {busqueda}")
    return busqueda

def buscar_imagen_inteligente(titulo):
    keyword = extraer_palabra_clave(titulo)
    print(f"📷 Buscando foto en Unsplash: {keyword}")
    
    # Buscamos en Unsplash (añadimos 'tech' para contexto)
    url_imagen = f"https://source.unsplash.com/1080x1920/?{keyword},tech"
    
    try:
        response = requests.get(url_imagen, allow_redirects=True, timeout=15)
        if response.status_code == 200 and len(response.content) > 1000:
            with open("fondo_temp.jpg", "wb") as f:
                f.write(response.content)
            return True
    except:
        print("⚠️ Fallo buscando imagen específica.")
    
    return False

def crear_video():
    print("🎬 Producción v5.0 (Final Polish)...")
    
    # 1. Noticia
    titulo, resumen = obtener_noticia_random()
    
    # 2. Audio
    # Truco: Añadimos un silencio al principio para que no empiece de golpe
    texto_leible = f"... Atención a la noticia tech de hoy. {titulo}. {resumen}"
    tts = gTTS(text=texto_leible, lang='es')
    tts.save("voz.mp3")
    
    clip_voz = AudioFileClip("voz.mp3")
    duracion = clip_voz.duration + 1.5 # Un poco más de margen al final
    
    # 3. Imagen Inteligente
    exito_foto = buscar_imagen_inteligente(titulo)
    
    if not exito_foto or not os.path.exists("fondo_temp.jpg"):
        print("Descargando fondo backup...")
        r = requests.get("https://images.unsplash.com/photo-1485827404703-89b55fcc595e?q=80&w=1080&fit=crop")
        with open("fondo_temp.jpg", "wb") as f: f.write(r.content)

    # Procesar Imagen
    fondo_img = ImageClip("fondo_temp.jpg").resize(height=1920)
    fondo_img = fondo_img.crop(x1=fondo_img.w/2 - 1080/2, y1=0, width=1080, height=1920)
    fondo_img = fondo_img.set_duration(duracion)
    
    # APLICAR MOVIMIENTO (Zoom lento más suave)
    # Usamos una función de moviepy para evitar errores de lambda
    fondo_animado = resize(fondo_img, lambda t : 1 + 0.03*t)
    fondo_animado = fondo_animado.set_position(('center', 'center'))

    # 4. Texto Profesional (Márgenes ajustados)
    # Caja un poco más ancha y menos alta
    caja_color = ColorClip(size=(1000, 700), color=(0,0,0)).set_opacity(0.65)
    caja_color = caja_color.set_position('center').set_duration(duracion)

    # Texto con un poco más de margen (size más pequeño que la caja)
    try:
        txt_clip = TextClip(titulo, fontsize=50, color='white', font='Arial-Bold',
                            method='caption', size=(900, 650), align='center')
    except:
        txt_clip = TextClip(titulo, fontsize=50, color='white',
                            method='caption', size=(900, 650), align='center')
    
    txt_clip = txt_clip.set_position('center').set_duration(duracion)

    # 5. Música
    audios = [clip_voz]
    if os.path.exists("musica.mp3"):
        musica = AudioFileClip("musica.mp3")
        if musica.duration < duracion:
            musica = afx.audio_loop(musica, duration=duracion)
        else:
            musica = musica.subclip(0, duracion)
        musica = musica.volumex(0.12) # Un pelín más baja
        audios.append(musica)

    # 6. Composición Final
    video_final = CompositeVideoClip([
        fondo_animado, 
        caja_color, 
        txt_clip,
        TextClip("TechXposed • Noticias Diarias", fontsize=35, color='yellow', font='Arial').set_position(('center', 1650)).set_duration(duracion)
    ], size=(1080,1920)).set_audio(CompositeAudioClip(audios))

    video_final.write_videofile("video_techxposed.mp4", fps=24, preset='ultrafast')
    print("✅ Video v5 Generado")

if __name__ == "__main__":
    crear_video()
