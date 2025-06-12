# core/tasks.py (Versão Final com Normalização)

import os
import json
import wave
from celery import shared_task
from .models import Transcricao
from django.conf import settings
from pydub import AudioSegment
# 1. Importamos a função de normalização
from pydub.effects import normalize
from vosk import Model, KaldiRecognizer


@shared_task(bind=True)
def transcrever_audio_task(self, transcricao_id):
    caminho_audio_wav = None
    try:
        transcricao = Transcricao.objects.get(id=transcricao_id)
        transcricao.status = 'PROCESSANDO'
        transcricao.save()

        caminho_audio_original = transcricao.audio.path

        # --- ETAPA DE PRÉ-PROCESSAMENTO DO ÁUDIO ---
        # Carregamos o áudio original
        audio = AudioSegment.from_file(caminho_audio_original)

        # 2. NORMALIZAÇÃO DE VOLUME (A NOVA ETAPA)
        # Aplicamos um efeito de normalização para aumentar o volume de áudios baixos
        audio_normalizado = normalize(audio)
        print("DEBUG: Volume do áudio normalizado.")

        # Definimos o caminho para o arquivo WAV temporário
        caminho_audio_wav = os.path.splitext(caminho_audio_original)[0] + ".wav"

        # Convertemos para o formato ideal para o Vosk (usando o áudio já normalizado)
        audio_final = audio_normalizado.set_channels(1)
        audio_final = audio_final.set_frame_rate(16000)
        audio_final.export(caminho_audio_wav, format="wav")
        print("DEBUG: Áudio convertido para WAV (16kHz, Mono).")
        # ----------------------------------------------

        # --- TRANSCRIÇÃO USANDO VOSK DIRETAMENTE ---
        caminho_modelo = os.path.join(settings.BASE_DIR, 'core', 'vosk-model-small-pt-0.3')
        model = Model(caminho_modelo)

        with wave.open(caminho_audio_wav, "rb") as wf:
            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)
            rec.AcceptWaveform(wf.readframes(wf.getnframes()))

        resultado_json = json.loads(rec.FinalResult())
        texto_transcrito = resultado_json.get('text', '')  # .get() é mais seguro
        print(f"DEBUG: Texto extraído: '{texto_transcrito}'")
        # ------------------------------------------

        transcricao.texto = texto_transcrito
        transcricao.status = 'CONCLUIDO'
        transcricao.save()

        return f"Transcrição {transcricao_id} concluída."

    except Exception as e:
        transcricao.status = 'ERRO'
        transcricao.texto = f"Ocorreu um erro: {str(e)}"
        transcricao.save()
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        raise

    finally:
        # Recomendo reativar a limpeza dos arquivos temporários agora
        if caminho_audio_wav and os.path.exists(caminho_audio_wav):
            os.remove(caminho_audio_wav)