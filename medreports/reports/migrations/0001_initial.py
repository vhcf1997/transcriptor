from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('accounts', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='MedicalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='accounts.user')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='AudioReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(upload_to='audio/')),
                ('transcript', models.TextField(blank=True)),
                ('approved', models.BooleanField(default=False)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='reports.medicalimage')),
            ],
        ),
    ]
