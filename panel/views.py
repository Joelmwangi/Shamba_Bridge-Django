from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import  redirect, get_object_or_404

from panel.forms import guest, auth, ProfileForm, ProductForm, WorkerForm
from django.shortcuts import render

from project import settings
from .models import Profile, Product, Worker
from django.contrib import messages



# Create your views here.

@guest
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})


@guest
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


@auth
def dashboard_view(request):
    data = Profile.objects.filter(user=request.user)
    product_count = Product.objects.filter(user=request.user).count()
    workers_count = Worker.objects.filter(user=request.user).count()
    chart_data = {
        'labels' : ['Workers', 'Products'],
        'data' : [workers_count, product_count]
    }
    return render(request, 'dashboard.html', {'data':data,'product_count': product_count, 'workers_count': workers_count, 'chart_data':chart_data})


def logout_view(request):
    logout(request)
    return redirect('login')


@guest
# def page(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('about')
#     else:
#         form = ProfileForm()
#     return render(request, 'about.html', {'form': form})

@auth
def about(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('about')
    else:
        form = ProfileForm()
    data = Profile.objects.filter(user=request.user)
    return render(request, 'about.html', {'data': data, 'form': form})

@auth
def product(request):
    if request.method == 'POST':
        form1 = ProductForm(request.POST, request.FILES)
        if form1.is_valid():
            new_product = form1.save(commit=False)
            new_product.user = request.user
            new_product.save()
            messages.success(request, 'Product added Succesfully')
            return redirect('product')
        else:
            # print(f"Form Errors: {form.errors}")
            messages.error(request, 'Product not Added Please check deatils')
    else:
        form1 = ProductForm()

    data1 = Product.objects.filter(user=request.user)

    return render(request, 'product.html', {'form1': form1, 'data1': data1})




@auth
def new_worker(request):
    if request.method == 'POST':
        nworker = WorkerForm(request.POST, request.FILES)
        if nworker.is_valid():
            new_worker = nworker.save(commit=False)
            new_worker.user = request.user
            new_worker.save()

            # Ensure we retrieve the email of the new worker
            recipient_email = new_worker.email  # This is where the email is saved

            # Send the email
            subject = 'Worker Registration Successful'
            message = f'Dear {new_worker.name},\n\nYour registration as a worker has been successfully completed we shall send you anther email to let you know on the date to start working.'

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [recipient_email],
                    fail_silently=False,
                )
                messages.success(request, 'Worker Added Successfully and email sent!')
            except Exception as e:
                messages.error(request, f'Error sending email: {str(e)}')

            return redirect('new_worker')
        else:
            messages.error(request, 'Worker Not Added, please check details')
    else:
        nworker = WorkerForm()

    worker1 = Worker.objects.filter(user=request.user)
    return render(request, 'new_worker.html', {'nworker': nworker, 'worker1': worker1})






@auth
def fire(request, id):
    worker = get_object_or_404(Worker, id=id)

    try:
        worker.delete()
        messages.success(request, 'Worker successfully fired.')
    except Exception as e:
        messages.error(request, f'Error firing worker: {str(e)}')

    return redirect('new_worker')
@auth
def edit(request, id):
    print(f"Request Method: {request.method}")
    profile = get_object_or_404(Profile, id=id)
    print(f"Profile: {profile}")
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully')
            return redirect('about')
        else:
            print(f"Form Errors: {form.errors}")
            messages.error(request, 'Please check details')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit.html', {'form': form, 'profile': profile})

@auth
def editproduct(request, id):
    print(f"Request Method: {request.method}")
    profile = get_object_or_404(Profile, id=id)
    print(f"Product: {product}")
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully')
            return redirect('product')
        else:
            print(f"Form Errors: {form.errors}")
            messages.error(request, 'Please check details')
    else:
        form = ProductForm(instance=profile)
    return render(request, 'product.html', {'form': form, 'product': product})

def pay(request):
    if request.method == 'POST':
        worker_ids = request.POST.getlist('worker_ids')
        print(worker_ids)  # Debug worker_ids

        # Get active workers belonging to the current user
        workers_to_update = Worker.objects.filter(
            id__in=worker_ids,
            status='Active',
            user=request.user,
            is_active=True
        )
        print(workers_to_update)  # Debug the queryset

        if workers_to_update.exists():
            # Update status to 'Paid'
            workers_to_update.update(status='Paid')

            # Send email notifications
            for worker in workers_to_update:
                print(f"Worker: {worker.name}, Email: {worker.email}")  # Debug worker email
                if worker.email:
                    try:
                        send_mail(
                            subject='Payment Notification',
                            message=f'Dear {worker.name}, your payment has been processed. Please check your bank account.',
                            from_email='your-email@example.com',
                            recipient_list=[worker.email],
                            fail_silently=False,
                        )
                    except Exception as e:
                        print(f"Error sending email to {worker.email}: {str(e)}")  # Log email errors

            messages.success(request, 'Payments processed and email notifications sent!')
        else:
            messages.warning(request, 'No eligible workers found for payment.')

        return redirect('pay')

    # Filter workers
    paid_workers = Worker.objects.filter(
        user=request.user,
        status='Paid',
        is_active=True
    ).values('id', 'Id_number', 'name', 'account', 'mode_payment', 'salary', 'status')

    pending_workers = Worker.objects.filter(
        user=request.user,
        status='Active',
        is_active=True
    ).values('id', 'Id_number', 'name', 'account', 'mode_payment', 'salary', 'status')

    return render(request, 'pay.html', {'paid_workers': paid_workers, 'pending_workers': pending_workers})




    # Filter active workers with status 'Paid'
    paid_workers = Worker.objects.filter(
        user=request.user,
        status='Paid',
        is_active=True  # Only show active paid workers
    ).values('id', 'Id_number', 'name', 'account', 'mode_payment', 'salary', 'status')

    # Filter active workers with status 'Active'
    pending_workers = Worker.objects.filter(
        user=request.user,
        status='Active',
        is_active=True  # Only show active pending workers
    ).values('id', 'Id_number', 'name', 'account', 'mode_payment', 'salary', 'status')

    return render(request, 'pay.html', {'paid_workers': paid_workers, 'pending_workers': pending_workers})
def sidebar(request):
    data = Profile.objects.fillter(user=request.user)
    return render(request, 'layouts/sidebar.html', {'data': data})

@auth
def delete(request, id):
    product = get_object_or_404(Product, id=id)

    try:
        product.delete()
        messages.success(request, 'Product Succefully deleted')
    except Exception as e:
        messages.error(request, 'Productt not deleted')

    return redirect('product')


def panel_view(request):
    return render(request, 'dashboard.html')