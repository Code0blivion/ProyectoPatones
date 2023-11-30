from datetime import date
import json
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Archivo, Cliente, TarjetaCredito, Dominio, SitioWeb, Plan, DominioCancelado, Ticket
from Distribuidor.models import Distribuidor, ExtensionDominio
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from random import random
from django.contrib import messages
from datetime import datetime, timedelta
from .validar_tarjeta import validar_tarjeta

# Create your views here.

def consulta_clientes(request):
    template = loader.get_template('CRUD.html')

    context = {
        "clientes": Cliente.objects.all(),
    }

    return HttpResponse(template.render(context, request))


def consulta_cliente(request):
    return render(request, "cliente.html")



@login_required
def editar_cliente(request, id_cliente):
    
    user = request.user
    if user.id == id_cliente:
        if request.method == 'POST':
            
            user.username = request.POST['nuevoUsuario']
            user.save()
            cliente = Cliente.objects.get(usuario_id = id_cliente)
            cliente.nombreCliente = request.POST['nuevoNombre']
            cliente.fechaNacimientoCliente = request.POST['nuevaFechaNacimiento']
            cliente.emailCliente = request.POST['nuevoEmail']
            cliente.paisCliente = request.POST['nuevoPais']
            cliente.ciudadCliente = request.POST['nuevaCiudad']
            cliente.save()
            return redirect('dashboard')
    else:
        return redirect('home')
    return render(request, "editarCliente.html", {'cliente':Cliente.objects.get(usuario_id = id_cliente)})


def cambiar_tarjeta(request):
    user = request.user

    cliente = Cliente.objects.get(usuario = user)
    tarjeta = TarjetaCredito.objects.get(clienteId = cliente)
    if request.method == 'POST':
        tarjeta = TarjetaCredito.objects.get(clienteId = cliente)
        tarjeta.numeroTarjeta = request.POST['numeroTarjeta']
        tarjeta.cvc = request.POST['cvc']
        tarjeta.fechaVencimientoMes = request.POST['mes']
        tarjeta.fechaVencimientoAnio = request.POST['anio']
        tarjeta.direccion = request.POST['direccion']
        if validar_tarjeta(tarjeta.numeroTarjeta) == True and tarjeta.numeroTarjeta.count('0') != len(tarjeta.numeroTarjeta):
            tarjeta.save()
            print("Tarjeta guardada")
            messages.success(request, 'La tarjeta de crédito se ha guardado correctamente.')
        else: 
            print('tarjeta no guardada')
            messages.success(request, 'Número de la tarjeta de credito no valido')
        return redirect('dashboard')
        
    else:
        return render(request, 'tarjeta.html',{'tarjeta':tarjeta, 'cliente':cliente})


@csrf_exempt
def registrarDominio(request):

    flag = 0
    if request.method == 'POST':
        extensionDominio = ExtensionDominio.objects.get(extensionDominio = request.POST['extension'])
        if not Dominio.objects.filter(nombreDominio = request.POST['nombreDominio'], extensionDominio = extensionDominio).exists():
            user = request.user
            cliente = Cliente.objects.get(usuario = user) 
            dominio = Dominio(clienteId = cliente, nombreDominio = request.POST['nombreDominio'],
                            extensionDominio = extensionDominio, fechaSolicitud = date.today(), tiempoPropiedad=request.POST['meses'])            
            dominio.save()       
        else:
            flag = 1

        return JsonResponse({'dominio':request.POST['nombreDominio'], 'flag': flag})
    
    else:
        return render(request, 'dominio.html')


@login_required   
def agregarPagina(request, id_cliente):

    user = request.user
    if user.id == id_cliente:
        cliente = Cliente.objects.get(usuario_id = id_cliente)
        id_C= cliente.clienteId
        dominios = Dominio.objects.filter(clienteId_id=id_C, estado='Sin usar')
        plan = cliente.planId
    else:
        return redirect('home')
    
    return render(request, "registroPaginaWeb.html", {'cliente':Cliente.objects.get(usuario_id = id_cliente), 'dominios_disponibles': dominios, 'plan': plan})

@csrf_exempt
def registrarPaginaWeb(request):
    if request.method == 'POST':
        user = request.user
        cliente = Cliente.objects.get(usuario=user)
        data = json.loads(request.body)
        dominio = data.get('dominio')
        dom=Dominio.objects.get(dominioId = dominio)
        sitio = SitioWeb(clienteId=cliente, dominio=dom, fechaSolicitud=date.today())
        #actualiza el estado del dominio
        sitio.save()  # Guardar el objeto SitioWeb en la base de datos
        dom.estado='En uso'
        dom.save()
        return JsonResponse({'redirect': '/dashboard'})  # Redirigir a la página de dashboard después de guardar
    else:
        return redirect('home')
   
@csrf_exempt
def registrarPaginaWebArchivo(request):
    if request.method == 'POST':
        user = request.user
        cliente = Cliente.objects.get(usuario=user)
        dominio = request.POST.get('dominio')
        dom=Dominio.objects.get(dominioId = dominio)

        #fechaH = fecha_hoy + timedelta(days=30)
        sitio = SitioWeb(clienteId=cliente, dominio=dom, fechaSolicitud=date.today())
        sitio.save()  # Guardar el objeto SitioWeb en la base de datos
        #-----------------------
        print("----")
        
        for key, file in request.FILES.items():
            nuevo_archivo = Archivo(clienteId=cliente, sitioId=sitio, archivo=file)
            nuevo_archivo.save()



        return JsonResponse({'redirect': '/dashboard'})  # Redirigir a la página de dashboard después de guardar
    else:
        return redirect('home')

@login_required  
def modificarPaginaWeb(request, webId):
    user = request.user
    cliente = Cliente.objects.get(usuario_id = user.id)
    id_C= cliente.clienteId
    dominios = Dominio.objects.filter(clienteId_id=id_C, estado='Sin usar')

    archivo= Archivo.objects.filter(sitioId_id=webId)
    sitio = SitioWeb.objects.get(webId = webId)
    
    dominio = Dominio.objects.filter(dominioId= sitio.dominio.dominioId).first()
    print(dominio.estado)
    return render(request, "modificarPaginaWeb.html", {'sitio':SitioWeb.objects.get(webId = webId), 'archivos': archivo, 'titulo':dominio, 'dominios':dominios})

@login_required  
def modificarDominio(request, dominioId):
    return render(request, "modificarDominio.html", {'dominio':Dominio.objects.get(dominioId = dominioId),
                                                      'distribuidor':Distribuidor.objects.get(distribuidorId = Dominio.objects.get(dominioId = dominioId).extensionDominio.distribuidorId.pk)})

@login_required  
def cancelarDominio(request, dominioId):
    dominio = Dominio.objects.get(dominioId = dominioId)
    dom_canc = DominioCancelado(clienteId = dominio.clienteId, nombreDominio = dominio.nombreDominio, extensionDominio = dominio.extensionDominio,
                                fechaSolicitud = dominio.fechaSolicitud, fechaCancelacion = date.today())
    dom_canc.save()
    dominio.delete()
    return redirect('dashboard')

@csrf_exempt
def subirArchivo(request):
    if request.method == 'POST':
        user = request.user
        cliente = Cliente.objects.get(usuario=user)
        sitio_id = request.POST.get('sitio') 
        sitio= SitioWeb.objects.get(webId=sitio_id)
        #-----------------------
        print("----")
        
        for key in request.FILES.keys():
            file = request.FILES[key]  # Obtener cada archivo individualmente
            
            nuevo_archivo = Archivo(clienteId=cliente, sitioId=sitio, archivo=file)
            nuevo_archivo.save()



        return JsonResponse({'success': True}) # Redirigir a la página de dashboard después de guardar
    else:
        return redirect('home')

@csrf_exempt  
def actualizarDominio(request):
    if request.method == 'POST':
        user = request.user
        cliente = Cliente.objects.get(usuario=user)

        dominioV = request.POST.get('dominioViejo') 
        dominioN= request.POST.get('dominioNuevo') 
        sitio = request.POST.get('sitio')
        #-----------------------
        print("----")
        domV=Dominio.objects.get(dominioId = dominioV)
        domV.estado = "Sin usar"
        domV.save()
        domN=Dominio.objects.get(dominioId = dominioN)
        domN.estado ="En uso"
        domN.save()

        st= SitioWeb.objects.get(webId=sitio)
        st.dominio = domN
        st.save()



        return JsonResponse({'success': True}) # Redirigir a la página de dashboard después de guardar
    else:
        return redirect('home')

@login_required
def dominiosDisponibles(request, dominio, flag):
    extensiones = ExtensionDominio.objects.all()

    data = []
    populares = []
    for extension in extensiones:
        try:
            Dominio.objects.get(extensionDominio=extension, nombreDominio=dominio)
            data.append((extension,True))
        except:
            data.append((extension,False))
            populares.append(extension)
    # Meter validacion de tarjeta aca
    tarjetaValida = validar_tarjeta(TarjetaCredito.objects.get(clienteId = Cliente.objects.get(usuario = request.user)).numeroTarjeta)
    print(tarjetaValida)
    return render(request,'dominio.html',{'data':data, 'dominioObj':dominio, 'populares':populares, 'flag':flag, 'tarjeta':tarjetaValida})


def dominiosDisponiblesSinRegistro(request, dominio):
    extensiones = ExtensionDominio.objects.all()
    data = []
    for extension in extensiones:
        try:
            Dominio.objects.get(extensionDominio=extension, nombreDominio=dominio)
            data.append((extension,True))
        except:
            data.append((extension,False))

    return render(request,'dominioSin.html',{'data':data, 'dominioObj':dominio})

@csrf_exempt
def agregarPlan(request):
    if request.method == 'POST':
        user = request.user
        cliente = Cliente.objects.get(usuario=user)
        data = json.loads(request.body)
        id = data.get('id', None)
        plan = Plan.objects.get(planId= id)
        cliente.planId = plan
        cliente.save()
        
        return JsonResponse({'redirect': '/dashboard'})  # Redirigir a la página de dashboard después de guardar
    else:
        return redirect('home')



def crearTicket(request):
    
    if request.method == 'POST':
            cliente = Cliente.objects.get(usuario=request.user)
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            ticket = Ticket(titulo=titulo, descripcion=descripcion, clienteId=cliente)  
            ticket.estado = "sin resolver"
            ticket.save()
            print(ticket)
            return redirect("dashboard")
    else:
        return render(request, "registrarTicket.html")
    

def vistaTicket(request, ticket_id):
    ticket = Ticket.objects.get(ticketId=ticket_id)
    return render(request, "consultarTicketCliente.html" ,{"Ticket":ticket})