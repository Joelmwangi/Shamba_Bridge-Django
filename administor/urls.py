from django.contrib import admin
from django.urls import path
from administor import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('send_mail_page/', views.send_mail_page, name='send_mail_page')
]