from .models import Distribuidor, ExtensionDominio
from Cliente.models import Cliente, TarjetaCredito, Dominio
import locale

class ReportDataGenerator:
    
    @classmethod
    def getDictData(cls, distribuidor):
        locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
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
                            'valorCon':locale.currency(dominio.extensionDominio.precioExtension, grouping=True),
                            'comision':locale.currency((distribuidor.comision/100)*dominio.extensionDominio.precioExtension, grouping=True),
                            'tarjeta':tarjeta.numeroTarjeta}) 
                
                total += dominio.extensionDominio.precioExtension
                total_comision += (distribuidor.comision/100)*dominio.extensionDominio.precioExtension
                
            data.append(locale.currency(total, grouping=True))
            data.append(locale.currency(total_comision, grouping=True))
            data.append(locale.currency(total-total_comision, grouping=True))
        
        return data