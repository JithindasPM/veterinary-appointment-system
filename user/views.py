from django.shortcuts import render,redirect,get_object_or_404
from django.views import View

# Create your views here.


from user.models import PetOwner_Profile
from user.models import Pet
from user.models import Doctor_Appointment
from admins.models import User
from doctor.models import Doctor_Profile

from user.forms import PetOwner_Profile_Form
from user.forms import Pet_Form
from user.forms import Appointment_Form



# class User_View(View):
#     def get(self,request):
#         return render(request,'user.html')

class User_View(View):
    def get(self, request):
        form = Pet_Form()
        pets = Pet.objects.filter(owner=request.user)
        return render(request, 'user.html', {'form': form,'pets':pets})
    
    def post(self, request):
        form = Pet_Form(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('user')
        print(request.user)
        pets = Pet.objects.filter(owner=request.user)
        return render(request, 'user.html', {'form': form, 'pets': pets})
    
class Pet_Update_View(View):
    def get(self, request, pk):
        pet = get_object_or_404(Pet, pk=pk, owner=request.user)
        form = Pet_Form(instance=pet)
        return render(request, 'pet_update.html', {'form': form, 'pet': pet})

    def post(self, request, pk):
        pet = get_object_or_404(Pet, pk=pk, owner=request.user)
        form = Pet_Form(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('user') 
        return render(request, 'pet_update.html', {'form': form, 'pet': pet})
    
class Pet_Delete_View(View):
    def get(self, request, pk):
        pet = get_object_or_404(Pet, pk=pk, owner=request.user)
        pet.delete()
        return redirect('user')


class User_Profile_Create_View(View):
    def get(self, request):
        form = PetOwner_Profile_Form()
        return render(request, 'user_profile.html', {'form': form})
    
    def post(self, request):
        form = PetOwner_Profile_Form(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('doctor') 
        return render(request, 'user_profile.html', {'form': form})
    
class User_Profile_Updation_View(View):
    def get(self,request):
        profile=get_object_or_404(PetOwner_Profile,user=request.user)
        form=PetOwner_Profile_Form(instance=profile)
        return render(request, 'user_profile.html', {'form': form})
    def post(self,request):
        profile=get_object_or_404(PetOwner_Profile,user=request.user)
        form=PetOwner_Profile_Form(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user')
        return render(request, 'user_profile.html', {'form': form})
    
class All_Doctor_View(View):
    def get(self,request):
        doctors=User.objects.filter(user_type='doctor', is_approved=True)
        return render(request,'all_doctor.html',{'doctors':doctors})
    

from django.http import Http404

def book_appointment(request, doctor_id):
    try:
        doctor_obj=User.objects.get(id=doctor_id)
        doctor = Doctor_Profile.objects.get(user=doctor_obj)
    except Doctor_Profile.DoesNotExist:
        # You can log this or show a message
        raise Http404("Doctor not found.")

    if request.method == 'POST':
        form = Appointment_Form(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = request.user
            appointment.save()
            return redirect('all_appointment')  
    else:
        form = Appointment_Form(user=request.user)  

    return render(request, 'book_appointment.html', {
        'form': form,
        'doctor': doctor
    })

    
class All_Appointment_View(View):
    def get(self,request):
        appointment=Doctor_Appointment.objects.filter(patient=request.user).order_by('-id')
        return render(request,'all_appointment.html',{'appointment':appointment})

class Appointment_Delete_View(View):
    def post(self,request,pk):
        data=get_object_or_404(Doctor_Appointment,pk=pk,patient=request.user)
        data.delete()
        return redirect('all_appointment')


import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor_Appointment
from django.views.generic import TemplateView

class CreatePaymentView(View):
    def get(self, request, appointment_id):
        appointment = get_object_or_404(Doctor_Appointment, id=appointment_id, is_paid=False)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Razorpay expects the amount in paise, so ₹500 = 50000 paise
        payment = client.order.create({
            'amount': 50000,
            'currency': 'INR',
            'payment_capture': '1'
        })

        appointment.razorpay_order_id = payment['id']
        appointment.save()

        context = {
            'appointment': appointment,
            'payment': payment,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'amount': 50000
        }

        return render(request, 'payment_page.html', context)

    @csrf_exempt
    def post(self, request, appointment_id):
        appointment = get_object_or_404(Doctor_Appointment, id=appointment_id)
    
        appointment.is_paid = True
        appointment.amount = 500  # Save ₹500 after payment
        appointment.save()
    
        return redirect('appointment_success')
