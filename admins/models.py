from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=[
        ('doctor', 'doctor'),
        ('user', 'user')
    ])
    is_approved=models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return self.username
    
    
