# Generated by Django 5.0.3 on 2025-04-11 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0004_doctor_profile_consulting_fee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor_profile',
            name='consulting_fee',
        ),
    ]
