from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from .forms import UserLoginForm, UserProfileForm
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomUserCreationForm
from products.models import Basket
from django.views.generic.base import TemplateView
from .models import EmailVerification
from .models import User
import logging

logger = logging.getLogger(__name__)


class EmailVerificationView(TemplateView):
    title = 'Email Verification'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        email = kwargs['email']
        user = User.objects.get(email=email)
        email_verification = EmailVerification.objects.get(user=user, code=code)
        try:
            if email_verification.is_expired():
                user.email_verified = True
                user.save()

            return super().get(request, *args, **kwargs)

        except User.DoesNotExist:
            logger.warning(f"Пользователь с почтой {email} существует")
            return HttpResponseRedirect(reverse('common'))
        except EmailVerification.DoesNotExist:
            return HttpResponseRedirect(reverse('common'))


# loginform
class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        return context


class UserRegisrtationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались! Подтвердите адрес эл.почты!'

    def get_context_data(self, **kwargs):
        context = super(UserRegisrtationView, self).get_context_data()
        context['title'] = 'Neighbourhood - Регистрация'
        return context


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))
