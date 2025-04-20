from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib import messages

# Create your views here.


from doctor.forms import Doctor_Profile_Form

from doctor.models import Doctor_Profile
from user.models import Doctor_Appointment


class Doctor_View(View):
    def get(self, request):
        doctor_profile = get_object_or_404(Doctor_Profile, user=request.user)
        appointments = Doctor_Appointment.objects.filter(doctor=doctor_profile).order_by('-id')[:2]

        appo = Doctor_Appointment.objects.filter(doctor=doctor_profile)

        patient_count = appo.values('patient').distinct().count()
        total_bookings = appo.count()
        confirmed_bookings = appo.filter(is_paid=True).count()
        non_confirmed_bookings = appo.filter(is_paid=True).count()

        show_modal = False
        if request.user.user_type == 'doctor' and not request.user.is_approved:
            show_modal = True

        return render(request, 'doctor.html', {
            'show_modal': show_modal,
            'appointments': appointments,
            'patient_count': patient_count,
            'total_bookings': total_bookings,
            'confirmed_bookings': confirmed_bookings,
            'non_confirmed_bookings':non_confirmed_bookings
        })



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
from user.models import PetOwner_Profile
def toggle_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Doctor_Appointment, id=appointment_id)
    appointment.is_confirmed = not appointment.is_confirmed
    appointment.save()
    return redirect('appointment_doctor')


from django.core.mail import send_mail
from django.conf import settings

def set_appointment_time(request, appointment_id):
    appointment = get_object_or_404(Doctor_Appointment, id=appointment_id)
    
    user_obj = PetOwner_Profile.objects.get(user=appointment.patient)
    new_time = request.POST.get('appointment_time')

    if new_time:
        appointment.appointment_time = new_time
        appointment.is_confirmed = True  # Mark appointment as confirmed
        appointment.save()

        # Email details
        subject = "🐾 VetWizard - Your Appointment is Confirmed!"
        message = (
            f"Hello {user_obj.full_name},\n\n"
            f"Your appointment with Dr. {appointment.doctor.full_name} has been approved.\n"
            f"📅 Date: {appointment.appointment_date}\n"
            f"⏰ Time: {appointment.appointment_time}\n"
            f"🐶 Pet: {appointment.pet.name}\n\n"
            f"Please be on time and bring all relevant documents if needed.\n\n"
            f"Thank you for using VetWizard!\n\n"
            f"Warm regards,\n\nTeam VetWizard 🐾"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_obj.email],
            fail_silently=False,
        )

    return redirect('appointment_doctor')
