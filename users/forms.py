from cProfile import label

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,UserChangeForm
from django import forms
from .models import User
from django.contrib.auth import get_user_model


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
class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': "custom-file-input"}),required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4','readonly':True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control py-4','readonly':True}))
    # this is a new branch and i need to  merge this branch with MAINST
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')
# max_length=50,