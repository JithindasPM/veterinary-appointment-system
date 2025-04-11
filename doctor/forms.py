from django import forms
from .models import Doctor_Profile

from django import forms
from .models import Doctor_Profile

class Doctor_Profile_Form(forms.ModelForm):
    class Meta:
        model = Doctor_Profile
        fields = [
            'full_name',
            'email',
            'address',
            'phone_number',
            'profile_picture',
            'place',
            'qualification',
            'years_of_experience',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address',
                'rows': 3
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
                'maxlength': 10
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'place': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter place'
            }),
            'qualification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter qualification'
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years of experience',
                'min': 0
            }),
        }

