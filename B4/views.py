import threading

# from dal import autocomplete
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DeleteView
from django.views.generic.base import View

from B4 import forms, models, utils


class CustomView(View):
    model = None
    queryset = None

    def dispatch(self, request, *args, **kwargs):
        if self.model and not self.queryset:
            self.queryset = self.model.objects.all()
        if self.queryset and hasattr(self.model, 'user') \
                and request.user.is_authenticated and not request.user.is_superuser:
            self.queryset = self.queryset.filter(user=request.user)
        return super().dispatch(request, *args, **kwargs)


class CustomListView(LoginRequiredMixin, generic.ListView, CustomView):
    pass


class CustomDetailView(CustomView, LoginRequiredMixin, generic.DetailView):
    pass


class CustomUpdateView(CustomView, LoginRequiredMixin, generic.UpdateView):
    pass


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
            return redirect('b4:general')
        else:
            warning = 'Неверный логин или пароль!!!'
            return Autorization.get(request=request, warning=warning)


def logout(request):
    django_logout(request)
    return redirect('b4:login')


class GeneralPage(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        obj = models.Note.objects.filter(user=request.user).order_by("?").first()
        return render(request, 'pages/general.html', locals())


class DefaultDeductionsView(LoginRequiredMixin, CustomView):
    model = models.DefaultDeductions
    form = forms.DefaultDeductionModelForm

    def get(self, request):
        qs = self.model.objects.filter(user=request.user)
        obj = qs.last() if qs.exists() \
            else self.model(user=request.user)
        form = self.form(instance=obj)
        return render(request, 'pages/default_deductions/default_deduction.html', locals())

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            obj = form.save()
        return render(request, 'pages/default_deductions/default_deduction.html', locals())


class NoteView(LoginRequiredMixin, CustomView):
    model = models.Note

    def get(self, request):
        paginator = Paginator(self.queryset, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'pages/note/note.html', {'queryset': page_obj})

    def post(self, request):
        text = request.POST.get('text')
        image = request.FILES.get('image')
        if not text and not image:
            return redirect('b4:note')
        obj = models.Note(text=text, image=image, user=request.user)
        # search_template = r'\d{2}.\d{2}.\d{4}'
        # if text and re.match(search_template, request.POST.get('text')):
        #     obj.date = datetime.strptime(
        #         re.match(search_template, request.POST.get('text')).group(0),
        #         '%d.%m.%Y'
        #     )
        #     obj.text = text[11:].strip()
        try:
            obj.save()
        except Exception as e:
            print(e)
        return redirect('b4:note')


@login_required
def get_bot_info_view(request):
    from tele_bot import main
    t1 = threading.Thread(target=main.receive_records_from_telegramm_bot)
    t1.start()
    return redirect('b4:note')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task

    def render_to_response(self, context, **response_kwargs):
        plan_id = self.request.GET.get('plan_id')
        if plan_id:
            plan = models.Plan.objects.get(pk=plan_id)
            context['form'] = self.form_class(initial={"plan": plan})
        return super(TaskCreateView, self).render_to_response(context, **response_kwargs)

    def get_success_url(self):
        plan_id = self.object.plan_id
        return reverse_lazy('b4:plan_detail', kwargs={'pk': plan_id}) if plan_id else super().get_success_url()


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    def get_success_url(self):
        plan_id = self.object.plan_id
        return reverse_lazy('b4:plan_detail', kwargs={'pk': plan_id}) if plan_id else super().get_success_url()


@login_required
def create_today_plan_task_view(request):
    utils.PlanTask.create_today_plan(request.user.id)
    return redirect('b4:plan_list')


# class PlanAutocomplete(autocomplete.Select2QuerySetView):
#     model = models.Plan
#
#     def get_queryset(self):
#         self.queryset = self.model.objects.order_by('-id')
#         qs = super().get_queryset()
#         if self.model and not qs:
#             qs = self.model.objects.all()
#         if self.check_qs(qs):
#             qs = qs.filter(user=self.request.user)
#         return qs
#
#     def check_qs(self, qs):
#         return bool(
#             qs and (hasattr(self.model, 'user') or hasattr(self.model, 'plan') and hasattr(self.model, 'user'))
#             and self.request.user.is_authenticated and not self.request.user.is_superuser
#         )
