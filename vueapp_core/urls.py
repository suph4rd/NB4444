from django.urls import path

from vueapp_core import views

app_name = 'vueapp_core'
urlpatterns = [
    path('', views.index, name='index'),
]
