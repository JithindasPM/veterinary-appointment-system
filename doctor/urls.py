
from django.urls import path

from doctor.views import Doctor_View
from doctor.views import Doctor_Profile_Create_View
from doctor.views import Doctor_Profile_Update_View
from doctor.views import Appointment_Doctor_View
from doctor.views import toggle_appointment_status
from doctor.views import set_appointment_time


urlpatterns = [
    
    path('doctor/', Doctor_View.as_view(), name='doctor'),
    path('doctor_profile/', Doctor_Profile_Create_View.as_view(), name='doctor_profile'),
    path('doctor_profile_update/', Doctor_Profile_Update_View.as_view(), name='doctor_profile_update'),
    path('appointment_doctor/', Appointment_Doctor_View.as_view(), name='appointment_doctor'),
    path('appointment/toggle/<int:appointment_id>/', toggle_appointment_status, name='toggle_appointment_status'),
    path('appointment/time/<int:appointment_id>/', set_appointment_time, name='set_appointment_time'),
    
    
]
