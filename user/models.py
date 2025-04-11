from django.db import models
from django.conf import settings  
from doctor.models import Doctor_Profile


class PetOwner_Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return self.full_name
    
class Pet(models.Model):
    owner = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=30)  # Dog, Cat
    breed = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    pet_picture = models.ImageField(upload_to='pet_images', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.species})"
    
from django.db import models
from django.conf import settings

class Doctor_Appointment(models.Model):
    doctor = models.ForeignKey(Doctor_Profile, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    pet=models.ForeignKey(Pet,on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(null=True,blank=True)
    reason = models.TextField()
    is_confirmed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,null=True,blank=True)

    def __str__(self):
        return f"Appointment with {self.doctor.full_name} on {self.appointment_date}"

