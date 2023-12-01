import xml.etree.ElementTree as ET
from Cliente.models import Dominio
import datetime

def generateRequest(request:dict):

    requestXML = ET.Element("request")

    head = ET.SubElement(requestXML,"head")
    ET.SubElement(head,"date").text = request['date']
    ET.SubElement(head, "time").text = request['time']
    ET.SubElement(head,"request_id").text = request['id']
    ET.SubElement(head, "distributor", id = request['distributor']['id']).text = request['distributor']['distributor']
    ET.SubElement(head,"language").text = request['language']
    ET.SubElement(head, "description").text = request['description']
    
    
    body = ET.SubElement(requestXML,"body")
    ET.SubElement(body,"domain", id = request['domain']['id']).text = request['domain']['domain']
    ET.SubElement(body,"extension", id = request['extension']['id']).text = request['extension']['extension']
    ET.SubElement(body,"client", id = request['client']['id']).text = request['client']['client']
    ET.SubElement(body,"price").text = request['price']
    ET.SubElement(body,"months").text = request['months']

    ET.indent(requestXML, space="  ")
    
    tree = ET.ElementTree(requestXML)

    print(tree)
    
    #tree.write("request"+request['id']+".xml", encoding='utf-8', xml_declaration=True)

    return ET.tostring(requestXML, encoding='utf-8').decode('utf-8')

def getRequest(domain):
    request = {}
    request['distributor'] = {'id':str(domain.extensionDominio.distribuidorId.pk),
    'distributor': domain.extensionDominio.distribuidorId.nombreDistribuidor}
    request['date'] = domain.fechaSolicitud.strftime("%d/%m/%Y")
    request['language'] = "es-CO"
    request['description'] = "DOMAIN REQUEST" 
    request['time'] = datetime.datetime.now().strftime("%H:%M:%S")
    request['id'] = str(domain.pk)
    request['domain'] = {'id':str(domain.pk), 'domain':domain.nombreDominio}
    request['extension'] = {'id':str(domain.extensionDominio.pk), 'extension':domain.extensionDominio.extensionDominio}
    request['client'] = {'id':str(domain.clienteId.pk), 'client':domain.clienteId.nombreCliente}
    request['price'] = str(domain.extensionDominio.precioExtension)
    request['months'] = str(domain.tiempoPropiedad)
    
    return request