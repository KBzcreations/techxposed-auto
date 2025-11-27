import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def subir_video():
    print("Iniciando subida a YouTube...")

    # 1. Cargar la llave secreta desde GitHub
    token_json = os.environ.get('YOUTUBE_TOKEN')
    if not token_json:
        print("❌ ERROR: No encuentro el secreto YOUTUBE_TOKEN")
        return

    # 2. Convertir texto a credenciales
    info = json.loads(token_json)
    creds = Credentials.from_authorized_user_info(info, ["https://www.googleapis.com/auth/youtube.upload"])

    # 3. Conectar con YouTube
    youtube = build('youtube', 'v3', credentials=creds)

    # 4. Configurar el video
    request_body = {
        'snippet': {
            'title': 'Curiosidad Tech del Día #Shorts',
            'description': 'Suscríbete para más datos curiosos de tecnología. #Technology #TechXposed #Facts',
            'tags': ['technology', 'curiosidades', 'tech', 'shorts'],
            'categoryId': '28' # Ciencia y Tecnología
        },
        'status': {
            'privacyStatus': 'public', # CAMBIA A 'public' CUANDO ESTÉS SEGURO
            'selfDeclaredMadeForKids': False
        }
    }

    # 5. Subir el archivo
    media = MediaFileUpload('video_techxposed.mp4', chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    )

    response = request.execute()
    print(f"✅ ¡VIDEO SUBIDO! ID: {response['id']}")

if __name__ == "__main__":
    subir_video()
