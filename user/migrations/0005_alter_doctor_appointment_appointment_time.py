# Generated by Django 5.0.3 on 2025-04-11 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_doctor_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor_appointment',
            name='appointment_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
