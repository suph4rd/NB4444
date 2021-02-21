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
    """МинФин, базовый класс"""
    minfin_name = 'Минфин'
    minfin_type = None
    queryset = models.Minfin.objects.all()
    template_name = 'Minfin/minfin.html'
    nds = 1

    def get(self, request):
        """
        Запрос на показ данных раздела Minfin
        :param request: объект запроса
        :return: рендерит шаблон с данныими
        """
        last_ostatoc = self.queryset.aggregate(ostatoc=Sum('price')).get('ostatoc') * -1 if self.queryset.exists() else 0
        paginator = Paginator(self.queryset, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'queryset': page_obj, 'last_ostatoc': last_ostatoc, 'minfin_name': self.minfin_name}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        text_input = request.POST.get('data')  # текст из формы
        if not text_input:
            '''Проверка Not Null формы'''
            return self.get(request)
        queryset = models.Minfin(type_table=self.minfin_type)   # инициализируем новый объект БД
        try:
            if re.match(r'-\d+.\d+', text_input):
                sum = re.match(r'-\d+.\d+', text_input)     # дробная отрицательная сумма
            elif re.match(r'\d+.\d+', text_input):
                sum = re.match(r'\d+.\d+', text_input)      # дробная сумма
            elif re.match(r'-\d+', text_input):
                sum = re.match(r'-\d+', text_input)  # достаём сумму, если она отрицательная
            else:
                sum = re.match(r'\d+', text_input)   # достаём сумму
            price = float(sum.group())
            queryset.price = price * self.nds if price > 0 else price      # мб Float или лучше Decimal
            queryset.describe = text_input[sum.end()+1:].strip()
            queryset.save()
            self.add_nds(queryset, price)
        except Exception as e:
            print("--------------------Ошибка------------------------------")
            print(e)
            print("--------------------Ошибка------------------------------")
        finally:
            return self.get(request)

    def add_nds(self, queryset: models.Minfin, price):
        """
        Извлекает с каждой операции ндс в размере, указанном в поле класса.
        При ставке НДС, равной 1, экземпляр НДС не создаётся.
        При отрицательном price экземпляр НДС не создаётся.
        :param queryset: Объект транзакции
        :param price: цена, пришедшая из request
        :return: Ничего не возвращает
        """
        if self.nds!=1 and price>0:
            models.Minfin.objects.create(
                price=price * (self.nds - 1),
                describe=queryset.describe,
                type_table=MinfinNDSView.minfin_type
            )


class MinfinEdaView(MinfinView):
    minfin_name = 'Еда'
    minfin_type = 0
    queryset = models.Minfin.objects.filter(type_table=minfin_type)
    template_name = 'Minfin/minfin_item.html'
    nds = 1.1


class MinfinAtractiveView(MinfinView):
    minfin_name = 'Развлечения'
    minfin_type = 1
    queryset = models.Minfin.objects.filter(type_table=minfin_type)
    template_name = 'Minfin/minfin_item.html'
    nds = 1.1


class MinfinRoadView(MinfinView):
    minfin_name = 'Проезд'
    minfin_type = 2
    queryset = models.Minfin.objects.filter(type_table=minfin_type)
    template_name = 'Minfin/minfin_item.html'
    nds = 1.1


class MinfinPhoneView(MinfinView):
    minfin_name = 'Телефон'
    minfin_type = 3
    queryset = models.Minfin.objects.filter(type_table=minfin_type)
    template_name = 'Minfin/minfin_item.html'


class MinfinDepreciationView(MinfinView):
    minfin_name = 'Амортизация'
    minfin_type = 4
    queryset = models.Minfin.objects.filter(type_table=minfin_type)
    template_name = 'Minfin/minfin_item.html'


class MinfinOtherView(MinfinView):
    minfin_name = 'Прочее'
    minfin_type = 5
    queryset = models.Minfin.objects.filter(type_table=minfin_type)
    template_name = 'Minfin/minfin_item.html'


class MinfinNDSView(MinfinView):
    minfin_name = 'НДС'
    minfin_type = 6
    queryset = models.Minfin.objects.filter(type_table=minfin_type)
    template_name = 'Minfin/minfin_item.html'
