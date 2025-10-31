from django.shortcuts import render
from .models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import UserLoginForm, UserProfileForm
from django.shortcuts import render
from .models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import UserLoginForm, UserProfileForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import logging

# Create your views here.


# loginform
def login_view(request):
    if request.method == 'POST':  # Изменено на POST
        form = AuthenticationForm(data=request.POST)  # Используйте data=request.POST
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Обратите внимание, что нужно передавать request
                return redirect('common')  # Перенаправление на общую страницу
            else:
                return render(request, 'users/login.html', {'form': form, 'error': 'Неверные имя или пароль'})
        else:
            return render(request, 'users/login.html', {'form': form, 'error': 'Ошибка в форме'})
    else:
        form = AuthenticationForm()
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

# logutform_newlog

def custom_logout(request):
    logout(request)  # стандартный выход
    # Ваша дополнительная логика (очистка cookies и т.п.)
    return redirect('users:login')


logger = logging.getLogger(__name__)


def profileview(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Профиль успешно обновлён!')
                return redirect('users:profile')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении: {e}')
                logger.error(f'Ошибка сохранения профиля: {e}')
        else:
            messages.error(request, 'Проверьте данные формы.')
            logger.error(form.errors)
    else:
        form = UserProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'users/profile.html', context)