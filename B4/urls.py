"""NB4444 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, reverse_lazy
from django.views import generic

from . import forms, models, utils, views

app_name = 'b4'
urlpatterns = [
    path('', views.GeneralPage.as_view(), name='general'),
    path('accounts/login/', views.Autorization.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),

    path('default-deductions/', views.DefaultDeductionsView.as_view(), name='default_deductions'),
    path('note/', views.NoteView.as_view(), name='note'),
    path(
        'plan/',
        views.CustomListView.as_view(
            model=models.Plan,
            template_name="pages/plan/list.html"
        ),
        name='plan_list'
    ),
    path(
        'plan/<int:pk>/',
        views.CustomDetailView.as_view(
            model=models.Plan,
            template_name="pages/plan/detail.html"
        ),
        name='plan_detail'
    ),
    path(
        'plan/create/',
        utils.made_login_required_generic_class(generic.CreateView).as_view(
            model=models.Plan,
            form_class=forms.get_custom_model_form(models.Plan, fields_list=['name', 'user']),
            template_name="pages/plan/create.html"
        ),
        name='plan_create'
    ),
    path(
        'plan/update/<int:pk>/',
        views.CustomUpdateView.as_view(
            model=models.Plan,
            form_class=forms.get_custom_model_form(models.Plan, fields_list=['name', 'user']),
            template_name="pages/plan/update.html"
        ),
        name='plan_update'
    ),
    path(
        'plan/delete/<int:pk>/',
        utils.made_login_required_generic_class(generic.DeleteView).as_view(
            model=models.Plan,
            template_name='pages/plan/delete.html',
            success_url=reverse_lazy('b4:plan_list')
        ),
        name='plan_delete'
    ),
    path('plan/create-today-plan/', views.create_today_plan_task_view, name='plan_today_create'),
    # path(
    #     r'^plan-autocomplete/$', views.PlanAutocomplete.as_view(), name='plan_autocomplete',
    # ),
    path(
        'plan/task/create/',
        views.TaskCreateView.as_view(
            model=models.Task,
            # form_class=forms.get_custom_model_form(models.Task),
            form_class=forms.TaskModelForm,
            template_name="pages/task/create.html"
        ),
        name='task_create'
    ),
    path(
        'plan/task/update/<int:pk>/',
        utils.made_login_required_generic_class(generic.UpdateView).as_view(
            model=models.Task,
            form_class=forms.TaskModelForm,
            template_name="pages/task/update.html"
        ),
        name='task_update'
    ),
    path(
        'plan/task/delete/<int:pk>/',
        views.TaskDeleteView.as_view(
            model=models.Task,
            template_name='pages/task/delete.html',
        ),
        name='task_delete'
    ),
    path('bot-response/', views.get_bot_info_view, name='bot_response'),
]
