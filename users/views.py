from django.urls import reverse_lazy

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.views import LoginView
from .forms import UserLoginForm, UserProfileForm
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomUserCreationForm
from products.models import Basket

from .models import User

# loginform
class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context['title'] = 'Neighbourhood - Авторизация'
        return context

class UserRegisrtationView(SuccessMessageMixin,CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались! Войдите в систему ниже. '
    def get_context_data(self, **kwargs):
        context = super(UserRegisrtationView,self).get_context_data()
        context['title'] = 'Neighbourhood - Регистрация'
        return context


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Добавлен **kwargs
        context['title'] = 'Neighbourhood - Профиль'
        baskets = Basket.objects.filter(user=self.object)
        total_sum = sum(basket.sum() for basket in baskets)
        total_quantity = sum(basket.quantity for basket in baskets)
        context['total_sum'] = total_sum
        context.update({
            'baskets': baskets,
            'total_sum': total_sum,
            'total_quantity': total_quantity,
        })
        return context











