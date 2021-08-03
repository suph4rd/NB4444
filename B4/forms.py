from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль ")

    class Meta:
        model = User
        fields = ('username', 'password')


def get_custom_model_form(model_name, fields_list="__all__"):
    class CustomModelForm(forms.ModelForm):
        class Meta:
            model = model_name
            fields = fields_list
    return CustomModelForm


