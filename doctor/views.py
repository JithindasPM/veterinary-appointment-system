from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib import messages

# Create your views here.


from doctor.forms import Doctor_Profile_Form

from doctor.models import Doctor_Profile
from user.models import Doctor_Appointment


class Doctor_View(View):
    def get(self, request):
        show_modal = False
        if request.user.user_type == 'doctor' and not request.user.is_approved:
            show_modal = True
        return render(request, 'doctor.html', {'show_modal': show_modal})


class Doctor_Profile_Create_View(View):
    def get(self, request):
        form = Doctor_Profile_Form()
        return render(request, 'doctor_profile.html', {'form': form})
    
    def post(self, request):
        form = Doctor_Profile_Form(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            request.user.refresh_from_db()
            if not request.user.is_approved:
                messages.warning(request, "Your profile is waiting for admin approval.")
                return redirect('home')
            else:
                return redirect('doctor')
        return render(request, 'doctor_profile.html', {'form': form})

class Doctor_Profile_Update_View(View):
    def get(self, request):
        profile = get_object_or_404(Doctor_Profile, user=request.user)
        form = Doctor_Profile_Form(instance=profile)
        return render(request, 'doctor_profile.html', {'form': form})

    def post(self, request):
        profile = get_object_or_404(Doctor_Profile, user=request.user)
        form = Doctor_Profile_Form(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('doctor')
        else:
            return render(request, 'doctor_profile.html', {'form': form})
    
class Appointment_Doctor_View(View):
    def get(self, request):
        doctor_profile = get_object_or_404(Doctor_Profile, user=request.user)
        appointments = Doctor_Appointment.objects.filter(doctor=doctor_profile).order_by('-id')
        return render(request, 'appointment_doctor.html', {'appointment': appointments})
    
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def toggle_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Doctor_Appointment, id=appointment_id)
    appointment.is_confirmed = not appointment.is_confirmed
    appointment.save()
    return redirect('appointment_doctor')


def set_appointment_time(request, appointment_id):
    appointment = get_object_or_404(Doctor_Appointment, id=appointment_id)
    new_time = request.POST.get('appointment_time')
    if new_time:
        appointment.appointment_time = new_time
        appointment.save()
    return redirect('appointment_doctor')
