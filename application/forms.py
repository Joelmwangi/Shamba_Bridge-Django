# application/forms.py
from django import forms
from panel.models import Product
from .models import Message, Reply


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'price_now', 'quantity', 'location']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type text....'}),

        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Reply here'})

        }


