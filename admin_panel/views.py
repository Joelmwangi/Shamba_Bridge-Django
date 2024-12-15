from django.forms import models
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from .models import Blog,  User
from django.db.models import Count
from .forms import BlogForm
from django.contrib.auth.decorators import login_required, user_passes_test
from panel.models import Worker
from panel.models import Product, User


def is_admin(user):
    return user.is_staff or user.is_superuser  # Customize this if needed

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'admin_panel/login.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Correct usage of Count for product counts grouped by product_name
    product_counts = Product.objects.values('product_name').annotate(count=Count('id'))

    # Get user and blog counts
    user_count = User.objects.count()
    blog_count = Blog.objects.count()

    # Prepare labels and data for the pie charts
    product_labels = [product['product_name'] for product in product_counts]
    product_data = [product['count'] for product in product_counts]

    # Data for users vs blogs comparison
    users_vs_blogs_labels = ['Users', 'Blogs']
    users_vs_blogs_data = [user_count, blog_count]

    # Render the dashboard template with the data for the charts
    return render(request, 'admin_panel/dashboard.html', {
        'product_labels': product_labels,
        'product_data': product_data,
        'users_vs_blogs_labels': users_vs_blogs_labels,
        'users_vs_blogs_data': users_vs_blogs_data
    })

# View for Managing Users
@login_required
@user_passes_test(is_admin)
def manage_users(request):
    # You can add logic to fetch and display users here
    return render(request, 'admin_panel/manage_users.html')
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin_panel/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('manage_users')

@login_required
@user_passes_test(is_admin)
def change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = PasswordChangeForm(user)
    return render(request, 'admin_panel/change_password.html', {'form': form, 'user': user})
@login_required
@user_passes_test(is_admin)
def manage_products(request):
    products = Product.objects.all()
    username_filter = request.GET.get('username')
    if username_filter:
        # Filter products by the provided username
        user = User.objects.filter(username=username_filter).first()
        if user:
            products = products.filter(user=user)
    return render(request, 'admin_panel/manage_products.html', {'products': products})


@login_required
@user_passes_test(is_admin)
def manage_workers(request):
    workers = Worker.objects.all()
    worker_name_filter = request.GET.get('worker_name')
    user_posted_filter = request.GET.get('user_posted')

    if worker_name_filter:
        workers = workers.filter(name__icontains=worker_name_filter)
    if user_posted_filter:
        user = User.objects.filter(username__icontains=user_posted_filter).first()
        if user:
            workers = workers.filter(user=user)

    return render(request, 'admin_panel/manage_workers.html', {'workers': workers})

@login_required
@user_passes_test(is_admin)
def manage_blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'admin_panel/manage_blogs.html', {'blogs': blogs})

@login_required
@user_passes_test(is_admin)
def post_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('manage_blogs')
    else:
        form = BlogForm()
    return render(request, 'admin_panel/post_blog.html', {'form': form})


def edit_blog(request, id):
    blog = get_object_or_404(Blog, id=id)

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('manage_blogs')  # Redirect to the manage blogs page
    else:
        form = BlogForm(instance=blog)

    return render(request, 'admin_panel/edit_blog.html', {'form': form, 'blog': blog})

def delete_blog(request, id):
    blog = get_object_or_404(Blog, id=id)

    if blog.author == request.user or request.user.is_staff:
        blog.delete()
        return redirect('manage_blogs')
    else:
        return redirect('manage_blogs')