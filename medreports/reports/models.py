from django.db import models
from django.conf import settings

class MedicalImage(models.Model):
    hospital = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignments')
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AudioReport(models.Model):
    image = models.ForeignKey(MedicalImage, on_delete=models.CASCADE, related_name='reports')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    audio = models.FileField(upload_to='audio/')
    transcript = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
