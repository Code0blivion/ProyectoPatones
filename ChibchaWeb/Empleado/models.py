from django.db import models
from django.contrib.auth.models import User
# Create your models here.Empleado

class Empleado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)   
    id = models.AutoField(primary_key=True)
    nombreEmpleado = models.CharField(verbose_name="nombre", max_length=20)
    fechaNacimientoEmpleado = models.DateField(verbose_name="Fecha de Nacimiento", blank=True, null=True)
    cargoEmpleado = models.CharField(verbose_name="cargoEmpleado", blank=False,max_length=15 )
    inicioContrato = models.DateField(verbose_name="Inicio de contrato", blank=True, null=True)
    telefonoEmpleado = models.CharField(blank=False, max_length=20)
    emailEmpleado = models.CharField(verbose_name="emailEmpleado", max_length=30)
    
    class Meta:
        ordering = ('nombreEmpleado',)

    def __str__(self) -> str:
        return self.nombreEmpleado
