from django import forms
from django.contrib.auth.forms import UserCreationForm
from admins.models import User


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=[('doctor', 'doctor'), ('user', 'user')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')

class Groq_Chat_Form(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control my-1',
            'placeholder': 'Ask anything . . .',
            'style': 'background-color:rgba(255, 255, 255, 0.4); height: 100px;',  # Adjust height
            'rows': 3,  # Set initial rows
        })
    )
    
    
from django import forms

class PasswordResetForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username',
        'class': 'form-control'
    }))

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter OTP',
        'class': 'form-control'
    }))


class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter new password',
        'class': 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm new password',
        'class': 'form-control'
    }))