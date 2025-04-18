from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate,logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Sum 


from doctor.models import Doctor_Profile
from user.models import PetOwner_Profile
from user.models import Doctor_Appointment
from admins.models import User
from admins.models import WebsiteReview
from shop.models import Cart
from shop.models import Product


class Home_View(View):
    def get(self,request):
        return render(request,'index.html')
    

class Admin_View(View):
    def get(self,request):
        total_purchased = Cart.objects.filter(buy=True).aggregate(total=Sum('total_price'))['total'] or 0
        total_stock = Product.objects.aggregate(total=Sum('stock'))['total'] or 0
        user_count = User.objects.filter(user_type='user').count()
        doctor_count = User.objects.filter(user_type='doctor').count()
        appointment=Doctor_Appointment.objects.all().order_by('-id')[:2]
        all_order=Cart.objects.filter(buy=True).order_by('-id')[:2]
        return render(request,'admin.html',{'appointment':appointment,'all_order':all_order,'user_count':user_count,
                                            'doctor_count':doctor_count,'total_stock':total_stock,'total_purchased':total_purchased})


class Registration_View(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = form.cleaned_data['user_type']
            user.save()
            return redirect('login') 
        return render(request, 'registration.html', {'form': form})


class Login_View(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                if user.user_type == 'doctor':
                    try:
                        profile = Doctor_Profile.objects.get(user=user)
                        if not all([
                            profile.full_name,
                            profile.email,
                            profile.address,
                            profile.phone_number,
                            profile.place,
                            profile.qualification,
                            profile.years_of_experience,
                        ]):
                            return redirect('doctor_profile')  
                    except Doctor_Profile.DoesNotExist:
                        return redirect('doctor_profile') 
                    return redirect('doctor')
                elif user.user_type == 'user':
                    try:
                        profile = PetOwner_Profile.objects.get(user=user)
                        if not all([
                            profile.full_name,
                            profile.email,
                            profile.phone_number,
                            profile.address,
                        ]):
                            return redirect('user_profile') 
                    except PetOwner_Profile.DoesNotExist:
                        return redirect('user_profile')
                    return redirect('user') 
                else:
                    return redirect('admin')
        return render(request, 'login.html', {'form': form})

class Logout_View(View):
    def get(self, request):
        logout(request)
        return redirect('home') 
    
class All_Doctor_Admin_View(View):
    def get(self,request):
        return render(request,'all_doctor_admin.html')
    

class Toggle_Doctor_Approval_View(View):
    def post(self, request, doctor_id):
        doctor = get_object_or_404(User, id=doctor_id, user_type='doctor')
        doctor.is_approved = not doctor.is_approved
        doctor.save()
        status = "approved" if doctor.is_approved else "unapproved"
        messages.success(request, f"Doctor {doctor.username} has been {status}.")
        return redirect('all_doctor_admin')  


class All_Users_View(View):
    def get(self,request):
        users=User.objects.filter(user_type='user')
        return render(request,'all_users.html',{'users':users})
    
import groq
import re

client = groq.Client(api_key="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")


def get_groq_response(user_input):
    """
    Communicate with the GROQ chatbot to get a response based on user input.
    """
    system_prompt = {
        "role": "system",
        "content": "You are a helpful assistant.Keep your answers short and to the point ."
    }

    chat_history = [system_prompt]

    # Append user input to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Get response from GROQ API
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=100,
        temperature=1.2
    )

    response = chat_completion.choices[0].message.content
    print(response)
    # Format response (convert *bold* to <b>bold</b>)
    response = re.sub(r'\\(.?)\\*', r'<b>\1</b>', response)

    return response

from .forms import Groq_Chat_Form
    
class Groq_View(View):
    def get(self, request, *args, **kwargs):
        form = Groq_Chat_Form()
        # Start with fresh chat history
        request.session['chat_history'] = []
        return render(request, 'chat.html', {'form': form, 'chat_history': []})
    
    def post(self, request, *args, **kwargs):
        form = Groq_Chat_Form(request.POST)
        user_input = request.POST.get('text')

        if not user_input:
            message = 'Please enter a message'
            return render(request, 'chat.html', {
                'error': message, 
                'form': form, 
                'chat_history': request.session.get('chat_history', [])
            })

        # Get response from Groq
        chatbot_response = get_groq_response(user_input)
        
        # Get existing chat history or initialize empty list
        chat_history = request.session.get('chat_history', [])
        
        # Add new messages to history
        chat_history.append({
            'user': user_input,
            'bot': chatbot_response
        })
        
        # Update session
        request.session['chat_history'] = chat_history
        request.session.modified = True
        
        form = Groq_Chat_Form()
        return render(request, 'chat.html', {
            'form': form, 
            'chat_history': chat_history
        })
        
class All_Booking_Admin_View(View):
    def get(self, request):
        paid_appointments = Doctor_Appointment.objects.filter(is_paid=True).order_by('-created_at')
        paginator = Paginator(paid_appointments, 10)  # Show 5 per page
        page_number = request.GET.get('page')
        paid_appointments = paginator.get_page(page_number)

        return render(request, 'all_bookind_admin.html', {'paid_appointments': paid_appointments})
    


@login_required
def website_reviews(request):
    reviews = WebsiteReview.objects.all().order_by('-created_at')  # Get all reviews

    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Prevent duplicate reviews by the same user
        if WebsiteReview.objects.filter(user=request.user).exists():
            review = WebsiteReview.objects.get(user=request.user)
            review.rating = rating
            review.comment = comment
            review.save()
        else:
            WebsiteReview.objects.create(user=request.user, rating=rating, comment=comment)

        return redirect('website_reviews')  # Redirect to avoid duplicate form submissions

    avg_rating = WebsiteReview.get_average_rating()  # Get average rating

    return render(request, 'website_reviews.html', {'reviews': reviews, 'avg_rating': avg_rating})