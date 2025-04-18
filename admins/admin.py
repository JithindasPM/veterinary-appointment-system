from django.contrib import admin

# Register your models here.

from .models import User
from user.models import Doctor_Appointment
from shop.models import Cart

admin.site.register(User)
admin.site.register(Doctor_Appointment)
admin.site.register(Cart)


