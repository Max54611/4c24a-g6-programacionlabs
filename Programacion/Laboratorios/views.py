from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib import messages

# Create your views here.

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'El nombre de usuario debe ser menor a 150 caracteres y no puede contener caracteres especiales'
        self.fields['password1'].help_text = 'La contraseña debe tener al menos 3 caracteres'
        self.fields['password2'].help_text = 'La contraseña debe tener al menos 3 caracteres'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Laboratorios:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'autenticacion/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('/listado')
    else:
        form = AuthenticationForm()
    return render(request, 'autenticacion/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

#PROGRAMACION LABORATORIOS

def index(request):
    listadoProgLabs = Programacion_laboratorio.objects.all()
    laboratorios = Laboratorio.objects.all()
    cursos_dictados = Curso_dictado.objects.all()
    context = {
        "labs": listadoProgLabs,
        "laboratorios": laboratorios,
        "cursos_dictados": cursos_dictados
    }
    return render(request, "index.html", context)

@login_required(login_url='Laboratorios:login')
def progLab(request):
    listadoProgLabs = Programacion_laboratorio.objects.all()
    laboratorios = Laboratorio.objects.all()
    cursos_dictados = Curso_dictado.objects.all()
    return render(request, "listado.html", {"labs": listadoProgLabs, "laboratorios": laboratorios, "cursos_dictados": cursos_dictados})

@login_required(login_url='Laboratorios:login')
def registrar(request):
    laboratorio_id = request.POST["txtlaboratorio"]
    curso_dictado_id = request.POST["txtcurso_dictado"]
    fecha = request.POST["txtfecha"]
    hora_inicio = request.POST["txthora_inicio"]
    hora_fin = request.POST["txthora_fin"]

    laboratorio = Laboratorio.objects.get(id=laboratorio_id)
    curso_dictado = Curso_dictado.objects.get(id=curso_dictado_id)

    if Programacion_laboratorio.objects.filter(
        Q(laboratorio=laboratorio) &
        (Q(fecha=fecha) & (Q(hora_inicio__range=(hora_inicio, hora_fin)) | Q(hora_fin__range=(hora_inicio, hora_fin))))).exists():
        messages.error(request, "Ya existe una programación para el laboratorio en el rango de fechas y horas especificado.")
    else:
        lab_programado = Programacion_laboratorio(
        laboratorio=laboratorio,
        curso_dictado=curso_dictado,
        fecha=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin)
        lab_programado.save()
        messages.success(request, "Programación de laboratorio registrada correctamente.")
    return redirect('/listado')

@login_required(login_url='Laboratorios:login')
def editar_datos(request,id):
    datos=Programacion_laboratorio.objects.get(id=id)

    codigo_lab=datos.laboratorio.id
    laboratorio=Laboratorio.objects.get(pk=codigo_lab)
    laboratorioListado=Laboratorio.objects.exclude(pk=codigo_lab)

    codigo_curso=datos.curso_dictado.id
    curso_dictado=Curso_dictado.objects.get(pk=codigo_curso)
    cursoListado=Curso_dictado.objects.exclude(pk=codigo_curso)
    
    listadoProgLabs = Programacion_laboratorio.objects.all()
    laboratorios = Laboratorio.objects.all()
    cursos_dictados = Curso_dictado.objects.all()

    context={
        'datos':datos,
        'laboratorio':laboratorio,
        'laboratorios':laboratorioListado,
        'curso_dictado':curso_dictado,
        'cursos':cursoListado,
        "labs": listadoProgLabs,
        "laboratorios": laboratorios,
        "cursos_dictados": cursos_dictados
    }
    return render(request,"editar.html",context)

@login_required(login_url='Laboratorios:login')
def editar(request):
    id=request.POST["idpro"]
    laboratorio_id=request.POST["txtlaboratorio"]
    curso_dictado_id = request.POST["txtcurso_dictado"]
    fecha = request.POST["txtfecha"]
    hora_inicio = request.POST["txthora_inicio"]
    hora_fin = request.POST["txthora_fin"]

    laboratorio = Laboratorio.objects.get(id=laboratorio_id)
    curso_dictado = Curso_dictado.objects.get(id=curso_dictado_id)

    if Programacion_laboratorio.objects.filter(
        Q(laboratorio=laboratorio) &
        (Q(fecha=fecha) & (Q(hora_inicio__range=(hora_inicio, hora_fin)) | Q(hora_fin__range=(hora_inicio, hora_fin))))).exclude(id=id).exists():
        messages.error(request, "Ya existe una programación para el laboratorio en el rango de fechas y horas especificado.")
    else:
        program = Programacion_laboratorio.objects.get(id=id)
        program.laboratorio = laboratorio
        program.curso_dictado = curso_dictado
        program.fecha = fecha
        program.hora_inicio = hora_inicio
        program.hora_fin = hora_fin
        program.save()
        messages.success(request, "Programación de laboratorio editada correctamente.")
    
    return redirect('/listado')

@login_required(login_url='Laboratorios:login')
def eliminar(request,id):
    program=Programacion_laboratorio.objects.get(id=id)
    program.delete()
    return redirect('/listado')