import threading

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DeleteView
from django.views.generic.base import View
from django.views.generic.edit import FormMixin

from B4 import forms, models, utils, mixins


class UserRecordMixin(View):
    model = None
    queryset = None

    def dispatch(self, request, *args, **kwargs):
        if self.model and not self.queryset:
            self.queryset = self.model.objects.all()
        if self.queryset and hasattr(self.model, 'user') \
                and request.user.is_authenticated and not request.user.is_superuser:
            self.queryset = self.queryset.filter(user=request.user)
        return super().dispatch(request, *args, **kwargs)


class CustomListView(LoginRequiredMixin, generic.ListView, UserRecordMixin, View):
    pass


class CustomDetailView(UserRecordMixin, LoginRequiredMixin, generic.DetailView, View):
    pass


class CustomUpdateView(UserRecordMixin, LoginRequiredMixin, generic.UpdateView, View):
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


class DefaultDeductionsView(LoginRequiredMixin, View):
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


class NoteListView(LoginRequiredMixin, mixins.NoteViewMixin, FormMixin, UserRecordMixin, generic.ListView):
    template_name = "pages/note/note.html"


class NoteCreateView(LoginRequiredMixin, mixins.NoteViewMixin, generic.CreateView):
    template_name = "pages/note/note.html"


class NoteUpdateView(LoginRequiredMixin, mixins.NoteViewMixin, generic.UpdateView):
    template_name = "pages/note/update_note.html"


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
            context['plan'] = plan
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

