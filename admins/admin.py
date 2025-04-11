from django.contrib import admin

# Register your models here.

from .models import User
from user.models import Doctor_Appointment

admin.site.register(User)
admin.site.register(Doctor_Appointment)

