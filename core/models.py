from django.db import models

from django.db import models

class Transcricao(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PROCESSANDO', 'Processando'),
        ('CONCLUIDO', 'Concluído'),
        ('ERRO', 'Erro'),
    ]
    audio = models.FileField(upload_to='audios/')
    texto = models.TextField(blank=True, null=True, verbose_name="Texto Transcrito")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transcrição #{self.id} - {self.status}"