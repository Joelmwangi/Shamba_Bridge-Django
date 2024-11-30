"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unittest.mock import patch
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from panel import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', views.panel_view, name='panel'),
    path('signup/', views.signup_view, name='signup'),
    path('about/', views.about, name='about'),
    path('product', views.product, name='product'),
    path('sidebar/', views.sidebar, name='sidebar'),
    path('new_worker', views.new_worker, name='new_worker'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('supplier/', views.supplier, name='supplier'),
    path('edit/<int:id>/', views.edit,name='edit'),
    path('pay/', views.pay, name='pay'),
    path('panel/fire/<int:id>/', views.fire, name='fire_worker'),
    path('delete/<int:id>/', views.delete, name='delete'),




]
