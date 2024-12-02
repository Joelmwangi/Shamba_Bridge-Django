from django.core.files.storage.filesystem import FileSystemStorage
from django.shortcuts import get_object_or_404
from panel.models import Product, Profile
from django.shortcuts import render, redirect
from .models import Message, Reply
from .forms import MessageForm, ReplyForm

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