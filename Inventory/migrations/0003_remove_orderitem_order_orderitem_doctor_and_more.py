# Generated by Django 5.1.2 on 2024-11-08 16:01

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0001_initial'),
        ('Inventory', '0002_inventoryitem_doctor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Doctor.doctorprofile'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='expected_delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='notes',
            field=models.TextField(blank=True, help_text='Additional order notes or instructions'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='Inventory.supplier'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='time_of_order',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_items', to='Inventory.inventoryitem'),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
