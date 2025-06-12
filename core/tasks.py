# core/tasks.py
import os
from celery import shared_task
from .models import Transcricao
import speech_recognition as sr
from django.conf import settings

@shared_task(bind=True)
def transcrever_audio_task(self, transcricao_id):
    try:
        transcricao = Transcricao.objects.get(id=transcricao_id)
        transcricao.status = 'PROCESSANDO'
        transcricao.save()

        caminho_audio = transcricao.audio.path
        # O nome da pasta deve ser exatamente o mesmo que você baixou
        caminho_modelo = os.path.join(settings.BASE_DIR, 'core', 'vosk-model-small-pt-0.3')

        r = sr.Recognizer()
        with sr.AudioFile(caminho_audio) as source:
            audio_data = r.record(source)

        # A mágica acontece aqui, usando o motor Vosk
        texto_transcrito = r.recognize_vosk(audio_data, language='pt', model_path=caminho_modelo)

        transcricao.texto = texto_transcrito
        transcricao.status = 'CONCLUIDO'
        transcricao.save()
        return f"Transcrição {transcricao_id} concluída."

    except Exception as e:
        transcricao.status = 'ERRO'
        transcricao.texto = f"Ocorreu um erro: {str(e)}"
        transcricao.save()
        # Isso ajuda a depurar o erro no Celery
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        raise