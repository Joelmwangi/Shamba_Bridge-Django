from itertools import product

from django.http import JsonResponse
from django.shortcuts import render, redirect

from application.models import Order
from panel.models import Product, Profile


# Create your views here.
def index(request):
    return render(request, 'index.html')

def test(request):
    return render(request, 'test.html')

def market(request):
    products = Product.objects.all()
    profiles = Profile.objects.all()
    return render(request, 'market.html', {'products': products, 'profile': profiles})

def get_product_details(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = {
            'id': product.id,
            'name': product.name,
            'price_now': float(product.price_now),

        }
        return  JsonResponse({'status':'success', 'data':data})
    except Product.DoesNotExist:
        return JsonResponse({'status':'error', 'message':'Product not found'})

def submit_order(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        price_now = request.POST['price_now']
        payment_number = request.POST['payment_number']

        Order.objects.create(
            product_name = product_name,
            price_now = price_now,
            paymnet_number = payment_number
        )
        return redirect('success')


def application_view(request):
    return render(request, 'dashboard.html')