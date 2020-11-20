import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# ___________________________________________LOGIN_PAGE_____________________________________________________________________
# _________________________________________________________________________________________________________________________
from django.views import View

from B4.forms import UserForm
from B4.models import standart_vichet, nlg, minfin, eda, nds, transport, razvlechenia, amortizatia, prochee
from NB4444 import settings


class General(View):
    def loginPage(request):
        # Форма входа
        userform = UserForm()
        #   авторизация
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            # непосредственная авторизация
            user = authenticate(request, username=username, password=password)

            # валидация авторизации
            if user is not None:
                login(request, user)

                return redirect(General.general)

        return render(request, 'login.html', {'userform': userform})

    #___________Выход__________________________________________________________________________________
    def logoutPage(request):
        #   выход
        logout(request)
        return redirect('login')

    #____________Главная_________________________________________________________________________________
    @login_required()
    def general(request):
        return render(request, 'general.html', {})

#__________НЛЖ___________________________________________________________________________________
@login_required()
def nlj(request):
    all_nlj = nlg.objects.all().order_by('-date_nlg').order_by('-id')
    now_date = datetime.datetime.now()

    # порядковые номера для вывода
    len_nlj = nlg.objects.count() + 1
    for nlj in all_nlj:
        nlj.id = str((nlj.id - len_nlj) * (-1)) +'.'

    # Валидация формы
    if request.method == 'POST':
        if request.POST.get('text_nlg') and request.FILES.get('image_nlg'):
            nlg.objects.create(date_nlg=now_date, text_nlg=request.POST.get('text_nlg'), image_nlg=request.FILES.get('image_nlg'))
        elif request.POST.get('text_nlg'):
            nlg.objects.create(date_nlg=now_date, text_nlg=request.POST.get('text_nlg'))
        elif request.FILES.get('image_nlg'):
            nlg.objects.create(date_nlg=now_date, image_nlg=request.FILES.get('image_nlg'))
    return render(request, 'NLJ.html', {'all_nlj':all_nlj,
                                        'MEDIA_URL':settings.MEDIA_URL,
                                        })

#____________Стандартные_Вычеты________________________________________________________________________________
@login_required()
def standartnie_vicheti(request):
    now_date = str(datetime.datetime.now().date())
    # Получаем данные из БД
    last_vicheti = standart_vichet.objects.last()
    print(last_vicheti)
    if last_vicheti==None:
        standart_vichet.objects.create(hata=0, proezd=0,mobila=0,eda=0)
        last_vicheti = standart_vichet.objects.last()
    last_vicheti.itogo = float(last_vicheti.hata) + \
                         float(last_vicheti.proezd) + \
                         float(last_vicheti.mobila) + \
                         float(last_vicheti.eda)
    # Валидация формы
    if request.method == 'POST':
        if request.POST.get('hata') \
                and request.POST.get('proezd') \
                and request.POST.get('mobila') \
                and request.POST.get('eda'):
            if request.POST.get('hata') != last_vicheti.hata \
                    or request.POST.get('proezd') != last_vicheti.proezd \
                    or request.POST.get('mobila') != last_vicheti.mobila \
                    or request.POST.get('eda') != last_vicheti.eda:
                standart_vichet.objects.create(hata=request.POST.get('hata'),
                                               proezd=request.POST.get('proezd'),
                                               mobila=request.POST.get('mobila'),
                                               eda=request.POST.get('eda'))
                # Пересчитываем переменные
                last_vicheti.hata = request.POST.get('hata')
                last_vicheti.proezd = request.POST.get('proezd')
                last_vicheti.mobila = request.POST.get('mobila')
                last_vicheti.eda = request.POST.get('eda')
                last_vicheti.itogo = float(last_vicheti.hata) + \
                                     float(last_vicheti.proezd) + \
                                     float(last_vicheti.mobila) + \
                                     float(last_vicheti.eda)

    return render(request, 'standart_vichet.html', {'last_vicheti':last_vicheti})


class Minfin(View):
    #________________Минфин_____________________________________________________________________________
    @login_required()
    def minfin(request):
        all_minfin = minfin.objects.all().order_by('-date_minfin').order_by('-id')

        # порядковые номера для вывода
        len_minfin = minfin.objects.count() + 1
        for minfinloc in all_minfin:
            minfinloc.id = str((minfinloc.id - len_minfin) * (-1)) + '.'

        # Инициализация остатка
        last_ostatoc = minfin.objects.last()
        if last_ostatoc == None:
            last_ostatoc = 0
        else:
            last_ostatoc = last_ostatoc.ostatoc_minfin
        return render(request, 'Minfin/minfin.html', {'all_minfin':all_minfin,
                                                      'last_ostatoc':last_ostatoc
                                                      })

    #________________Еда_____________________________________________________________________________
    @login_required()
    def minfin_eda(request):
        # Переменные
        all_eda = eda.objects.all().order_by('-date_eda').order_by('-id')
        percent_nds = 0.1
        now_date = datetime.datetime.now()

        # порядковые номера для вывода
        len_eda = eda.objects.count() + 1
        for edaloc in all_eda:
            edaloc.id = str((edaloc.id - len_eda) * (-1)) + '.'

        # Инициализация остатка
        last_ostatoc = eda.objects.last()
        if last_ostatoc == None:
            last_ostatoc = 0
        else:
            last_ostatoc = last_ostatoc.ostatoc_eda
        # Валидация формы
        if request.method == 'POST':
            if request.POST.get('eda'):
                sum_eda = request.POST.get('eda').split()[0]
                # проверка на отрицательное число
                if float(sum_eda) < 0:
                    percent_nds = 0
                describe_eda = request.POST.get('eda')[request.POST.get('eda').index(' ')+1:]

                # Новый экземпляр Minfin
                last_ostatoc_minfin = minfin.objects.last()
                # Инициализация остатка
                if last_ostatoc_minfin == None:
                    last_ostatoc_minfin = 0
                else:
                    last_ostatoc_minfin = last_ostatoc_minfin.ostatoc_minfin
                last_ostatoc_minfin = int(float(last_ostatoc_minfin)*100)/100 - int(float(sum_eda)*100)/100
                minfin.objects.create(date_minfin=now_date, ostatoc_minfin=last_ostatoc_minfin,
                                      sum_minfin=sum_eda, describe_minfin='(Еда) ' + describe_eda)

                # Новый экземпляр Nds
                last_ostatoc_nds = nds.objects.last()
                # Инициализация остатка
                if last_ostatoc_nds == None:
                    last_ostatoc_nds = 0
                else:
                    last_ostatoc_nds = last_ostatoc_nds.ostatoc_nds
                sum_eda = int(float(request.POST.get('eda').split()[0])*100)/100 * percent_nds
                last_ostatoc_nds = int(float(last_ostatoc_nds)*100)/100 - int(float(sum_eda)*100)/100
                nds.objects.create(date_nds=now_date, ostatoc_nds=last_ostatoc_nds,
                                      sum_nds=sum_eda, describe_nds='(Еда) ' + describe_eda)
                # добавляем операцию в Минфин
                last_ostatoc_minfin = int(float(last_ostatoc_minfin) * 100) / 100 - int(float(sum_eda * percent_nds) * 100) / 100
                minfin.objects.create(date_minfin=now_date, ostatoc_minfin=last_ostatoc_minfin,
                                      sum_minfin=int(float(sum_eda) * percent_nds * 100) / 100, describe_minfin='(НДС) ' + describe_eda)

                # Новый экземпляр Eda
                sum_eda = int(int(float(request.POST.get('eda').split()[0]) * 100) / 100 * (percent_nds + 1) * 100) / 100
                ostatoc_eda = int(float(last_ostatoc)*100)/100 - sum_eda
                last_ostatoc = ostatoc_eda
                eda.objects.create(date_eda=now_date, ostatoc_eda=ostatoc_eda,
                               sum_eda=sum_eda, describe_eda=describe_eda)
        return render(request, 'Minfin/minfin_eda.html', {'all_eda':all_eda,
                                                          'last_ostatoc':last_ostatoc})

    #________________Транспорт_____________________________________________________________________________
    @login_required(login_url='login/')
    def minfin_transport(request):
        # Переменные
        all_transport = transport.objects.all().order_by('-date_transport').order_by('-id')
        percent_nds = 0.03
        now_date = datetime.datetime.now()

        # порядковые номера для вывода
        len_transport = transport.objects.count() + 1
        for transportloc in all_transport:
            transportloc.id = str((transportloc.id - len_transport) * (-1)) + '.'

        # Инициализация остатка
        last_ostatoc = transport.objects.last()
        if last_ostatoc == None:
            last_ostatoc = 0
        else:
            last_ostatoc = last_ostatoc.ostatoc_transport
        # Валидация формы
        if request.method == 'POST':
            if request.POST.get('transport'):
                sum_transport = request.POST.get('transport').split()[0]
                # проверка на отрицательное число
                if float(sum_transport) < 0:
                    percent_nds = 0
                describe_transport = request.POST.get('transport')[request.POST.get('transport').index(' ') + 1:]

                # Новый экземпляр Minfin
                last_ostatoc_minfin = minfin.objects.last()
                # Инициализация остатка
                if last_ostatoc_minfin == None:
                    last_ostatoc_minfin = 0
                else:
                    last_ostatoc_minfin = last_ostatoc_minfin.ostatoc_minfin
                last_ostatoc_minfin = int(float(last_ostatoc_minfin) * 100) / 100 - int(float(sum_transport) * 100) / 100
                minfin.objects.create(date_minfin=now_date, ostatoc_minfin=last_ostatoc_minfin,
                                      sum_minfin=sum_transport, describe_minfin='(Транспорт) ' + describe_transport)

                # Новый экземпляр Nds
                last_ostatoc_nds = nds.objects.last()
                # Инициализация остатка
                if last_ostatoc_nds == None:
                    last_ostatoc_nds = 0
                else:
                    last_ostatoc_nds = last_ostatoc_nds.ostatoc_nds
                sum_transport = int(float(request.POST.get('transport').split()[0]) * 100) / 100 * percent_nds
                last_ostatoc_nds = int(float(last_ostatoc_nds) * 100) / 100 - int(float(sum_transport) * 100) / 100
                nds.objects.create(date_nds=now_date, ostatoc_nds=last_ostatoc_nds,
                                   sum_nds=sum_transport, describe_nds='(Транспорт) ' + describe_transport)
                # добавляем операцию в Минфин
                last_ostatoc_minfin = int(float(last_ostatoc_minfin) * 100) / 100 - int(
                    float(sum_transport * percent_nds) * 100) / 100
                minfin.objects.create(date_minfin=now_date, ostatoc_minfin=last_ostatoc_minfin,
                                      sum_minfin=int(float(sum_transport) * percent_nds * 100) / 100,
                                      describe_minfin='(НДС) ' + describe_transport)

                # Новый экземпляр transport
                sum_transport = int(int(float(request.POST.get('transport').split()[0]) * 100) / 100 * (percent_nds + 1) * 100) / 100
                ostatoc_transport = int(float(last_ostatoc) * 100) / 100 - sum_transport
                last_ostatoc = ostatoc_transport
                transport.objects.create(date_transport=now_date, ostatoc_transport=ostatoc_transport,
                                   sum_transport=sum_transport, describe_transport=describe_transport)
        return render(request, 'Minfin/minfin_transport.html', {'all_transport':all_transport,
                                                                'last_ostatoc':last_ostatoc})

    #________________Развлечения_____________________________________________________________________________
    @login_required(login_url='login/')
    def minfin_razvlechenia(request):
        # Переменные
        all_razvlechenia = razvlechenia.objects.all().order_by('-date_razvlechenia').order_by('-id')
        percent_nds = 0.3
        now_date = datetime.datetime.now()

        # порядковые номера для вывода
        len_razvlechenia = razvlechenia.objects.count() + 1
        for razvlechenialoc in all_razvlechenia:
            razvlechenialoc.id = str((razvlechenialoc.id - len_razvlechenia) * (-1)) + '.'

        # Инициализация остатка
        last_ostatoc = razvlechenia.objects.last()
        if last_ostatoc == None:
            last_ostatoc = 0
        else:
            last_ostatoc = last_ostatoc.ostatoc_razvlechenia
        # Валидация формы
        if request.method == 'POST':
            if request.POST.get('razvlechenia'):
                sum_razvlechenia = request.POST.get('razvlechenia').split()[0]
                # проверка на отрицательное число
                if float(sum_razvlechenia) < 0:
                    percent_nds = 0
                describe_razvlechenia = request.POST.get('razvlechenia')[request.POST.get('razvlechenia').index(' ') + 1:]

                # Новый экземпляр Minfin
                last_ostatoc_minfin = minfin.objects.last()
                # Инициализация остатка
                if last_ostatoc_minfin == None:
                    last_ostatoc_minfin = 0
                else:
                    last_ostatoc_minfin = last_ostatoc_minfin.ostatoc_minfin
                last_ostatoc_minfin = int(float(last_ostatoc_minfin) * 100) / 100 - int(
                    float(sum_razvlechenia) * 100) / 100
                minfin.objects.create(date_minfin=now_date, ostatoc_minfin=last_ostatoc_minfin,
                                      sum_minfin=sum_razvlechenia, describe_minfin='(Развлечения) ' + describe_razvlechenia)

                # Новый экземпляр Nds
                last_ostatoc_nds = nds.objects.last()
                # Инициализация остатка
                if last_ostatoc_nds == None:
                    last_ostatoc_nds = 0
                else:
                    last_ostatoc_nds = last_ostatoc_nds.ostatoc_nds
                sum_razvlechenia = int(float(request.POST.get('razvlechenia').split()[0]) * 100) / 100 * percent_nds
                last_ostatoc_nds = int(float(last_ostatoc_nds) * 100) / 100 - int(float(sum_razvlechenia) * 100) / 100
                nds.objects.create(date_nds=now_date, ostatoc_nds=last_ostatoc_nds,
                                   sum_nds=sum_razvlechenia, describe_nds='(Развлечения) ' + describe_razvlechenia)
                # добавляем операцию в Минфин
                last_ostatoc_minfin = int(float(last_ostatoc_minfin) * 100) / 100 - int(
                    float(sum_razvlechenia * percent_nds) * 100) / 100
                minfin.objects.create(date_minfin=now_date, ostatoc_minfin=last_ostatoc_minfin,
                                      sum_minfin=int(float(sum_razvlechenia) * percent_nds * 100) / 100,
                                      describe_minfin='(НДС) ' + describe_razvlechenia)

                # Новый экземпляр razvlechenia
                sum_razvlechenia = int(int(float(request.POST.get('razvlechenia').split()[0]) * 100) / 100 * (percent_nds + 1) * 100) / 100
                ostatoc_razvlechenia = int(float(last_ostatoc) * 100) / 100 - sum_razvlechenia
                last_ostatoc = ostatoc_razvlechenia
                razvlechenia.objects.create(date_razvlechenia=now_date, ostatoc_razvlechenia=ostatoc_razvlechenia,
                                         sum_razvlechenia=sum_razvlechenia, describe_razvlechenia=describe_razvlechenia)
        return render(request, 'Minfin/minfin_razvlechenia.html', {'all_razvlechenia':all_razvlechenia,
                                                                   'last_ostatoc':last_ostatoc})

    #_______________Амортизация______________________________________________________________________________
    @login_required(login_url='login/')
    def minfin_ammortizatia(request):
        # Переменные
        all_amortizatia = amortizatia.objects.all().order_by('-date_amortizatia').order_by('-id')
        percent_nds = 0.1
        now_date = datetime.datetime.now()

        # порядковые номера для вывода
        len_amortizatia = amortizatia.objects.count() + 1
        for amortizatialoc in all_amortizatia:
            amortizatialoc.id = str((amortizatialoc.id - len_amortizatia) * (-1)) + '.'

        # Инициализация остатка
        last_ostatoc = amortizatia.objects.last()
        if last_ostatoc == None:
            last_ostatoc = 0
        else:
            last_ostatoc = last_ostatoc.ostatoc_amortizatia
        # Валидация формы
        if request.method == 'POST':
            if request.POST.get('amortizatia'):
                sum_amortizatia = request.POST.get('amortizatia').split()[0]
                # проверка на отрицательное число
                if float(sum_amortizatia) < 0:
                    percent_nds = 0
                describe_amortizatia = request.POST.get('amortizatia')[
                                        request.POST.get('amortizatia').index(' ') + 1:]

                # Новый экземпляр Minfin
                last_ostatoc_minfin = minfin.objects.last()
                # Инициализация остатка
                if last_ostatoc_minfin == None:
                    last_ostatoc_minfin = 0
                else:
                    last_ostatoc_minfin = last_ostatoc_minfin.ostatoc_minfin
                last_ostatoc_minfin = int(float(last_ostatoc_minfin) * 100) / 100 - int(
                    float(sum_amortizatia) * 100) / 100
                minfin.objects.create(date_minfin=now_date, ostatoc_minfin=last_ostatoc_minfin,
                                      sum_minfin=sum_amortizatia,
                                      describe_minfin='(Амортизация) ' + describe_amortizatia)

                # Новый экземпляр Nds
                last_ostatoc_nds = nds.objects.last()
                # Инициализация остатка
                if last_ostatoc_nds == None:
                    last_ostatoc_nds = 0
                else:
                    last_ostatoc_nds = last_ostatoc_nds.ostatoc_nds
                sum_amortizatia = int(float(request.POST.get('amortizatia').split()[0]) * 100) / 100 * percent_nds
                last_ostatoc_nds = int(float(last_ostatoc_nds) * 100) / 100 - int(float(sum_amortizatia) * 100) / 100
                nds.objects.create(date_nds=now_date, ostatoc_nds=last_ostatoc_nds,
                                   sum_nds=sum_amortizatia, describe_nds='(Амортизация) ' + describe_amortizatia)
                # добавляем операцию в Минфин
                last_ostatoc_minfin = int(float(last_ostatoc_minfin) * 100) / 100 - int(
                    float(sum_amortizatia * percent_nds) * 100) / 100
                minfin.objects.create(date_minfin=now_date, ostatoc_minfin=last_ostatoc_minfin,
                                      sum_minfin=int(float(sum_amortizatia) * percent_nds * 100) / 100,
                                      describe_minfin='(НДС) ' + describe_amortizatia)

                # Новый экземпляр amortizatia
                sum_amortizatia = int(int(float(request.POST.get('amortizatia').split()[0]) * 100) / 100 * (percent_nds + 1) *100) / 100
                ostatoc_amortizatia = int(float(last_ostatoc) * 100) / 100 - sum_amortizatia
                last_ostatoc = ostatoc_amortizatia
                amortizatia.objects.create(date_amortizatia=now_date, ostatoc_amortizatia=ostatoc_amortizatia,
                                            sum_amortizatia=sum_amortizatia,
                                            describe_amortizatia=describe_amortizatia)
        return render(request, 'Minfin/minfin_amortizatia.html', {'all_amortizatia':all_amortizatia,
                                                                   'last_ostatoc':last_ostatoc})

    #_______________Прочее______________________________________________________________________________
    @login_required(login_url='login/')
    def minfin_prochee(request):
        # Переменные
        all_prochee = prochee.objects.all().order_by('-date_prochee').order_by('-id')
        percent_nds = 0.05
        now_date = datetime.datetime.now()

        # порядковые номера для вывода
        len_prochee = prochee.objects.count() + 1
        for procheeloc in all_prochee:
            procheeloc.id = str((procheeloc.id - len_prochee) * (-1)) + '.'

        # Инициализация остатка
        last_ostatoc = prochee.objects.last()
        if last_ostatoc == None:
            last_ostatoc = 0
        else:
            last_ostatoc = last_ostatoc.ostatoc_prochee
        # Валидация формы
        if request.method == 'POST':
            if request.POST.get('prochee'):
                sum_prochee = request.POST.get('prochee').split()[0]
                # проверка на отрицательное число
                if float(sum_prochee)<0:
                    percent_nds = 0
                describe_prochee = request.POST.get('prochee')[
                                        request.POST.get('prochee').index(' ') + 1:]

                # Новый экземпляр Minfin
                last_ostatoc_minfin = minfin.objects.last()
                # Инициализация остатка
                if last_ostatoc_minfin == None:
                    last_ostatoc_minfin = 0
                else:
                    last_ostatoc_minfin = last_ostatoc_minfin.ostatoc_minfin
                last_ostatoc_minfin = int(float(last_ostatoc_minfin) * 100) / 100 - int(
                    float(sum_prochee) * 100) / 100
                minfin.objects.create(date_minfin=now_date, ostatoc_minfin=last_ostatoc_minfin,
                                      sum_minfin=sum_prochee,
                                      describe_minfin='(Прочее) ' + describe_prochee)

                # Новый экземпляр Nds
                last_ostatoc_nds = nds.objects.last()
                # Инициализация остатка
                if last_ostatoc_nds == None:
                    last_ostatoc_nds = 0
                else:
                    last_ostatoc_nds = last_ostatoc_nds.ostatoc_nds
                sum_prochee = int(float(request.POST.get('prochee').split()[0]) * 100) / 100 * percent_nds
                last_ostatoc_nds = int(float(last_ostatoc_nds) * 100) / 100 - int(float(sum_prochee) * 100) / 100
                nds.objects.create(date_nds=now_date, ostatoc_nds=last_ostatoc_nds,
                                   sum_nds=sum_prochee, describe_nds='(Прочее) ' + describe_prochee)
                # добавляем операцию в Минфин
                last_ostatoc_minfin = int(float(last_ostatoc_minfin) * 100) / 100 - int(
                    float(sum_prochee * percent_nds) * 100) / 100
                minfin.objects.create(date_minfin=now_date, ostatoc_minfin=last_ostatoc_minfin,
                                      sum_minfin=int(float(sum_prochee) * percent_nds * 100) / 100,
                                      describe_minfin='(НДС) ' + describe_prochee)

                # Новый экземпляр prochee
                sum_prochee = int(
                    int(float(request.POST.get('prochee').split()[0]) * 100) / 100 * (percent_nds + 1) * 100) / 100
                ostatoc_prochee = int(float(last_ostatoc) * 100) / 100 - sum_prochee
                last_ostatoc = ostatoc_prochee
                prochee.objects.create(date_prochee=now_date, ostatoc_prochee=ostatoc_prochee,
                                            sum_prochee=sum_prochee,
                                            describe_prochee=describe_prochee)
        return render(request, 'Minfin/minfin_prochee.html', {'all_prochee':all_prochee,
                                                                   'last_ostatoc':last_ostatoc})

    #______________НДС_______________________________________________________________________________
    @login_required(login_url='login/')
    def minfin_nds(request):
        all_nds = nds.objects.all().order_by('-date_nds').order_by('-id')
        # Инициализация остатка
        last_ostatoc = nds.objects.last()
        now_date = datetime.datetime.now()

        # порядковые номера для вывода
        len_nds = nds.objects.count() + 1
        for ndsloc in all_nds:
            ndsloc.id = str((ndsloc.id - len_nds) * (-1)) + '.'

        if last_ostatoc == None:
            last_ostatoc = 0
        else:
            last_ostatoc = last_ostatoc.ostatoc_nds
        # Валидация формы
        if request.method == 'POST':
            if request.POST.get('nds'):
                # Новый экземпляр nds
                sum_nds = int(float(request.POST.get('nds').split()[0]) * 100) / 100
                ostatoc_nds = int(float(last_ostatoc) * 100) / 100 - sum_nds
                last_ostatoc = ostatoc_nds
                describe_nds = request.POST.get('nds')[
                                   request.POST.get('nds').index(' ') + 1:]
                nds.objects.create(date_nds=now_date, ostatoc_nds=ostatoc_nds,
                                       sum_nds=sum_nds,
                                       describe_nds=describe_nds)

                # добавляем операцию в Минфин
                last_ostatoc_minfin = minfin.objects.last()
                # Инициализация остатка
                if last_ostatoc_minfin == None:
                    last_ostatoc_minfin = 0
                else:
                    last_ostatoc_minfin = last_ostatoc_minfin.ostatoc_minfin
                last_ostatoc_minfin = int(float(last_ostatoc_minfin) * 100) / 100 - int(
                    float(sum_nds) * 100) / 100
                minfin.objects.create(date_minfin=now_date, ostatoc_minfin=last_ostatoc_minfin,
                                      sum_minfin=int(float(sum_nds) * 100) / 100,
                                      describe_minfin='(НДС) ' + describe_nds)
        return render(request, 'Minfin/minfin_nds.html', {'all_nds':all_nds,
                                                          'last_ostatoc':last_ostatoc})
