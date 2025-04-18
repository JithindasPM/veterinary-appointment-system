
from django.urls import path
from . import views


from shop.views import Shop_View
from shop.views import Main_Shop_View
from shop.views import Category_Add_View
from shop.views import Category_Update_View
from shop.views import Category_Delete_View
from shop.views import Product_Add_View
from shop.views import Product_Update_View
from shop.views import Product_Delete_View
from shop.views import Product_Detail_View
from .views import AddToCartView
from shop.views import Cart_Delete_View


urlpatterns = [
    
    path('shop', Shop_View.as_view(), name='shop'),
    path('main_shop', Main_Shop_View.as_view(), name='main_shop'),
    path('category_add', Category_Add_View.as_view(), name='category_add'),
    path('category_update/<int:pk>/', Category_Update_View.as_view(), name='category_update'),
    path('category_delete/<int:pk>/', Category_Delete_View.as_view(), name='category_delete'),
    path('product_add', Product_Add_View.as_view(), name='product_add'),
    path('products_update/<int:pk>/', Product_Update_View.as_view(), name='products_update'),
    path('products_delete/<int:pk>/', Product_Delete_View.as_view(), name='products_delete'),
    path('products_detail/<int:pk>/', Product_Detail_View.as_view(), name='products_detail'),
    path('cart/add/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart_delete/<int:pk>/', Cart_Delete_View.as_view(), name='cart_delete'),
    path('checkout_product/<int:item_id>/', views.checkout_product, name='checkout_product'),
path('success_payment/', views.success_payment, name='success_payment'),
    
]
