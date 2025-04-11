from django.db import models
from django.conf import settings  

class Doctor_Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone_number = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='images', blank=True, null=True)
    place = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    is_approved=models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return self.full_name
    
