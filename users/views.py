
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import UserLoginForm, UserProfileForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import UserLoginForm, UserProfileForm
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
import logging

# Create your views here.


# loginform
def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('common')
    else:
        form = UserLoginForm(request=request)
    context = {'form': form}
    return render(request, 'users/login.html',context)

# regform
def registerview(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('users:login')
        else:
            return render(request, 'users/register.html', {'form': form, 'error': 'Исправьте ошибки в форме'})
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# logutformYYYY

def custom_logout(request):
    logout(request)  # стандартный выход
    # Ваша дополнительная логика (очистка cookies и т.п.)
    return redirect('users:login')


logger = logging.getLogger(__name__)


def profileview(request):
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            instance=request.user
        )
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Профиль успешно обновлён!')
                return redirect('users:profile')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации данных: {e}')
                logger.error(f'Validation error in profile save: {e}')
            except DatabaseError as e:
                messages.error(request, 'Ошибка сохранения в базу данных')
                logger.error(f'Database error in profile save: {e}')
            except Exception as e:
                messages.error(request, f'Неожиданная ошибка: {e}')
                logger.exception('Unexpected error in profile save')
        else:
            messages.error(request, 'Проверьте данные формы.')
            logger.error(f'Form errors: {form.errors}')
    else:
        form = UserProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'users/profile.html', context)