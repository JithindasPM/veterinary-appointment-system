from django.db import models
from admins.models import User

# Create your models here.

class Product_Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Product_Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.conf import settings
from django.db import models
from decimal import Decimal  # Import Decimal to handle currency values accurately

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference custom user model
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    buy=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        # Update total_price before saving the cart object
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

