# Generated by Django 5.0.3 on 2025-04-11 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_doctor_profile_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor_profile',
            name='consulting_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
