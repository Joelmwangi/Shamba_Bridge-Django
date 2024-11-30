from django.shortcuts import redirect
from django import forms
from .models import Profile, Product
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
            'price_before' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Price ksh'}),
            'price_now': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price ksh'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kisii'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+2547243563'}),

        }