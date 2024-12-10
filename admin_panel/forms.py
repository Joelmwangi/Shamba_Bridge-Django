from django import forms
from panel.models import Worker
from panel.models import Product
from .models import Blog

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price_now']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'link', 'venue']

        widgets = {

        'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Benefits of modern farming'}),
        'content' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'In modern farming has been made easy bt the available technologies...'}),
        'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'www.shujaasolutions.com'}),
        'venue' : forms.TextInput(attrs={'class':'forms-control', 'placeholder':'Nakuru Show, grounds'}),


        }