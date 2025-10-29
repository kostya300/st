from django.contrib.auth.forms import AuthenticationForm
from django import forms
from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')
    pass


# А в разметке для инпутов добавляем атрибут name, в котором значениями будут username и password. И обязательно инпут и лэбел должны быть связаны через id, т.е у label должен быть атрибут for  в котором должно быть указано то же самое, что и в id input.