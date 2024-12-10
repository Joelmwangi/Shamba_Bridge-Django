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
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.contrib import messages
from panel.forms import ProductForm
from panel.models import Product, Profile
from django.shortcuts import render, redirect
from .models import Message
from .forms import MessageForm, ReplyForm
import json
import os
from django.conf import settings
from django.http import JsonResponse


def save_transaction_status(request):
    # Example dynamic data from the request
    transaction_data = {
        "MerchantRequestID": request.GET.get("MerchantRequestID", "default_merchant_id"),
        "CheckoutRequestID": request.GET.get("CheckoutRequestID", "default_checkout_id"),
        "ResponseCode": request.GET.get("ResponseCode", "0"),
        "ResponseDescription": request.GET.get("ResponseDescription", "Success. Request accepted for processing"),
        "CustomerMessage": request.GET.get("CustomerMessage", "Success. Request accepted for processing"),
    }

    # Determine transaction status dynamically
    transaction_data["TransactionStatus"] = "Successful" if transaction_data["ResponseCode"] == "0" else "Failed"

    # File path for storing transactions
    output_file = os.path.join(settings.MEDIA_ROOT, "transactions", "transaction_status.json")

    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Load existing transactions if the file exists, otherwise create a new list
        if os.path.exists(output_file):
            with open(output_file, "r") as file:
                all_transactions = json.load(file)
        else:
            all_transactions = []

        # Append the new transaction to the list
        all_transactions.append(transaction_data)

        # Write updated transactions back to the file
        with open(output_file, "w") as file:
            json.dump(all_transactions, file, indent=4)

        # Return success response
        return JsonResponse({
            "message": "Transaction status saved successfully.",
            "status": 1,
            "transactions_count": len(all_transactions),
            "file": output_file
        })

    except Exception as e:
        # Handle exceptions
        return JsonResponse({
            "message": f"An error occurred: {str(e)}",
            "status": 0
        })

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
#
# def pay_now(request):
#     client = MpesaClient()
#     phone_number = request.POST.get('phone_number')
#     amount = 1
#     account_reference = 'Shamba Bridge Kenya'
#     transaction_desc = 'payment for web dev'
#     callback_url = 'https://darajambill.herokuapp.com/express-payment'
#     response = client.stk_push(phone_number,amount,account_reference,transaction_desc,callback_url)
#     return HttpResponse(response)
#



def pay_now(request):
    client = MpesaClient()
    phone_number = request.POST.get('phone_number')
    amount = 100
    account_reference = 'Shamba Bridge Kenya'
    transaction_desc = 'Payment for web dev'
    # callback_url = 'https://darajambill.herokuapp.com/express-payment'
    callback_url = 'https://lipia-api.kreativelabske.com/api'

    # Generate a reference number (e.g., ShBr0111)
    reference_number = "ShBr" + get_random_string(length=4, allowed_chars="0123456789")

    response = client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

    if hasattr(response, 'status_code') and response.status_code == 'success':
        # Save payment to database with 'success' status
        payment = Payment.objects.create(
            phone_number=phone_number,
            amount=amount,
            status='success',
            reference_number=reference_number  # Store the reference number
        )

        # Redirect user to the success page
        return redirect('success_page')  # Replace 'success_page' with the name of your success URL

    else:
        # Save payment to database with 'failed' status
        payment = Payment.objects.create(
            phone_number=phone_number,
            amount=amount,
            status='failed'
        )

        # Render an HTML page for the failed transaction
        return render(request, 'failure.html', {
            'message': 'Payment failed. Please try again.',
            'phone_number': phone_number,
            'amount': amount,
            'payment_id': payment.id,
        })


def order(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, ' Updated successfully')
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