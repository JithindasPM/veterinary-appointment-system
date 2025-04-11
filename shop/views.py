from django.shortcuts import render
from django.views import View

# Create your views here.


class Shop_View(View):
    def get(self,request):
        return render(request,'shop.html')