# Generated by Django 5.1.2 on 2025-01-12 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0007_alter_doctorprofile_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='experience',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='specialty',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
