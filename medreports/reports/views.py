from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MedicalImage, AudioReport
from .forms import ImageUploadForm, AudioUploadForm, TranscriptForm
import speech_recognition as sr


def transcribe_audio(path):
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    try:
        return r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        return ''

@login_required
def hospital_upload(request):
    if not request.user.role == 'hospital':
        return redirect('login')
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.hospital = request.user
            img.save()
            return redirect('hospital_upload')
    else:
        form = ImageUploadForm()
    return render(request, 'hospital_upload.html', {'form': form})

@login_required
def doctor_images(request):
    images = MedicalImage.objects.filter(doctor=request.user)
    return render(request, 'doctor_images.html', {'images': images})

@login_required
def upload_audio(request, pk):
    image = get_object_or_404(MedicalImage, pk=pk, doctor=request.user)
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.image = image
            report.doctor = request.user
            report.save()
            report.transcript = transcribe_audio(report.audio.path)
            report.save()
            return redirect('review_transcript', report.pk)
    else:
        form = AudioUploadForm()
    return render(request, 'upload_audio.html', {'form': form, 'image': image})

@login_required
def review_transcript(request, pk):
    report = get_object_or_404(AudioReport, pk=pk, doctor=request.user)
    if request.method == 'POST':
        form = TranscriptForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.approved = True
            report.save()
            return redirect('doctor_images')
    else:
        form = TranscriptForm(instance=report)
    return render(request, 'review_transcript.html', {'form': form, 'report': report})

@login_required
def hospital_reports(request):
    if not request.user.role == 'hospital':
        return redirect('login')
    images = MedicalImage.objects.filter(hospital=request.user)
    return render(request, 'hospital_reports.html', {'images': images})
