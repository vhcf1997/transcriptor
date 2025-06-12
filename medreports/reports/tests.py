from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import MedicalImage, AudioReport
from django.core.files.uploadedfile import SimpleUploadedFile

class ModelTests(TestCase):
    def setUp(self):
        self.doctor = get_user_model().objects.create_user(username='d', password='x', role='doctor')
        self.hospital = get_user_model().objects.create_user(username='h', password='x', role='hospital')

    def test_create_image(self):
        img = SimpleUploadedFile('test.png', b'\x00', content_type='image/png')
        m = MedicalImage.objects.create(hospital=self.hospital, doctor=self.doctor, image=img)
        self.assertEqual(m.hospital, self.hospital)

class ViewTests(TestCase):
    def test_login_required(self):
        resp = self.client.get('/doctor/images/')
        self.assertEqual(resp.status_code, 302)

    def test_doctor_only_access(self):
        self.client.login(username='h', password='x')
        resp = self.client.get('/doctor/images/')
        self.assertEqual(resp.status_code, 302)

    def test_doctor_access_success(self):
        self.client.login(username='d', password='x')
        resp = self.client.get('/doctor/images/')
        self.assertEqual(resp.status_code, 200)
