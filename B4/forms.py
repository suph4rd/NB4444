from dal import autocomplete
from django.contrib.auth.models import User
from django import forms

from B4 import models


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


class TaskModelForm(forms.ModelForm):
    plan = forms.ModelChoiceField(
        label="План",
        queryset=models.Plan.objects.all(),
        widget=autocomplete.ModelSelect2(url="plan_autocomplete")
    )

    class Meta:
        model = models.Task
        exclude = ("created_at", "updated_at")

