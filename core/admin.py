from django.contrib import admin
from .models import Transcricao

@admin.register(Transcricao)
class TranscricaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'texto', 'criado_em')
    list_filter = ('status',)
    readonly_fields = ('texto', 'criado_em', 'atualizado_em')