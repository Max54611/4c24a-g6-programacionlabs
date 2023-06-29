from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q

# Create your views here.



#PROGRAMACION LABORATORIOS
def progLab(request):
    listadoProgLabs = Programacion_laboratorio.objects.all()
    laboratorios = Laboratorio.objects.all()
    cursos_dictados = Curso_dictado.objects.all()
    return render(request, "listado.html", {"labs": listadoProgLabs, "laboratorios": laboratorios, "cursos_dictados": cursos_dictados})

def registrar(request):
    laboratorio_id = request.POST["txtlaboratorio"]
    curso_dictado_id = request.POST["txtcurso_dictado"]
    fecha = request.POST["txtfecha"]
    hora_inicio = request.POST["txthora_inicio"]
    hora_fin = request.POST["txthora_fin"]

    laboratorio = Laboratorio.objects.get(id=laboratorio_id)
    curso_dictado = Curso_dictado.objects.get(id=curso_dictado_id)

    lab_programado = Programacion_laboratorio.objects.create(laboratorio=laboratorio, curso_dictado=curso_dictado, fecha=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin)
    return redirect('/listado')

def editar_datos(request,id):
    datos=Programacion_laboratorio.objects.get(id=id)

    codigo_lab=datos.laboratorio.id
    laboratorio=Laboratorio.objects.get(pk=codigo_lab)
    laboratorioListado=Laboratorio.objects.exclude(pk=codigo_lab)

    codigo_curso=datos.curso_dictado.id
    curso_dictado=Curso_dictado.objects.get(pk=codigo_curso)
    cursoListado=Curso_dictado.objects.exclude(pk=codigo_curso)

    context={
        'datos':datos,
        'laboratorio':laboratorio,
        'laboratorios':laboratorioListado,

        'curso_dictado':curso_dictado,
        'cursos':cursoListado
    }
    return render(request,"editar.html",context)

def editar(request):
    id=request.POST["idpro"]
    laboratorio_id=request.POST["txtlaboratorio"]
    curso_dictado_id = request.POST["txtcurso_dictado"]
    fecha = request.POST["txtfecha"]
    hora_inicio = request.POST["txthora_inicio"]
    hora_fin = request.POST["txthora_fin"]

    laboratorio = Laboratorio.objects.get(id=laboratorio_id)
    curso_dictado = Curso_dictado.objects.get(id=curso_dictado_id)

    lab_programado = Programacion_laboratorio.objects.filter(id=id).update(laboratorio=laboratorio, curso_dictado=curso_dictado, fecha=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin)
    return redirect('/listado')

def eliminar(request,id):
    program=Programacion_laboratorio.objects.get(id=id)
    program.delete()
    return redirect('/listado')






