import re
import threading
from datetime import datetime
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.views.generic.base import View
from B4 import models, forms, utils
from NB4444.settings import MEDIA_URL


class Autorization(View):

    @staticmethod
    def get(request, warning=None):
        user_form = forms.UserForm()
        warning = warning
        return render(request, 'pages/login.html', locals())

    @staticmethod
    def post(request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('general')
        else:
            warning = 'Неверный логин или пароль!!!'
            return Autorization.get(request=request, warning=warning)


def logout(request):
    django_logout(request)
    return redirect('login')


class GeneralPage(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        return render(request, 'pages/general.html', {})


class DefaultDeductionsView(LoginRequiredMixin, View):
    form = forms.get_custom_model_form(models.DefaultDeductions)

    def get(self, request):
        form = self.form()
        obj = models.DefaultDeductions.objects.last() if models.DefaultDeductions.objects.exists() \
            else models.DefaultDeductions.objects.none()
        form.initial = obj.__dict__
        return render(request, 'pages/default_deductions/default_deduction.html', locals())

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'pages/default_deductions/default_deduction.html', locals())


class NoteView(LoginRequiredMixin, View):
    queryset = models.Note.objects.all()

    def get(self, request):
        paginator = Paginator(self.queryset, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'pages/note/note.html', {'queryset': page_obj, 'MEDIA_URL': MEDIA_URL})

    def post(self, request):
        text = request.POST.get('text')
        image = request.FILES.get('image')
        if not text and not image:
            return redirect('note')
        queryset = models.Note(text=text, image=image)
        search_template = r'\d{2}.\d{2}.\d{4}'
        if text and re.match(search_template, request.POST.get('text')):
            queryset.date = datetime.strptime(
                re.match(search_template, request.POST.get('text')).group(0),
                '%d.%m.%Y'
            )
            queryset.text = text[11:].strip()
        try:
            queryset.save()
        except Exception as e:
            print(e)
        finally:
            return redirect('note')


@login_required
def get_bot_info_view(request):
    from botV4 import main
    t1 = threading.Thread(target=main.receive_records_from_telegramm_bot)
    t1.start()
    return redirect('note')


class TaskCreateView(LoginRequiredMixin, CreateView):
    def get_success_url(self):
        plan_id = self.object.plan_id
        return reverse_lazy('plan_detail', kwargs={'pk': plan_id}) if plan_id else super().get_success_url()


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    def get_success_url(self):
        plan_id = self.object.plan_id
        return reverse_lazy('plan_detail', kwargs={'pk': plan_id}) if plan_id else super().get_success_url()


@login_required
def create_today_plan_task_view(request):
    utils.PlanTask.create_today_plan(request.user.id)
    return redirect('plan_list')
