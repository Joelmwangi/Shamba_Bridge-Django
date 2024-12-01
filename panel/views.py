from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import  redirect, get_object_or_404

from panel.forms import guest, auth, ProfileForm, ProductForm, WorkerForm
from django.shortcuts import render
from .models import Profile, Product, Worker, send_welcome_email
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
    pending_status_count = Worker.objects.filter(user=request.user, status_salary='pending').count()

    chart_data = {
        'labels': ['Workers', 'Products', 'Pending Salaries'],
        'data': [workers_count, product_count, pending_status_count]
    }

    return render(request, 'dashboard.html', {
        'data': data,
        'product_count': product_count,
        'workers_count': workers_count,
        'pending_status_count': pending_status_count,
        'chart_data': chart_data
    })

def supplier(request):
    return render(request, 'supplier.html')
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
            # send_welcome_email(new_worker.email)
            # messages.success(request, 'Worker Added Successfully, and an email has been sent.')
            return redirect('new_worker')
            messages.success(request, 'Worker Added Succesfully')
            return redirect('new_worker')
        else:
            messages.error(request, 'Worker Not Added check details please')
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

@auth
def pay(request):
    if request.method == 'POST':
        worker_ids = request.POST.getlist('worker_ids')
        workers_to_update = Worker.objects.filter(
            id__in=worker_ids,
            status='active',
            user=request.user
        )
        workers_to_update.update(status='paid')
        return redirect('pay')

    paid_workers = Worker.objects.filter(
        user=request.user,
        status='paid'
    ).values('id', 'Id_number', 'name', 'account', 'mode_payment', 'salary', 'status')

    pending_workers = Worker.objects.filter(
        user=request.user,
        status='active'
    ).values('id', 'Id_number', 'name', 'account', 'mode_payment', 'salary', 'status')

    return render(request, 'pay.html', {'paid_workers': paid_workers, 'pending_workers': pending_workers})




def panel_view(request):
    return render(request, 'dashboard.html')

