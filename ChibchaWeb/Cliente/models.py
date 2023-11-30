from django.db import models
from django.contrib.auth.models import User
import datetime
from Distribuidor.models import ExtensionDominio

# Create your models here. Ciente

class Caracteristica(models.Model):
    caracteristicaId = models.AutoField(primary_key=True)
    caracteristica = models.TextField(verbose_name="caracteristica", blank=False)

    def __str__(self) -> str:
        return self.caracteristica

class Plan(models.Model):
    planId = models.AutoField(primary_key=True)
    nombrePlan = models.CharField(verbose_name="paquete", blank=True, max_length=20)
    tituloPlan = models.TextField(verbose_name="titulo", blank= False, null=True)
    #plataforma = models.CharField(verbose_name="plataforma", blank=True, max_length=15)
    descripcionPlan = models.TextField(verbose_name="descripcion", blank=False)
    caracteristicasPlan = models.ManyToManyField(Caracteristica)
    precioMensual = models.IntegerField(verbose_name="precio", blank=False)

    class Meta:
        ordering = ('nombrePlan',)

    def __str__(self) -> str:
        return self.nombrePlan

class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    clienteId = models.AutoField(primary_key=True)
    nombreCliente = models.CharField(verbose_name="nombre", max_length=20)
    fechaNacimientoCliente = models.DateField(verbose_name="Fecha de Nacimiento", blank=True, null=True)
    emailCliente = models.EmailField(verbose_name="emailCliente", max_length=30)
    paisCliente = models.CharField(verbose_name="paisCliente",blank=False, max_length=10)
    ciudadCliente = models.CharField(verbose_name="ciudadCliente", blank=False, max_length=15)
    planId = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    ClienteActivo = models.BooleanField(default=False) 
    last_login = models.DateTimeField(null=True, blank=True)
    is_authenticated = models.BooleanField(default=False)

    def is_authenticated(self):
        return self.is_authenticated
    class Meta:
        ordering = ('nombreCliente',)
        

    def __str__(self) -> str:
        return self.nombreCliente


class TarjetaCredito(models.Model):
    tarjetaId = models.AutoField(primary_key=True)
    clienteId = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numeroTarjeta = models.CharField(blank=False,verbose_name="tarjeta numero",max_length=18)
    cvc = models.CharField(blank=False, max_length=3)
    fechaVencimientoMes = models.IntegerField(verbose_name="Fecha mes", blank=True, null=True)
    fechaVencimientoAnio = models.IntegerField(verbose_name="Fecha anio", blank=True, null=True)
    direccion = models.CharField(blank=False, verbose_name = "direccion", max_length=50, null=True)

    def __str__(self) -> str:
        return self.clienteId.nombreCliente


class Dominio(models.Model):
    dominioId = models.AutoField(primary_key=True)
    clienteId = models.ForeignKey(Cliente,on_delete=models.CASCADE, null=True)
    estado = models.CharField(blank=False, verbose_name="estadoDominio",max_length=15, default="Sin usar")
    nombreDominio = models.CharField(blank=False,verbose_name="nombreDominio",max_length=100)
    extensionDominio = models.ForeignKey(ExtensionDominio, on_delete=models.CASCADE)
    tiempoPropiedad = models.IntegerField(verbose_name="tiempoPropiedad", blank=False, null=True)
    fechaSolicitud = models.DateField(verbose_name="fechaSolicitud",null=True, blank=True, max_length=10)
    
    class Meta:
        ordering = ('nombreDominio',)

    def __str__(self) -> str:
        return self.nombreDominio + self.extensionDominio.extensionDominio

class DominioCancelado(models.Model):
    dominioId = models.AutoField(primary_key=True)
    clienteId = models.ForeignKey(Cliente,on_delete=models.CASCADE, null=True)
    nombreDominio = models.CharField(blank=False,verbose_name="nombreDominio",max_length=100)
    extensionDominio = models.ForeignKey(ExtensionDominio, on_delete=models.CASCADE)
    fechaSolicitud = models.DateField(verbose_name="fechaSolicitud",null=True, blank=True, max_length=10)
    fechaCancelacion = models.DateField(verbose_name="fechaCancelación", null=True, blank=True, max_length=10)

    class Meta:
        ordering = ('nombreDominio',)

    def __str__(self) -> str:
        return self.nombreDominio + self.extensionDominio.extensionDominio

class SitioWeb(models.Model):
    webId = models.AutoField(primary_key=True)
    clienteId = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    dominio = models.ForeignKey(Dominio, on_delete=models.CASCADE, null=True)
    fechaSolicitud = models.DateField(verbose_name="Fecha desolicitud",null=True, blank=True, max_length=10)

    def __str__(self) -> str:
        return self.dominio.nombreDominio + self.dominio.extensionDominio.extensionDominio

class Ticket(models.Model):
    ticketId = models.AutoField(primary_key=True)
    clienteId = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descripcion = models.TextField(verbose_name="Descripcion", blank=True, max_length=100)
    estado = models.CharField(null=True, max_length=20)
    titulo = models.CharField(max_length=100, null =True)


class Archivo(models.Model):
    archivoId= models.AutoField(primary_key=True)
    clienteId = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    sitioId = models.ForeignKey(SitioWeb,on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='archivos/')






    




