from django.shortcuts import render, redirect
from django.contrib.auth import login
from Cliente.models import Cliente, Plan, TarjetaCredito, SitioWeb, Dominio, Ticket
from Cliente.validar_tarjeta import validar_tarjeta
from Empleado.models import Empleado
from Distribuidor.models import Distribuidor, ExtensionDominio
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Rol



# Create your views here.
def inicioSesion(request):
    if request.method == 'POST':
        username = request.POST['usuarioCliente']
        password = request.POST['contraseniaCliente']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            mensaje_advertencia = "Este usario no existe o la clave es erronea."
            return render(request, 'login.html', {'mensaje_advertencia': mensaje_advertencia})
    return render(request, 'login.html')


def ingresar(request):
    if request.user.is_authenticated:       
        return redirect('dashboard')
    else:
        return render(request, 'login.html')


def singout(request):
    logout(request)
    return redirect('home')


def eliminar_usuario(request):
    request.user.delete()
    return redirect('home')

@login_required
def dashboard_view(request):
    # Esta vista solo es accesible si el usuario ha iniciado sesión
    
    try:
        user = request.user
        rol = Rol.objects.get(usuario = user).rol
        
        if rol == "Cliente":
            cliente = Cliente.objects.get(usuario = user)
            tarjeta =  TarjetaCredito.objects.get(clienteId = cliente)
            sitios_web = SitioWeb.objects.filter(clienteId=cliente)
            dominios = Dominio.objects.filter(clienteId=cliente)
            tickets = Ticket.objects.filter(clienteId=cliente)
            tarjeta.save()
            return render(request, "cliente.html", {'cliente':cliente, 'tarjeta':tarjeta, 'sitios_web':sitios_web, 'dominios':dominios, "tickets":tickets})
        elif rol == "Distribuidor":
            #Lo que pasa cuando un distribuidor inicia sesión
            distribuidor = Distribuidor.objects.get(usuario = user)
            extensionesDistri = ExtensionDominio.objects.filter(distribuidorId = distribuidor)
            dominios_distr = Dominio.objects.filter(extensionDominio__in = extensionesDistri)
            return render(request, "distribuidor.html", {'distribuidor':distribuidor, 'extensiones':extensionesDistri, 'dominios':dominios_distr})
        elif rol == "Empleado":
            #Lo que pasa cuando un empleado inicia sesión
            empleado = Empleado.objects.get(usuario = user)
            tickets = Ticket.objects.filter(estado="sin resolver")
            return render(request, "empleado.html", {'empleado':empleado, "tickets":tickets})
    except:        
        if user.is_superuser:
            return HttpResponseRedirect("/admin")
        return redirect('error500')

def registro_clientes(request):

    if request.method == 'POST':
        if not Cliente.objects.filter(emailCliente = request.POST['email']).exists():
            if request.POST['pass'] == request.POST['Repass']:
                try:
                    user = User.objects.create_user(username = request.POST['user'], password=request.POST['pass'])
                    user.save()
                    login(request, user)
                except:
                    return render(request, 'login.html', {'mensaje_advertencia':"EL NOMBRE DE USUARIO REGISTRADO YA EXISTE. INTENTA CON OTRO"})

                nombre = request.POST['name']
                fecha_nac = request.POST['fecha']
                email = request.POST['email']
                pais = request.POST['countrySelect']
                ciudad = request.POST['citySelect']


                nuevoCliente = Cliente(usuario=user, nombreCliente=nombre, fechaNacimientoCliente=fecha_nac, emailCliente=email,
                                    paisCliente=pais, ciudadCliente=ciudad, ClienteActivo=False)

                nuevoCliente.save()

                tarjeta = TarjetaCredito(clienteId = nuevoCliente, numeroTarjeta = "0000000000000000", cvc = "000", direccion = "" )

                tarjeta.save()

                rol = Rol(usuario = user, rol="Cliente")

                rol.save()

                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'mensaje_advertencia':"LAS CONTRASEÑAS NO COINCIDEN"})
        else:
            return render(request, 'login.html', {'mensaje_advertencia':"Ya existe un usuario con este correo. Intenta recuperar tu contraseña"})
    else:
        return render(request, 'login.html')



def home(request):
    return render(request, "inicio.html")

def acercaDeNos(request):
    return render(request, "acercaDeNos.html")

def planes(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            cliente = Cliente.objects.get(usuario=user)
            valor_aceptado = cliente.planId
            tarjetaValida = validar_tarjeta(TarjetaCredito.objects.get(clienteId = Cliente.objects.get(usuario = request.user)).numeroTarjeta)
            print(tarjetaValida)
        except Cliente.DoesNotExist:
            tarjetaValida=False
            valor_aceptado = None
    else:
        # Si el usuario no está autenticado, establece el valor_aceptado en None
        tarjetaValida=False
        valor_aceptado = None

    return render(request, "planes.html",{'planes':Plan.objects.all()[:3] , 'valor_aceptado': valor_aceptado, 'tarjeta': tarjetaValida})

def error_500(request):
    return render(request, "error500.html")