from django import forms

from shop.models import Product_Category
from shop.models import Product

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

class Product_Form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'stock', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Enter product description'}),
            'category': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select product category'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product price'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock quantity'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }