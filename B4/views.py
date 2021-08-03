import re
import threading
from datetime import datetime
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic.base import View
from B4 import models, forms
from NB4444.settings import MEDIA_URL


class Autorization(View):
    """Авторизация"""

    @staticmethod
    def get(request, warning=None):
        userform = forms.UserForm()
        warning = warning
        return render(request, 'pages/login.html', locals())

    @staticmethod
    def post(request):
        username = request.POST['username']
        password = request.POST['password']
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
    """Главная страница"""

    @staticmethod
    def get(request):
        return render(request, 'pages/general.html', {})


class StandartVichetiView(View):
    """Стандартные вычеты"""

    @staticmethod
    def get(request):
        queryset = models.StandartVichet.objects.last()
        return render(request, 'pages/standart_vichet.html', {'last_vicheti': queryset})

    @staticmethod
    def post(request):
        queryset = models.StandartVichet(
            hata=float(request.POST.get('hata').replace(',', '.')),
            proezd=float(request.POST.get('proezd').replace(',', '.')),
            mobila=float(request.POST.get('mobila').replace(',', '.')),
            eda=float(request.POST.get('eda').replace(',', '.'))
        )
        try:
            queryset.save()
        except Exception as e:
            print(e)
        finally:
            return redirect("standartnie_vicheti")


class NlgView(View):
    """Направление личной жизни"""
    queryset = models.Nlg.objects.all()

    def get(self, request):
        paginator = Paginator(self.queryset, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'pages/NLJ.html', {'queryset': page_obj, 'MEDIA_URL': MEDIA_URL})

    def post(self, request):
        text_nlg = request.POST.get('text_nlg')
        image_nlg = request.FILES.get('image_nlg')
        if not text_nlg and not image_nlg:
            return redirect('nlj')
        queryset = models.Nlg(text_nlg=text_nlg, image_nlg=image_nlg)
        search_template = r'\d{2}.\d{2}.\d{4}'
        if text_nlg and re.match(search_template, request.POST.get('text_nlg')):
            queryset.date_nlg = datetime.strptime(
                re.match(search_template, request.POST.get('text_nlg')).group(0),
                '%d.%m.%Y'
            )
            queryset.text_nlg = text_nlg[11:].strip()
        try:
            queryset.save()
        except Exception as e:
            print(e)
        finally:
            return redirect('nlj')


def get_bot_info(request):
    from botV4 import main
    t1 = threading.Thread(target=main.main)
    t1.start()
    return redirect('nlj')
