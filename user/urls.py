from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/success/', views.register_success, name='register_success'),
    path('profile/', views.user_profile, name='user_profile'),
]
