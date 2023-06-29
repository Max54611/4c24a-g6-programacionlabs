from django.urls import path
from .import views

urlpatterns = [

    path('listado',views.progLab, name='labs'),
    path('registrar',views.registrar),


]