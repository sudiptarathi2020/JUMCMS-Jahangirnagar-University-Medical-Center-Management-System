# Generated by Django 4.0.3 on 2024-10-30 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('completed', 'Completed')], max_length=20)),
                ('medical_test', models.CharField(choices=[('CBC', 'Complete Blood Count (CBC)'), ('BMP', 'Basic Metabolic Panel (BMP)'), ('Urinalysis', 'Urinalysis'), ('Xray', 'X-ray'), ('ECG', 'Electrocardiogram(ECG)')], default=False, max_length=200)),
                ('lab_technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_appointments', to='users.labtechnician')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DoctorAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('completed', 'Completed')], max_length=20)),
                ('reason', models.CharField(default=False, max_length=200)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointments', to='users.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
