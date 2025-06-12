from django.urls import path
from . import views

urlpatterns = [
    path('hospital/upload/', views.hospital_upload, name='hospital_upload'),
    path('hospital/reports/', views.hospital_reports, name='hospital_reports'),
    path('doctor/images/', views.doctor_images, name='doctor_images'),
    path('doctor/upload/<int:pk>/', views.upload_audio, name='upload_audio'),
    path('doctor/review/<int:pk>/', views.review_transcript, name='review_transcript'),
]
