from django.urls import path
from .views import editar_empleado, consultarTicketsEmp
from Home.views import eliminar_usuario 

urlpatterns = [
    #path("", consulta_clientes, name='consultaClientes'),
    #path("prueba", consulta_empleado, name='consultaCliente'),
    #path("<int:id_empleado>/delete", eliminar_usuario, name='eliminar'),
    path("<int:id_empleado>/modificar", editar_empleado, name='editarEmpleado'),
    path("consultarTicketEmp/<int:ticket_id>",consultarTicketsEmp, name="consultarTicketsEmp")
]