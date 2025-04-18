from django.shortcuts import render,redirect
from django.views import View
from shop.forms import Product_Category_Form


# Create your views here.

    
class Shop_View(View):
    def get(self,request):
        return render(request,'shop.html')
    
class Main_Shop_View(View):
    def get(self,request):
        return render(request,'main_shop.html')
    

class Product_Category_Add_View(View):
    template_name = 'category.html' 

    def get(self, request):
        form = Product_Category_Form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = Product_Category_Form(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('category_list') 
        return render(request, self.template_name, {'form': form})
