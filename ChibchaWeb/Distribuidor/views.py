from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from Cliente.models import Cliente, Dominio, DominioCancelado
from .models import Distribuidor, ExtensionDominio
from .BancaryReportFacade import BancaryReportFacade
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .ReportAdapter import ReportAdapter
from Distribuidor.XMLGenerator import getRequest, generateRequest

# Create your views here.
@login_required
def editar_distribuidor(request, id_distribuidor):
    
    user = request.user
    if user.id == id_distribuidor:
        if request.method == 'POST':
            
            distr = Distribuidor.objects.get(usuario_id = id_distribuidor)
            distr.nombreDistribuidor = request.POST['nombre']
            distr.categoria = request.POST['categoria']
            if request.POST['categoria'] == "basico":
                distr.comision = 15
            else:
                distr.comision = 20
                
            distr.save()
            return redirect('dashboard')
    else:
        return redirect('home')
    return render(request, "editarDistribuidor.html", {'distribuidor':Distribuidor.objects.get(usuario_id = id_distribuidor)})


def descargarReporte(request):
    generador = BancaryReportFacade()
    distribuidor = Distribuidor.objects.get(usuario=request.user)  
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
    generador.generatePDF(response, distribuidor.nombreDistribuidor,ReportAdapter.getListData(distribuidor))

    return response

def reporteContrato(request, dist):
    
    extensiones_dist = ExtensionDominio.objects.filter(distribuidorId_id=dist)
    
    dominios_dist = Dominio.objects.filter(extensionDominio__in=extensiones_dist)
    
    clientes_con_dominios_dist = Cliente.objects.filter(dominio__in=dominios_dist).distinct()

    dominios_can_dis = DominioCancelado.objects.filter(extensionDominio__in=extensiones_dist)

    datos_clientes = []
    # Iterar sobre los clientes
    for cliente in clientes_con_dominios_dist:
        # Obtener los dominios asociados a cada cliente
        dominios_cliente = Dominio.objects.filter(clienteId_id=cliente,extensionDominio__in=extensiones_dist )

        # Almacenar los datos en un diccionario
        datos_cliente = {
            'cliente': cliente,
            'dominio': dominios_cliente
        }

        # Agregar el diccionario a la lista
        datos_clientes.append(datos_cliente)

    for dato_cliente in datos_clientes:
        for dominio in dato_cliente['dominio']:
            extension_dominio_id = dominio.extensionDominio_id
            distribuidor_extensiondominio = ExtensionDominio.objects.filter(extensionId=extension_dominio_id).first()
            dominio.distribuidor_extensiondominio = distribuidor_extensiondominio
    # Pasar la lista de datos_clientes a la plantilla


    return render(request, "repContratos.html", {'distribuidor':Distribuidor.objects.get(distribuidorId = dist), 'datos_clientes': datos_clientes, 'dominiosCan':dominios_can_dis})


@login_required
def registroExtension(request):

    flag = False
    if request.method == 'POST':
        distribuidor = Distribuidor.objects.get(usuario=request.user)
        if not ExtensionDominio.objects.filter(extensionDominio = request.POST['nombreExtension']).exists():
            extension = ExtensionDominio(distribuidorId = distribuidor, extensionDominio=request.POST['nombreExtension'],
                                        precioExtension=request.POST['precio'])
            extension.save()
        else:
            flag = True
        
        extensionesDistri = ExtensionDominio.objects.filter(distribuidorId = distribuidor)
        dominios_distr = Dominio.objects.filter(extensionDominio__in = extensionesDistri)
        return render(request, "distribuidor.html", {'distribuidor':distribuidor, 'extensiones':extensionesDistri, 'dominios':dominios_distr, 'flag':flag})

@login_required
def vmodificarExtension(request, ext):
   
    return render(request, "modificarDominioDistribuidor.html", {'ext':ExtensionDominio.objects.get(extensionId = ext)})

@login_required
@csrf_exempt
def modificarPrecioExtension(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        nuevo_precio = data.get('precio')
        extension_id = data.get('id')
        
        
        exte = ExtensionDominio.objects.get(extensionId = int(extension_id))
        exte.precioExtension = float(nuevo_precio)
        exte.save()
        # Devolver una respuesta JSON
        return JsonResponse({'success': True})
    else:
        # Manejar otros métodos HTTP según sea necesario
        # ...
        None


def solicitudXML(request, dominioId):
    dominio = Dominio.objects.get(dominioId = dominioId)
    req = getRequest(dominio)
    return render(request, 'Solicitudes.html',{'dominio':dominio, 'texto':generateRequest(req)})
