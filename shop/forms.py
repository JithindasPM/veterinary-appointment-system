from django import forms
from shop.models import Product_Category

class Product_Category_Form(forms.ModelForm):
    class Meta:
        model = Product_Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a short description',
                'rows': 4
            }),
        }
