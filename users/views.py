from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models.query_utils import select_related_descend
from django.http import JsonResponse
from django.template.context_processors import request
from django.urls import reverse_lazy

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.views import LoginView
from .forms import UserLoginForm, UserProfileForm
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth import logout
import logging
from products.models import Basket
from django.contrib.auth.decorators import login_required

from .models import User


# Create your views here.


# loginform
class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
# def login_view(request):
#     if request.method == "POST":
#         form = UserLoginForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 auth_login(request, user)
#                 return redirect('common')
#     else:
#         form = UserLoginForm(request=request)
#     context = {'form': form}
#     return render(request, 'users/login.html',context)



class UserRegisrtationView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    def get_context_data(self, **kwargs):
        context = super(UserRegisrtationView,self).get_context_data()
        context['title'] = 'Neighbourhood'
        return context


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Добавлен **kwargs
        context['title'] = 'Neighbourhood'
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

# logger = logging.getLogger(__name__)
#
#
# def profileview(request):
#     if request.method == 'POST':
#         form = UserProfileForm(
#             request.POST,
#             files=request.FILES,
#             instance=request.user
#         )
#         if form.is_valid():
#             print("Форма валидна")
#             try:
#                 form.save()
#                 print("Данные сохранены")
#                 return redirect('users:profile')
#             except Exception as e:
#                 print(f"Ошибка сохранения: {e}")
#         else:
#             print(f"Ошибки формы: {form.errors}")
#     else:
#         form = UserProfileForm(instance=request.user)
#     #  cycle   подсчёт
#     total_sum = 0
#     total_quantity = 0
#     for basket in Basket.objects.filter(user=request.user):
#         total_sum += basket.sum()
#         total_quantity += basket.quantity
#     context = {'form': form,
#                'baskets': Basket.objects.filter(user=request.user),
#                'total_sum': total_sum,'total_quantity': total_quantity,
#                }
#
#     return render(request, 'users/profile.html', context)

# regform
# def registerview(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             messages.success(request, 'Аккаунт успешно зарегестрирован')
#             user = form.save()
#             auth_login(request, user)
#             return redirect('users:login')
#         else:
#             return render(request, 'users/register.html', {'form': form, 'error': 'Исправьте ошибки в форме'})
#     else:
#         form = UserCreationForm()
#     return render(request, 'users/register.html', {'form': form})











