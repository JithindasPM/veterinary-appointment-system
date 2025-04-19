from django import forms
from user.models import PetOwner_Profile
from user.models import Pet

from .models import Doctor_Appointment

class PetOwner_Profile_Form(forms.ModelForm):
    class Meta:
        model = PetOwner_Profile
        fields = [
            'full_name',
            'email',
            'phone_number',
            'address',
            'profile_picture',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number', 'maxlength': '10'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class Pet_Form(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'pet_picture']
        
        labels = {
            'name': 'Pet Name',
            'species': 'Species',
            'breed': 'Breed',
            'age': 'Age (years)',
            'pet_picture': 'Pet Photo'
        }
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter pet name'
            }),
            'species': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., Dog, Cat'
            }),
            'breed': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter breed'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter age in years'
            }),
            'pet_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
        

class Appointment_Form(forms.ModelForm):
    class Meta:
        model = Doctor_Appointment
        fields = ['appointment_date', 'reason', 'pet']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pet': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)


from django import forms
from .models import Adopter

class AdopterForm(forms.ModelForm):
    class Meta:
        model = Adopter
        fields = [ 'phone', 'email', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
                'rows': 3
            }),
        }
