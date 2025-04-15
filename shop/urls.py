
from django.urls import path
from shop.views import Shop_View

urlpatterns = [
    
    path('shop', Shop_View.as_view(), name='shop'),
    
]
