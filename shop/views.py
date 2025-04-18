from django.shortcuts import render,redirect,get_object_or_404
from django.views import View


from shop.models import Product_Category
from shop.models import Product
from shop.models import Cart

from shop.forms import Product_Category_Form
from shop.forms import Product_Form


# Create your views here.

    
class Shop_View(View):
    def get(self,request):
        return render(request,'shop.html')
    
class Main_Shop_View(View):
    def get(self, request):
        product = Product.objects.filter(stock__gt=0).order_by('-id') 
        return render(request, 'main_shop.html', {'product': product})

class Category_Add_View(View):
    template_name = 'category.html' 

    def get(self, request):
        form = Product_Category_Form()
        category=Product_Category.objects.all()
        return render(request, self.template_name, {'form': form,'category':category})

    def post(self, request):
        category=Product_Category.objects.all()
        form = Product_Category_Form(request.POST)
        if form.is_valid():
            form.save()
            form = Product_Category_Form()
        return render(request, self.template_name, {'form': form,'category':category})

class Category_Update_View(View):
    template_name = 'category.html'

    def get(self, request, pk):
        data = get_object_or_404(Product_Category, pk=pk)
        form = Product_Category_Form(instance=data)
        category=Product_Category.objects.all()
        return render(request, self.template_name, {'form': form, 'category': category})

    def post(self, request, pk):
        category=Product_Category.objects.all()
        data = get_object_or_404(Product_Category, pk=pk)
        form = Product_Category_Form(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('category_add')  
        return render(request, self.template_name, {'form': form, 'category': category})
    
class Category_Delete_View(View):

    def get(self, request, pk):
        category = get_object_or_404(Product_Category, pk=pk)
        category.delete()
        return redirect('category_add') 

class Product_Add_View(View):
    def get(self, request):
        form = Product_Form()
        product=Product.objects.all().order_by('-id')
        return render(request, 'product.html', {'form': form,'product':product})

    def post(self, request):
        product=Product.objects.all().order_by('-id')
        form = Product_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = Product_Form()
        return render(request, 'product.html', {'form': form,'product':product})
    
class Product_Update_View(View):
    def get(self, request, pk):
        data = get_object_or_404(Product, id=pk)
        form = Product_Form(instance=data)
        product = Product.objects.all().order_by('-id')
        return render(request, 'product.html', {'form': form, 'product': product})

    def post(self, request, pk):
        data = get_object_or_404(Product, id=pk)
        form = Product_Form(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('product_add')  


class Product_Delete_View(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return redirect('product_add')
    
class Product_Detail_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        product=Product.objects.get(id=id)
        return render(request,'product_detail.html',{'product':product})
        
# views.py
class AddToCartView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST.get('quantity', 1))

        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return redirect('cart')  

def cart_view(request):
    # Get the logged-in user's cart items
    cart_items = Cart.objects.filter(user=request.user,buy=False).order_by('-id')

    # Calculate the total price of the cart
    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
 
 
class Cart_Delete_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        product=Cart.objects.get(id=id)
        product.delete()
        return redirect('cart')
    
import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart
from decimal import Decimal

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def checkout_product(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user, buy=False)

    # Amount should be in paise
    amount = int(cart_item.total_price * 100)

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency='INR',
                                                       payment_capture='1'))

    # Store order_id temporarily in session (or you could make a model if needed)
    request.session['razorpay_order_id'] = razorpay_order['id']
    request.session['cart_item_id'] = item_id

    context = {
        'cart_item': cart_item,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order['id'],
        'amount': amount,
        'currency': 'INR',
    }

    return render(request, 'checkout.html', context)

from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def success_payment(request):
#     cart_item_id = request.session.get('cart_item_id')
#     if cart_item_id:
#         cart_item = Cart.objects.filter(id=cart_item_id, user=request.user).first()
#         if cart_item:
#             cart_item.buy = True
#             cart_item.save()
#     return redirect('cart')  # Or a success page

from django.shortcuts import redirect
from .models import Cart, Product
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def success_payment(request):
    cart_item_id = request.session.get('cart_item_id')
    
    if cart_item_id:
        cart_item = Cart.objects.filter(id=cart_item_id, user=request.user).first()
        
        if cart_item:
            # Decrease stock from the product
            product = cart_item.product
            if product.stock >= cart_item.quantity:
                product.stock -= cart_item.quantity
                product.save()

                # Mark as bought
                cart_item.buy = True
                cart_item.save()
            else:
                # Optional: You can add a message if stock is insufficient
                print("Not enough stock!")

    return redirect('cart')  # Or a dedicated success page

