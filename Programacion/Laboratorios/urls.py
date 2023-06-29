from django.urls import path
from .import views

urlpatterns = [

    path('listado',views.progLab, name='labs'),
    path('registrar',views.registrar),
    path('editar/<id>',views.editar_datos),
    path('editar',views.editar),
    path('eliminar/<id>',views.eliminar)
]