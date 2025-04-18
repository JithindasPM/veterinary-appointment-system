# Generated by Django 5.0.3 on 2025-04-09 11:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor_Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=10)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='images')),
                ('place', models.CharField(max_length=100)),
                ('qualification', models.CharField(max_length=100)),
                ('years_of_experience', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
