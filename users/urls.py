from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from django.template.context_processors import media
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import UserLoginView, UserRegisrtationView, UserProfileView, EmailVerificationView

app_name = 'users'
urlpatterns = [
    path('login/', UserLoginView.as_view() ,name='login'),
    path('register/', UserRegisrtationView.as_view() ,name='register'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', LogoutView.as_view() , name='logout'),
    path('verify/<str:email>/<uuid:code>', EmailVerificationView.as_view() , name='email_verification'),
]