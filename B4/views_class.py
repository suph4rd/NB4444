import re
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic.base import View

from B4.forms import UserForm
from B4.models import standart_vichet, nlg, minfin, eda, transport, razvlechenia, amortizatia, prochee, nds
from NB4444.settings import MEDIA_URL


class Autorization(View):
    '''Авторизация'''
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
    '''Выход из профиля'''
    def get(self, request):
        logout(request)
        return redirect('login')


class General_page(LoginRequiredMixin, View):
    '''Главная страница'''
    def get(self, request):
        return render(request, 'general.html', {})


class Standartnie_vicheti(View):
    '''Стандартные вычеты'''
    def get(self, request):
        queryset = standart_vichet.objects.last()
        return render(request, 'standart_vichet.html', {'last_vicheti': queryset})


    def post(self, request):
        queryset = standart_vichet(
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
            return Standartnie_vicheti.get(self, request)


class Nlg(View):
    '''Направление личной жизни'''
    def get(self, request):
        queryset = nlg.objects.all()
        paginator = Paginator(queryset, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'NLJ.html', {'queryset': page_obj,
                                            'MEDIA_URL': MEDIA_URL})

    def post(self, request):
        text_nlg = request.POST.get('text_nlg')
        image_nlg = request.FILES.get('image_nlg')

        if not text_nlg and not image_nlg:
            return Nlg.get(self, request)
        queryset = nlg(text_nlg=text_nlg, image_nlg=image_nlg)


        if text_nlg and re.match(r'\d{2}.\d{2}.\d{4}', request.POST.get('text_nlg')):
            queryset.date_nlg = datetime.strptime(re.match(r'\d{2}.\d{2}.\d{4}', request.POST.get('text_nlg')).group(0), '%d.%m.%Y')
            queryset.text_nlg = text_nlg[11:].strip()
        try:
            queryset.save()
        except Exception as e:
            print(e)
        finally:
            return Nlg.get(self, request)


class Minfin(View):
    '''МинФин'''
    def get(self, request):
        queryset = minfin.objects.all()

        if queryset:
            last_ostatoc = eda.objects.first().ostatoc_eda
        else:
            last_ostatoc = 0

        paginator = Paginator(queryset, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Minfin\minfin.html', {'queryset': page_obj,
                                                      'last_ostatoc': last_ostatoc})



class Minfin_eda(View):
    '''Еда'''
    def get(self, request):
        queryset = eda.objects.all()        # все записи

        if queryset:
            last_ostatoc = eda.objects.first().ostatoc_eda  # актуальный остаток
        else:
            last_ostatoc = 0

        paginator = Paginator(queryset, 50)     # Пагинация из 50 страниц
        page_number = request.GET.get('page')   # номер текущей страницы
        page_obj = paginator.get_page(page_number)  # записи для текущей страницы

        return render(request, 'Minfin\minfin_eda.html', {'queryset': page_obj,
                                                          'last_ostatoc': last_ostatoc})

    def post(self, request):
        text_input = request.POST.get('eda')  # текст из формы

        if not text_input:
            '''Проверка Not Null формы'''
            return Minfin_eda.get(self, request)

        queryset = eda()    # инициализируем новый объект БД

        try:
            if re.match(r'-\d+.\d+', text_input):
                sum = re.match(r'-\d+.\d+', text_input)     # дробная отрицательная сумма
            elif re.match(r'\d+.\d+', text_input):
                sum = re.match(r'\d+.\d+', text_input)      # дробная сумма
            elif re.match(r'-\d+', text_input):
                sum = re.match(r'-\d+', text_input)  # достаём сумму, если она отрицательная
            else:
                sum = re.match(r'\d+', text_input)   # достаём сумму

            queryset.sum_eda = float(sum.group())
            queryset.ostatoc_eda = 0
            queryset.describe_eda = text_input[sum.end()+1:].strip()
            queryset.save()

        except Exception as e:
            print(e)
        finally:
            return Minfin_eda.get(self, request)


class Minfin_transport(View):
    '''Транспорт'''
    def get(self, request):
        queryset = transport.objects.all()

        if queryset:
            last_ostatoc = transport.objects.first().ostatoc_transport
        else:
            last_ostatoc = 0

        paginator = Paginator(queryset, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Minfin\minfin_transport.html', {'queryset': page_obj,
                                                                'last_ostatoc': last_ostatoc})

    def post(self, request):
        text_input = request.POST.get('transport')  # текст из формы

        if not text_input:
            '''Проверка Not Null формы'''
            return Minfin_transport.get(self, request)

        queryset = transport()    # инициализируем новый объект БД

        try:
            if re.match(r'-\d+.\d+', text_input):
                sum = re.match(r'-\d+.\d+', text_input)     # дробная отрицательная сумма
            elif re.match(r'\d+.\d+', text_input):
                sum = re.match(r'\d+.\d+', text_input)      # дробная сумма
            elif re.match(r'-\d+', text_input):
                sum = re.match(r'-\d+', text_input)  # достаём сумму, если она отрицательная
            else:
                sum = re.match(r'\d+', text_input)   # достаём сумму

            queryset.sum_transport = float(sum.group())
            queryset.ostatoc_transport = 0
            queryset.describe_transport = text_input[sum.end()+1:].strip()
            queryset.save()

        except Exception as e:
            print(e)
        finally:
            return Minfin_transport.get(self, request)


class Minfin_razvlechenia(View):
    '''Развлечения'''
    def get(self, request):
        queryset = razvlechenia.objects.all()

        if queryset:
            last_ostatoc = razvlechenia.objects.first().ostatoc_razvlechenia
        else:
            last_ostatoc = 0

        paginator = Paginator(queryset, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Minfin\minfin_razvlechenia.html', {'queryset': page_obj,
                                                                  'last_ostatoc': last_ostatoc})

    def post(self, request):
        text_input = request.POST.get('razvlechenia')  # текст из формы

        if not text_input:
            '''Проверка Not Null формы'''
            return Minfin_razvlechenia.get(self, request)

        queryset = razvlechenia()    # инициализируем новый объект БД

        try:
            if re.match(r'-\d+.\d+', text_input):
                sum = re.match(r'-\d+.\d+', text_input)     # дробная отрицательная сумма
            elif re.match(r'\d+.\d+', text_input):
                sum = re.match(r'\d+.\d+', text_input)      # дробная сумма
            elif re.match(r'-\d+', text_input):
                sum = re.match(r'-\d+', text_input)  # достаём сумму, если она отрицательная
            else:
                sum = re.match(r'\d+', text_input)   # достаём сумму

            queryset.sum_razvlechenia = float(sum.group())
            queryset.ostatoc_razvlechenia = 0
            queryset.describe_razvlechenia = text_input[sum.end()+1:].strip()
            queryset.save()

        except Exception as e:
            print(e)
        finally:
            return Minfin_razvlechenia.get(self, request)


class Minfin_amortizatia(View):
    '''Аммортизация'''
    def get(self, request):
        queryset = amortizatia.objects.all()

        if queryset:
            last_ostatoc = amortizatia.objects.first().ostatoc_amortizatia
        else:
            last_ostatoc = 0

        paginator = Paginator(queryset, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Minfin\minfin_amortizatia.html', {'queryset': page_obj,
                                                                  'last_ostatoc': last_ostatoc})

    def post(self, request):
        text_input = request.POST.get('amortizatia')  # текст из формы

        if not text_input:
            '''Проверка Not Null формы'''
            return Minfin_amortizatia.get(self, request)

        queryset = amortizatia()    # инициализируем новый объект БД

        try:
            if re.match(r'-\d+.\d+', text_input):
                sum = re.match(r'-\d+.\d+', text_input)     # дробная отрицательная сумма
            elif re.match(r'\d+.\d+', text_input):
                sum = re.match(r'\d+.\d+', text_input)      # дробная сумма
            elif re.match(r'-\d+', text_input):
                sum = re.match(r'-\d+', text_input)  # достаём сумму, если она отрицательная
            else:
                sum = re.match(r'\d+', text_input)   # достаём сумму

            queryset.sum_amortizatia = float(sum.group())
            queryset.ostatoc_amortizatia = 0
            queryset.describe_amortizatia = text_input[sum.end()+1:].strip()
            queryset.save()

        except Exception as e:
            print(e)
        finally:
            return Minfin_amortizatia.get(self, request)


class Minfin_prochee(View):
    '''Прочее'''
    def get(self, request):
        queryset = prochee.objects.all()

        if queryset:
            last_ostatoc = prochee.objects.first().ostatoc_prochee
        else:
            last_ostatoc = 0

        paginator = Paginator(queryset, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Minfin\minfin_prochee.html', {'queryset': page_obj,
                                                              'last_ostatoc': last_ostatoc})

    def post(self, request):
        text_input = request.POST.get('prochee')  # текст из формы

        if not text_input:
            '''Проверка Not Null формы'''
            return Minfin_prochee.get(self, request)

        queryset = prochee()    # инициализируем новый объект БД

        try:
            if re.match(r'-\d+.\d+', text_input):
                sum = re.match(r'-\d+.\d+', text_input)     # дробная отрицательная сумма
            elif re.match(r'\d+.\d+', text_input):
                sum = re.match(r'\d+.\d+', text_input)      # дробная сумма
            elif re.match(r'-\d+', text_input):
                sum = re.match(r'-\d+', text_input)  # достаём сумму, если она отрицательная
            else:
                sum = re.match(r'\d+', text_input)   # достаём сумму

            queryset.sum_prochee = float(sum.group())
            queryset.ostatoc_prochee = 0
            queryset.describe_prochee = text_input[sum.end()+1:].strip()
            queryset.save()

        except Exception as e:
            print(e)
        finally:
            return Minfin_prochee.get(self, request)


class Minfin_nds(View):
    '''Ндс'''
    def get(self, request):
        queryset = nds.objects.all()

        if queryset:
            last_ostatoc = nds.objects.first().ostatoc_nds
        else:
            last_ostatoc = 0

        paginator = Paginator(queryset, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Minfin\minfin_nds.html', {'queryset': page_obj,
                                                          'last_ostatoc': last_ostatoc})

    def post(self, request):
        text_input = request.POST.get('nds')  # текст из формы

        if not text_input:
            '''Проверка Not Null формы'''
            return Minfin_nds.get(self, request)

        queryset = nds()    # инициализируем новый объект БД

        try:
            if re.match(r'-\d+.\d+', text_input):
                sum = re.match(r'-\d+.\d+', text_input)     # дробная отрицательная сумма
            elif re.match(r'\d+.\d+', text_input):
                sum = re.match(r'\d+.\d+', text_input)      # дробная сумма
            elif re.match(r'-\d+', text_input):
                sum = re.match(r'-\d+', text_input)  # достаём сумму, если она отрицательная
            else:
                sum = re.match(r'\d+', text_input)   # достаём сумму

            queryset.sum_nds = float(sum.group())
            queryset.ostatoc_nds = 0
            queryset.describe_nds = text_input[sum.end()+1:].strip()
            queryset.save()

        except Exception as e:
            print(e)
        finally:
            return Minfin_nds.get(self, request)




