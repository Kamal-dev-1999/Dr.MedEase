# Generated by Django 5.1.2 on 2025-01-12 04:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_patientprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='patient_contact',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='patient_name',
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='patients.patientprofile'),
            preserve_default=False,
        ),
    ]
