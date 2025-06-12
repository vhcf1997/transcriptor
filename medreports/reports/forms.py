from django import forms
from .models import MedicalImage, AudioReport

class ImageUploadForm(forms.ModelForm):
    """Form used by hospitals to assign images to doctors."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # limit doctor choices to users with doctor role
        self.fields['doctor'].queryset = self.fields['doctor'].queryset.filter(role='doctor')

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
