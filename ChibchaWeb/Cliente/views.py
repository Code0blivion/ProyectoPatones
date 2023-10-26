from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Cliente
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import django.http.multipartparser
from django.contrib.auth.decorators import login_required
# Create your views here.

def consulta_clientes(request):
    template = loader.get_template('CRUD.html')

    context = {
        "clientes" : Cliente.objects.all(),
    }

    return HttpResponse(template.render(context, request))

def consulta_cliente(request):
    return render(request, "cliente.html")

def inicioSesion(request):
    
    if request.method == 'POST':
        username = request.POST['usuarioCliente']
        password = request.POST['contraseniaCliente']
        
        user = authenticate(username=username,password=password)
        print(user)
        if user is not None:
            login(request, user)
            return render(request,"cliente.html")
        else:
            return render(request,'login.html')
            
        

def ingresar(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
       return render(request, 'login.html')
        
@login_required
def dashboard_view(request):
    # Esta vista solo es accesible si el usuario ha iniciado sesión
    return render(request, "cliente.html")

def registro_clientes(request):

    if request.method == 'POST':
      
      nombre = request.POST['name']
      contras = request.POST['pass']
      fecha_nac = request.POST['fecha']
      email = request.POST['email']
      pais = request.POST['countrySelect']
      ciudad = request.POST['citySelect']
      username = request.POST['user']  
      plan = request.POST['plan']

      nuevoCliente = Cliente(nombreCliente=nombre, fechaNacimientoCliente = fecha_nac, emailCliente = email,
                             paisCliente = pais, ciudadCliente = ciudad, usuarioCliente = username, planCliente = plan, 
                             ClienteActivo = False, contraseniaCliente = contras)
      
      nuevoCliente.save()

      return render(request,'index.html')

    else:
        return render(request,'login.html')


def eliminar_clientes(request, ids_clientes):
    pass


def eliminar_cliente(request, id_cliente):

    if request.method == "POST" and request.is_ajax():
    
        Cliente.objects.filter(id=id_cliente).delete()

        
    return HttpResponseRedirect('/clientes/registro')