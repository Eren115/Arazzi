from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .cart import Cart
from .forms import AddToCartForm, CheckoutForm
from django.contrib import messages
import stripe
from django.conf import settings
from .utillities import checkout
from django.http import JsonResponse, HttpResponse


import json



def frontpage(request):
    cart = Cart(request)
    remove_from_cart = request.GET.get('remove_from_cart', '')
    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('frontpage')
    
    return render(request, "core/index.html", {'cart': cart})




def gallery(request):
    products = Product.objects.all()
    cart = Cart(request)
    remove_from_cart = request.GET.get('remove_from_cart', '')
    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('gallery')

    context = {
        'products': products,
        'cart': cart,
    }

    

    

    return render(request, "core/gallery.html", context)



def rem(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        
        product_id = request.POST.get('product_id')
        print(product_id)
        if product_id:
            cart.remove(product_id)
            return HttpResponse('')
    return HttpResponse('')
    

def cc(request, slug):
    cart = Cart(request)
    if request.method == 'GET':
        serialized_cart = []    
        for item in cart:
            product_dict = {
                'id': item['id'],   
                'get_thumbnail': item['product'].get_thumbnail(),
                'title': item['product'].title,
                'quantity': item['quantity'],
                'total_price': item['total_price'],
                'slug': item['product'].slug,
                
            }
            
            serialized_cart.append(product_dict)
        return HttpResponse(json.dumps(serialized_cart))
       

def csn(request):
    cart = Cart(request)
    if request.method == 'GET':
        serialized_cart = []    
        for item in cart:
            product_dict = {
                'id': item['id'],   
                'get_thumbnail': item['product'].get_thumbnail(),
                'title': item['product'].title,
                'quantity': item['quantity'],
                'total_price': item['total_price'],
                'slug': item['product'].slug,
                
            }
            
            serialized_cart.append(product_dict)
        return HttpResponse(json.dumps(serialized_cart))


def addToCart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)

    

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        cart.add(product_id=product.id, quantity=quantity, update_quantity=True)
        return redirect('productPage', slug)
    else:
        print('something went wrong')


    


def removeFromCart(request, slug):
    cart = Cart(request)

    if request.method == 'GET':
        remove_from_cart = request.GET.get('remove_from_cart', '')
        slug = request.GET.get('slug', '')
        if remove_from_cart:
            cart.remove(remove_from_cart)
        serialized_cart = []    
        for item in cart:
            product = item['product']
            product_dict = {
                'id': item['id'],   
                'get_thumbnail': item['product'].get_thumbnail(),
                'title': item['product'].title,
                'quantity': item['quantity'],
                'total_price': item['total_price'],
                
            }
            
            
            serialized_cart.append(product_dict)
            
    return HttpResponse(json.dumps(serialized_cart))
    

def productPage(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(product_id=product.id, quantity=quantity, update_quantity=True)
            return redirect('productPage', slug)
        else:
            return HttpResponseBadRequest()
            

    else:
        form = AddToCartForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('productPage', slug)

    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('productPage', slug)
    
    return render(request, "core/productPage.html", {'product': product, 'cart': cart })






def checkoutPage(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token']

            charge = stripe.Charge.create(
                amount=int(cart.get_total_cost() * 100),
                currency='INR',
                description='Charge from Arazzi',
                source=stripe_token
            )

            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            street_address = form.cleaned_data['street_address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip = 1

            order = checkout(request, email, full_name, street_address, city, state, zip, cart.get_total_cost())

            cart.clear()

            print(order)

            return redirect('success')
    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    if remove_from_cart:
        cart.remove(remove_from_cart)

    
    return render(request, "core/checkout.html", {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY, 'cart': cart})

def success(request):
    return render(request, 'core/success.html')