from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
# А в разметке для инпутов добавляем атрибут name, в котором значениями будут username и password. И обязательно инпут и лэбел должны быть связаны через id, т.е у label должен быть атрибут for  в котором должно быть указано то же самое, что и в id input.
