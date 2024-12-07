from audioop import reverse

from django.core.files.storage.filesystem import FileSystemStorage
from django.shortcuts import get_object_or_404
from django_daraja.mpesa.core import MpesaClient
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from .forms import ProductForm
from django.urls import reverse
from .models import Payment
from django.contrib import messages
from panel.forms import ProductForm
from panel.models import Product, Profile
from django.shortcuts import render, redirect
from .models import Message
from .forms import MessageForm, ReplyForm

def success(request):
    return render(request, 'success.html')

def failure(request):
    return render(request, 'failure.html')
# Create your views here.
def index(request):
    return render(request, 'index.html')

def test(request):
    return render(request, 'test.html')

def market(request):
    products = Product.objects.all()
    profiles = Profile.objects.all()
    return render(request, 'market.html', {'products': products, 'profile': profiles})

def community(request):
    return render(request, 'community.html')

def application_view(request):
    return render(request, 'dashboard.html')



def edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product successfully')
            return redirect('about')
        else:
            messages.error(request, 'Please check foorm details')
    else:
        form = ProductForm(instance=product)
    # return render(request, 'edit.html', {'form':form, 'student':student})
    return render(request, 'edit.html', {'form': form, 'student':product})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def get_product(request, id):
    products = get_object_or_404(Product, id=id)
    return render(request, 'products.html', {'products':products})

def pay_now(request):
    client = MpesaClient()
    phone_number = request.POST.get('phone_number')
    amount = 1
    account_reference = 'Shamba Bridge Kenya'
    transaction_desc = 'payment for web dev'
    callback_url = 'https://darajambill.herokuapp.com/express-payment'
    response = client.stk_push(phone_number,amount,account_reference,transaction_desc,callback_url)
    return HttpResponse(response)
    

# def pay_now(request):
#     client = MpesaClient()
#     phone_number = request.POST.get('phone_number')
#     amount = 1
#     account_reference = 'Shamba Bridge Kenya'
#     transaction_desc = 'payment for web dev'
#     callback_url = 'https://darajambill.herokuapp.com/express-payment'
#
#     response = client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
#
#     if hasattr(response, 'status_code') and response.status_code == 'success':
#         # Save payment to database with 'success' status
#         payment = Payment.objects.create(
#             phone_number=phone_number,
#             amount=amount,
#             status='success'
#         )
#         return JsonResponse({
#             'status': 'success',
#             'message': 'Payment processed successfully.',
#             'payment_id': payment.id
#         }, status=200)
#     else:
#         # Save payment to database with 'failed' status
#         payment = Payment.objects.create(
#             phone_number=phone_number,
#             amount=amount,
#             status='failed'
#         )
#         return JsonResponse({
#             'status': 'failed',
#             'message': 'Payment failed. Please try again.',
#             'payment_id': payment.id
#         }, status=400)



def order(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student Updated successfully')
            return redirect('about')
        else:
            messages.error(request, 'Please check foorm details')
    else:
        form = ProductForm(instance=product)
    # return render(request, 'edit.html', {'form':form, 'student':student})
    return render(request, 'market.html', {'form': form, 'student':product})




def chat_view(request):
    messages = Message.objects.all()

    username = request.session.get('username', None)

    if request.method == 'POST':
        if 'username' in request.POST:
            username = request.POST.get('username')
            request.session['username'] = username

        message_form = MessageForm(request.POST, request.FILES)
        if message_form.is_valid() and username:
            message = message_form.save(commit=False)
            message.username = username
            image = request.FILES.get('image')
            if image:
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                message.image_url = fs.url(filename)
            message.save()
            return redirect('application:chat')

        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply_form.save()
            return redirect('application:chat')

    else:
        message_form = MessageForm()
        reply_form = ReplyForm()

    return render(request, 'chat.html', {
        'messages': messages,
        'message_form': message_form,
        'reply_form': reply_form,
        'username': username
    })

def post_reply(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.message = message
            reply.save()
            return redirect('application:chat')

    else:
        reply_form = ReplyForm()

    return redirect('application:chat')