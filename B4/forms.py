# форма авторизации
from django.contrib.auth.models import User
from django import forms

from B4.models import nlg


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль ")
    class Meta:
        model = User
        fields = ('username', 'password')

