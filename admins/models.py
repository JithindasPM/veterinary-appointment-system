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
    
    

class WebsiteReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who submits the review
    rating = models.PositiveIntegerField(default=1)  # Rating between 1-5
    comment = models.TextField(blank=True, null=True)  # Optional review text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the review

    def __str__(self):
        return f"{self.user.username} - {self.rating}⭐"

    @classmethod
    def get_average_rating(cls):
        avg = cls.objects.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0  # Get average rating with 1 decimal place