# core/views.py
from django.shortcuts import render, redirect
from .forms import TranscricaoForm
from .tasks import transcrever_audio_task

def upload_view(request):
    if request.method == 'POST':
        form = TranscricaoForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva o formulário para criar o objeto Transcricao no banco
            nova_transcricao = form.save()

            # Dispara a tarefa do Celery com o ID do objeto
            transcrever_audio_task.delay(nova_transcricao.id)

            # Redireciona para uma página de sucesso
            return redirect('sucesso', pk=nova_transcricao.id)
    else:
        form = TranscricaoForm()
    return render(request, 'core/upload.html', {'form': form})

def sucesso_view(request, pk):
    return render(request, 'core/sucesso.html', {'pk': pk})