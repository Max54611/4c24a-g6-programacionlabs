from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.db import IntegrityError
from django.contrib import messages

# Create your views here.



#PROGRAMACION LABORATORIOS
def progLab(request):
    listadoProgLabs = Programacion_laboratorio.objects.all()
    laboratorios = Laboratorio.objects.all()
    cursos_dictados = Curso_dictado.objects.all()
    return render(request, "listado.html", {"labs": listadoProgLabs, "laboratorios": laboratorios, "cursos_dictados": cursos_dictados})

#No se permite registrar un laboratorio en una fecha y hora que ya se encuentre registrado o en el mismo rango de horas
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

def eliminar(request,id):
    program=Programacion_laboratorio.objects.get(id=id)
    program.delete()
    return redirect('/listado')
