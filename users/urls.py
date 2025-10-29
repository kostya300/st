from django.contrib import admin
from django.contrib.auth import logout
from django.template.context_processors import media
from django.urls import path
from .views import login_view, registerview,custom_logout

app_name = 'users'
urlpatterns = [
    path('login/', login_view ,name='login'),
    path('register/', registerview ,name='register'),
    path('logout/', custom_logout, name='logout'),
]