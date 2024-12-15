from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-workers/', views.manage_workers, name='manage_workers'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path('manage-blogs/', views.manage_blogs, name='manage_blogs'),
    path('post-blog/', views.post_blog, name='post_blog'),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('change-password/<int:user_id>/', views.change_password, name='change_password'),
    path('edit_blog/<int:id>/', views.edit_blog, name='edit_blog'),
    path('delete_blog/<int:id>/', views.delete_blog, name='delete_blog'),
]
