
from django.urls import path
from shop.views import Shop_View
from shop.views import Main_Shop_View
from shop.views import Product_Category_Add_View

urlpatterns = [
    
    path('shop', Shop_View.as_view(), name='shop'),
    path('main_shop', Main_Shop_View.as_view(), name='main_shop'),
    path('main_shop', Product_Category_Add_View.as_view(), name='main_shop'),
    
    
]
