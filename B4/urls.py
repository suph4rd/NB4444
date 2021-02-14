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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from B4 import views_class
from NB4444 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views_class.Autorization.as_view(), name='login'),
    path('logout/', views_class.Logout.as_view(), name='logout'),
    path('', views_class.GeneralPage.as_view(), name='general'),
    path('standartnie_vicheti/', views_class.StandartVichetiView.as_view(), name='standartnie_vicheti'),
    path('nlj/', views_class.NlgView.as_view(), name='nlj'),
    path('minfin/', views_class.MinfinView.as_view(), name='minfin'),
    path('minfin_eda/', views_class.MinfinEdaView.as_view(), name='minfin_eda'),
    path('minfin_transport', views_class.MinfinRoadView.as_view(), name='minfin_transport'),
    path('minfin_razvlechenia/', views_class.MinfinAtractiveView.as_view(), name='minfin_razvlechenia'),
    path('minfin_ammortizatia/', views_class.MinfinDepreciationView.as_view(), name='minfin_ammortizatia'),
    path('minfin_prochee/', views_class.MinfinOtherView.as_view(), name='minfin_prochee'),
    path('minfin_nds/', views_class.MinfinNDSView.as_view(), name='minfin_nds'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('accounts/login/', views.General.loginPage, name='login'),
#     path('logout/', views.General.logoutPage, name='logout'),
#     path('', views.General.general, name='general'),
#     path('standartnie_vicheti/', views.standartnie_vicheti, name='standartnie_vicheti'),
#     path('nlj/', views.nlj, name='nlj'),
#     path('minfin/', views.Minfin.minfin, name='minfin'),
#     path('minfin_eda/', views.Minfin.minfin_eda, name='minfin_eda'),
#     path('minfin_transport', views.Minfin.minfin_transport, name='minfin_transport'),
#     path('minfin_razvlechenia/', views.Minfin.minfin_razvlechenia, name='minfin_razvlechenia'),
#     path('minfin_ammortizatia/', views.Minfin.minfin_ammortizatia, name='minfin_ammortizatia'),
#     path('minfin_prochee/', views.Minfin.minfin_prochee, name='minfin_prochee'),
#     path('minfin_nds/', views.Minfin.minfin_nds, name='minfin_nds'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
