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
from django.conf.urls.static import static
from django.views import generic

from . import views, models, forms
from NB4444 import settings
from django.contrib import admin


urlpatterns = [
    path('', views.GeneralPage.as_view(), name='general'),
    path('admin/', admin.site.urls),
    path('accounts/login/', views.Autorization.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),

    path('standartnie-vicheti/', views.StandartVichetiView.as_view(), name='standartnie_vicheti'),
    path('nlj/', views.NlgView.as_view(), name='nlj'),
    path(
        'plan/list/',
        generic.ListView.as_view(
            model=models.Plan,
            queryset=models.Plan.objects.select_related(),
            template_name="pages/plan/list.html"
        ),
        name='plan_list'
    ),
    path(
        'plan/<int:pk>/',
        generic.DetailView.as_view(
            model=models.Plan,
            template_name="pages/plan/detail.html"
        ),
        name='plan_detail'
    ),
    path(
        'plan/create/',
        generic.CreateView.as_view(
            model=models.Plan,
            form_class=forms.get_custom_model_form(models.Plan),
            template_name="pages/plan/create.html"
        ),
        name='plan_create'
    ),
    path(
        'plan/update/<int:pk>/',
        generic.UpdateView.as_view(
            model=models.Plan,
            form_class=forms.get_custom_model_form(models.Plan),
            template_name="pages/plan/update.html"
        ),
        name='plan_update'
    ),
    path(
        'plan/delete/<int:pk>/',
        generic.DeleteView.as_view(
            model=models.Plan,
            template_name='pages/plan/delete.html',
            success_url=reverse_lazy('plan_list')
        ),
        name='plan_delete'
    ),
    path(
        'plan/task/create/',
        generic.CreateView.as_view(
            model=models.Task,
            form_class=forms.get_custom_model_form(models.Task),
            template_name="pages/task/create.html"
        ),
        name='task_create'
    ),
    path(
        'plan/task/update/<int:pk>/',
        generic.UpdateView.as_view(
            model=models.Task,
            form_class=forms.get_custom_model_form(models.Task),
            template_name="pages/task/update.html"
        ),
        name='task_update'
    ),
    path(
        'plan/task/delete/<int:pk>/',
        generic.DeleteView.as_view(
            model=models.Task,
            template_name='pages/task/delete.html',
            success_url=reverse_lazy('plan_list')
        ),
        name='task_delete'
    ),
    path('bot-response/', views.get_bot_info, name='bot_response'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
