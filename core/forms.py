# core/forms.py
from django import forms
from .models import Transcricao

class TranscricaoForm(forms.ModelForm):
    class Meta:
        model = Transcricao
        fields = ['audio']