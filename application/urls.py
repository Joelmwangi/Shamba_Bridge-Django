from tkinter.font import names
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from application import views

app_name = 'application'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
     path('application/', views.application_view, name='application'),
    path('market/', views.market, name='market'),
    path('pay-now/', views.pay_now, name='pay_now'),
    path('community/', views.community, name='community'),
    path('chat/', views.chat_view, name='chat'),
    path('products/<int:id>/', views.get_product, name='view_product'),
    path('order/<int:id>/', views.order, name='order'),
    path('reply/<int:message_id>/', views.post_reply, name='post_reply'),
    path('test/', views.test, name='test'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),

]
