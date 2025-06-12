from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('sucesso/<int:pk>/', views.sucesso_view, name='sucesso'),
]