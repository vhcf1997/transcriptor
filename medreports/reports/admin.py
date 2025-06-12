from django.contrib import admin
from .models import MedicalImage, AudioReport

admin.site.register(MedicalImage)
admin.site.register(AudioReport)
