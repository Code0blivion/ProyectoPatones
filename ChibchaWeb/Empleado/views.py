from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Empleado 
from Cliente.models import Ticket 
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.

def consulta_empleado(request):
    return render(request, "empleado.html")


@login_required
def editar_empleado(request, id_empleado):

    user = request.user
    if user.id == id_empleado:
        if request.method == 'POST':
            empleado = Empleado.objects.get(usuario_id = id_empleado)
            empleado.nombreEmpleado = request.POST['nombre']
            empleado.cargoEmpleado = request.POST['cargo']
            empleado.fechaNacimientoEmpleado = request.POST['fechaNacimiento']
            empleado.telefonoEmpleado = request.POST['telefono']
            empleado.inicioContrato = request.POST['inicioContrato']
            empleado.save()
            return redirect('dashboard')
    else:
        return redirect('home')
    return render(request, "editarEmpleado.html", {'empleado':Empleado.objects.get(usuario_id = id_empleado)})

def consultarTicketsEmp(request, ticket_id):
    ticket = Ticket.objects.get(ticketId=ticket_id)
    if request.method == "POST":
        estado = request.POST["ticket"]
        ticket.estado = estado
        ticket.save()
        return redirect("dashboard")
    else:
        return render(request, "consultarTickedEmpleado.html", {"ticket":ticket})
    