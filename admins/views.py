from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate,logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


from doctor.models import Doctor_Profile
from user.models import PetOwner_Profile
from .models import User

class Home_View(View):
    def get(self,request):
        return render(request,'index.html')
    

class Admin_View(View):
    def get(self,request):
        return render(request,'admin.html')


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
        doctors=User.objects.filter(user_type='doctor').order_by('-id')
        return render(request,'all_doctor_admin.html',{'doctors':doctors})
    

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