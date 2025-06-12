from django import forms
from .models import MedicalImage, AudioReport

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = MedicalImage
        fields = ['doctor', 'image']

class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = AudioReport
        fields = ['audio']

class TranscriptForm(forms.ModelForm):
    class Meta:
        model = AudioReport
        fields = ['transcript']
