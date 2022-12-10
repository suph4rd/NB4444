# from dal import autocomplete
from django import forms
from django.contrib.auth.models import User

from B4 import models


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль ")

    class Meta:
        model = User
        fields = ('username', 'password')


def get_custom_model_form(model_name, fields_list="__all__", exclude_fields=None):
    class CustomModelForm(forms.ModelForm):
        class Meta:
            model = model_name
            if exclude_fields:
                exclude = exclude_fields
            else:
                fields = fields_list
    return CustomModelForm


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ("plan", "section", "description", "is_ready")


class DefaultDeductionModelForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput
    )

    class Meta:
        model = models.DefaultDeductions
        fields = ("house", "travel", "phone", "food", "user")


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        obj = super().save(commit)
        obj.set_password(obj.password)
        obj.save()
        return obj


class NoteModelForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ["text", "image", "user"]
        widgets = {
            "user": forms.HiddenInput()
        }

