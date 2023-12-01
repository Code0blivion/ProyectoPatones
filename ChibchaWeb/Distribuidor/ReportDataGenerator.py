from .models import Distribuidor, ExtensionDominio
from Cliente.models import Cliente, TarjetaCredito, Dominio

class ReportDataGenerator:
    
    @classmethod
    def getDictData(cls, distribuidor):
        dominiosDistribuidor = []
        extensionesDistribuidor = ExtensionDominio.objects.filter(distribuidorId = distribuidor)
        data = []

        if extensionesDistribuidor:
            for dominio in Dominio.objects.all():
                try:
                    if dominio.extensionDominio in extensionesDistribuidor:
                        dominiosDistribuidor.append(dominio)
                except:
                    pass

            total = 0
            total_comision = 0
            for dominio in dominiosDistribuidor:
                tarjeta = TarjetaCredito.objects.get(clienteId = dominio.clienteId)
                data.append({'nombreDom':dominio.nombreDominio,
                            'extension':dominio.extensionDominio.extensionDominio,
                            'nombreCli':dominio.clienteId.nombreCliente,
                            'fechaReg':dominio.fechaSolicitud,
                            'valorCon':str(dominio.extensionDominio.precioExtension),
                            'comision':str((distribuidor.comision/100)*dominio.extensionDominio.precioExtension),
                            'tarjeta':tarjeta.numeroTarjeta}) 
                
                total += dominio.extensionDominio.precioExtension
                total_comision += (distribuidor.comision/100)*dominio.extensionDominio.precioExtension
                
            data.append(str(total))
            data.append(str(total_comision))
            data.append(str(total-total_comision))
        
        return data