from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
# from django.contrib.auth import get_user_model
# User = get_user_model() 

# Create your views here.


from user.models import PetOwner_Profile
from user.models import Pet
from user.models import Doctor_Appointment
from doctor.models import Doctor_Profile
from shop.models import Cart

from user.forms import PetOwner_Profile_Form
from user.forms import Pet_Form
from user.forms import Appointment_Form


class User_View(View):
    def get(self, request):
        form = Pet_Form()
        pets = Pet.objects.filter(owner=request.user)
        appointment=Doctor_Appointment.objects.filter(patient=request.user).order_by('-id')[:2]
        order=Cart.objects.filter(user=request.user,buy=True)[:2]
        return render(request, 'user.html', {'form': form,'pets':pets,'appointment':appointment,'order':order})
    
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
            return redirect('user') 
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
    

# class All_Doctor_View(View):
#     def get(self,request):
#         doctors=User.objects.filter(user_type='doctor', is_approved=True)
#         return render(request,'all_doctor.html',{'doctors':doctors})

class All_Doctor_View(View):
    def get(self, request):
        # Import directly from the admins app
        from admins.models import User
        doctors = User.objects.filter(user_type='doctor', is_approved=True)
        return render(request, 'all_doctor.html', {'doctors': doctors})
    

from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings

def book_appointment(request, doctor_id):
    try:
        from admins.models import User
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
            send_mail(
                subject="📅 New Appointment via VetWizard",
                message=(
                    f"Hello Dr. {doctor.full_name},\n\n"
                    f"You have received a new appointment through VetWizard!\n\n"
                    f"👤 Patient: {request.user.username}\n"
                    f"📅 Date: {appointment.appointment_date}\n"
                    f"🐾 Pet: {appointment.pet}\n"
                    f"📝 Reason: {appointment.reason}\n\n"
                    f"Please log in to VetWizard to confirm or manage the appointment.\n\n"
                    f"Thank you,\n\n"
                    f"🐾 VetWizard Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[doctor.email],
                fail_silently=False,
            )
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


class ToggleAdoptView(View):
    def post(self, request, pet_id):
        # Get the pet object by ID
        pet = get_object_or_404(Pet, id=pet_id)

        # Toggle the 'adopt' status
        pet.adopt = not pet.adopt
        pet.save()

        # Redirect to the pet list or details page
        return redirect('user')  # Change 'pet_list' to your actual pet list view name


from django.contrib.auth.models import User  # default User model

from django.contrib.auth import get_user_model  # Use get_user_model() to get the custom User model

class Adoption_View(View):
    def get(self, request):
        pets = Pet.objects.filter(adopt=True).exclude(owner=request.user)
        pet_with_owners = []

        # Get the custom User model
        User = get_user_model()

        for pet in pets:
            try:
                # Step 1: Match pet.owner (name string) with a User.username
                user = User.objects.get(username=pet.owner)

                # Step 2: Get PetOwner_Profile connected to that user
                owner_profile = PetOwner_Profile.objects.get(user=user)
            except (User.DoesNotExist, PetOwner_Profile.DoesNotExist):
                owner_profile = None

            pet_with_owners.append({
                'pet': pet,
                'owner': owner_profile
            })

        return render(request, 'adopt.html', {'pet_with_owners': pet_with_owners})

from .forms import AdopterForm
class AdopterDetailsView(View):
    def get(self, request, pet_id):
        pet = Pet.objects.get(id=pet_id)
        owner_username = pet.owner
        from admins.models import User
        user_obj = User.objects.get(username=owner_username)
        owner_profile = PetOwner_Profile.objects.get(user=user_obj)
        
        form = AdopterForm()
        return render(request, 'adopter_form.html', {'form': form, 'pet': pet})

    def post(self, request, pet_id):
        form = AdopterForm(request.POST)
        
        pet = Pet.objects.get(id=pet_id)
        owner_username = pet.owner
        from admins.models import User
        user_obj = User.objects.get(username=owner_username)
        owner_profile = PetOwner_Profile.objects.get(user=user_obj)
        
        if form.is_valid():
            # Save adopter details in a new Adopter model or update if necessary
            adopter = form.save(commit=False)
            adopter.pet = Pet.objects.get(id=pet_id)
            adopter.name = request.user.username
            adopter.save()

            # Set the pet's adoption status
            pet = Pet.objects.get(id=pet_id)
            pet.adopt = True  # Assuming the pet is now adopted
            pet.save()
            
            send_mail(
                subject="🐾 VetWizard - New Adoption Request!",
                message=(
                    f"Hello {owner_profile.full_name},\n\n"
                    f"You have received a new adoption request for your pet \"{pet.name}\" on VetWizard.\n\n"
                    f"Requester Username: {request.user}\n\n"
                    "Please log in to your VetWizard account to review the request.\n\n"
                    "Thank you,\n\nTeam VetWizard 🐶"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,  # ✅ change to your email
                recipient_list=[owner_profile.email],
                fail_silently=False,
            )

            return redirect('my_adoption_requests') 
        
from .models import Pet, Adopter
from django.core.mail import send_mail
from django.conf import settings

class AdoptionRequestsView(View):
    def get(self, request):
        # Get all pets owned by the logged-in user
        pets = Pet.objects.filter(owner=request.user)  # Adjust this depending on how owner is stored
        
        # Get all adoption requests related to these pets
        adoption_requests = Adopter.objects.filter(pet__in=pets)
        
        # Render the requests to the template
        return render(request, 'adoption_requests.html', {'adoption_requests': adoption_requests})

class ToggleAdoptionView(View):
    def post(self, request, adopter_id):
        adopter = Adopter.objects.get(id=adopter_id)
        
        adopter.is_approved = not adopter.is_approved  # Toggle the approval status
        adopter.save()
        
        if adopter.is_approved:
            subject = "🐾 VetWizard - Adoption Request Approved!"
            message = (
                f"Hello {adopter.name},\n\n"
                f"Great news! Your adoption request for the pet \"{adopter.pet.name}\" has been approved 🎉\n\n"
                f"Our team or the pet owner will contact you shortly.\n\n"
                "Thank you for choosing VetWizard.\n\n"
                "Warm regards,\n\nTeam VetWizard 🐶"
            )
        else:
            subject = "🐾 VetWizard - Adoption Request Rejected"
            message = (
                f"Hello {adopter.name},\n\n"
                f"We're sorry to inform you that your adoption request for \"{adopter.pet.name}\" was not approved.\n\n"
                "Feel free to explore other adorable pets available for adoption on VetWizard.\n\n"
                "Warm regards,\n\nTeam VetWizard 🐾"
            )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[adopter.email],
            fail_silently=False,
        )
        
        return redirect('adoption_requests')  # Redirect back to the adoption requests page

class User_Orders(View):
    def get(self,request):
        order=Cart.objects.filter(user=request.user,buy=True)
        return render(request,'user_order.html',{'order':order})
    
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .models import Adopter, PetOwner_Profile

class MyAdoptionRequestsView(ListView):
    model = Adopter
    template_name = 'my_adoption_request.html'
    context_object_name = 'adoption_requests'

    def get_queryset(self):
        return Adopter.objects.filter(name=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        adoption_data = []

        for adopter in context['adoption_requests']:
            try:
                User = get_user_model()
                user = User.objects.get(username=adopter.pet.owner)
                owner_profile = PetOwner_Profile.objects.get(user=user)
            except (User.DoesNotExist, PetOwner_Profile.DoesNotExist):
                owner_profile = None

            adoption_data.append({
                'adopter': adopter,
                'owner': owner_profile,
            })

        context['adoption_data'] = adoption_data
        return context


from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Adopter

class DeleteAdoptionRequestView(View):
    def post(self, request, pk):
        adoption_request = get_object_or_404(Adopter, pk=pk, name=request.user.username)
        adoption_request.delete()
        messages.success(request, "Adoption request deleted successfully.")
        return redirect('my_adoption_requests')
