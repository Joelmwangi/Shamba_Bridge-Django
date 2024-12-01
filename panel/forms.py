from random import choices

from django.contrib.admindocs.utils import ROLES
from django.shortcuts import redirect
from django import forms
from .models import Profile, Product, Worker
from django.http import HttpResponse, Http404


def auth(view_function):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated == False:
            return redirect('login')
        return view_function(request, *args, **kwargs)
    return wrapped_view

def guest(view_function):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return view_function(request, *args, **kwargs)
    return wrapped_view

def guest(view_function):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:

            if '/admin/' in request.path:
                return redirect('page')
        return view_function(request, *args, **kwargs)
    return wrapped_view


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'placeholder':'User'}),
            'image' : forms.FileInput(attrs={'class':'form-control','accept':'image/*', 'title':'upload image here'}),
            'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Joel Mwangi'}),
            'farm_nol' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Fk23253'}),
            'farm_product': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Maize' }),
            'location' : forms.TextInput(attrs={'class':'form-control','placeholder':'Kericho'})

        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'placeholder': 'User'}),
            'image' : forms.FileInput(attrs={'class':'form-control', 'accept':'image/*','title':'Upload Image here'}),
            'product_name': forms.TextInput(attrs={'class':'form-control','placeholder':'milk'}),
            'date_time' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'date and time'}),
            'quantity' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'10 Bags'}),
            'price_before' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Price ksh'}),
            'price_now': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price ksh'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kisii'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+2547243563'}),

        }
MODE_OF_PAYMENT =  [
    ('mpesa', 'Mpesa'),
    ('bank', 'Bank'),
    ('airtel', 'Airtel'),
]
ROLES_WOKERS = [
    ('gate Keper', 'Gate Keeper'),
    ('farm manager', 'Farm Manger'),
    ('Farm worker', 'Farm worker'),
    ('driver', 'Driver'),

]

SALARY_STATUS = [
    ('paid', 'Paid'),
    ('pending', 'Pending'),
    ('Dispersed', 'Dispersed')
]
class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'

        widgets ={
            'user': forms.Select(attrs={'class': 'form-control', 'placeholder': 'User'}),
            'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Full Name'}),
            'Id_number' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'39565758'}),
            'email': forms.TextInput(attrs={'class':'form-control', 'placeholder':'johndoe@gmail.com'}),
            'role' : forms.Select(choices=ROLES_WOKERS, attrs={'class':'form-control', 'placeholder':'Feeding Animals'}),
            'mode_payment' : forms.Select(choices=MODE_OF_PAYMENT, attrs={'class':'form-control', 'placeholder':'Mpesa'}),
            'account' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'012848494000/ +2543738399'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' +254112054071'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' 10,000'}),
            'status_salary' : forms.Select(choices=SALARY_STATUS, attrs={'class': 'form-control', 'placeholder': 'User'}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'User'}),
        }