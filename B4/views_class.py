import re
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic.base import View
from B4.forms import UserForm
from B4 import models
from NB4444.settings import MEDIA_URL


class Autorization(View):
    """Авторизация"""
    def get(self, request, warning=None):
        content = {}
        userform = UserForm()
        content['warning'] = warning
        content['userform'] = userform
        return render(request, 'login.html', content)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('general')
        else:
            warning = 'Неверный логин или пароль!!!'
            return Autorization.get(self, request=request, warning=warning)

class Logout(View):
    """Выход из профиля"""
    def get(self, request):
        logout(request)
        return redirect('login')


class GeneralPage(LoginRequiredMixin, View):
    """Главная страница"""
    def get(self, request):
        return render(request, 'general.html', {})


class StandartVichetiView(View):
    """Стандартные вычеты"""
    def get(self, request):
        queryset = models.StandartVichet.objects.last()
        return render(request, 'standart_vichet.html', {'last_vicheti': queryset})

    def post(self, request):
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
            return StandartVichetiView.get(self, request)


class NlgView(View):
    """Направление личной жизни"""
    def get(self, request):
        queryset = models.Nlg.objects.all()
        paginator = Paginator(queryset, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'NLJ.html', {'queryset': page_obj,
                                            'MEDIA_URL': MEDIA_URL})

    def post(self, request):
        text_nlg = request.POST.get('text_nlg')
        image_nlg = request.FILES.get('image_nlg')
        if not text_nlg and not image_nlg:
            return NlgView.get(self, request)
        queryset = models.Nlg(text_nlg=text_nlg, image_nlg=image_nlg)
        if text_nlg and re.match(r'\d{2}.\d{2}.\d{4}', request.POST.get('text_nlg')):
            queryset.date_nlg = datetime.strptime(re.match(r'\d{2}.\d{2}.\d{4}', request.POST.get('text_nlg')).group(0), '%d.%m.%Y')
            queryset.text_nlg = text_nlg[11:].strip()
        try:
            queryset.save()
        except Exception as e:
            print(e)
        finally:
            return NlgView.get(self, request)


class MinfinView(View):
    """МинФин"""
    queryset = models.Minfin.objects.all()
    template_name = 'Minfin/minfin.html'
    nds = 1

    def get(self, request):
        last_ostatoc = self.queryset.aggregate(ostatoc=Sum('price')).get('ostatoc') * -1 if self.queryset.exists() else 0
        paginator = Paginator(self.queryset, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'queryset': page_obj, 'last_ostatoc': last_ostatoc}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        text_input = request.POST.get('data')  # текст из формы
        if not text_input:
            '''Проверка Not Null формы'''
            return self.get(request)
        queryset = models.Minfin()    # инициализируем новый объект БД
        try:
            if re.match(r'-\d+.\d+', text_input):
                sum = re.match(r'-\d+.\d+', text_input)     # дробная отрицательная сумма
            elif re.match(r'\d+.\d+', text_input):
                sum = re.match(r'\d+.\d+', text_input)      # дробная сумма
            elif re.match(r'-\d+', text_input):
                sum = re.match(r'-\d+', text_input)  # достаём сумму, если она отрицательная
            else:
                sum = re.match(r'\d+', text_input)   # достаём сумму
            queryset.price = float(sum.group()) * self.nds      # мб Float или лучше Decimal
            queryset.describe = text_input[sum.end()+1:].strip()
            queryset.save()
        except Exception as e:
            print(e)
        finally:
            return self.get(request)


class MinfinEdaView(MinfinView):
    queryset = models.Minfin.objects.filter(type_table=0)
    template_name = 'Minfin/minfin_item.html'
    nds = 1.1


class MinfinAtractiveView(MinfinView):
    queryset = models.Minfin.objects.filter(type_table=1)
    template_name = 'Minfin/minfin_item.html'
    nds = 1.1


class MinfinRoadView(MinfinView):
    queryset = models.Minfin.objects.filter(type_table=2)
    template_name = 'Minfin/minfin_item.html'
    nds = 1.1


class MinfinPhoneView(MinfinView):
    queryset = models.Minfin.objects.filter(type_table=3)
    template_name = 'Minfin/minfin_item.html'


class MinfinDepreciationView(MinfinView):
    queryset = models.Minfin.objects.filter(type_table=4)
    template_name = 'Minfin/minfin_item.html'


class MinfinOtherView(MinfinView):
    queryset = models.Minfin.objects.filter(type_table=5)
    template_name = 'Minfin/minfin_item.html'


class MinfinNDSView(MinfinView):
    queryset = models.Minfin.objects.filter(type_table=6)
    template_name = 'Minfin/minfin_item.html'
