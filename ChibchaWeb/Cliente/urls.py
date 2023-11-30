from django.urls import path
from .views import consulta_cliente, consulta_clientes, editar_cliente, cambiar_tarjeta, registrarDominio,agregarPlan, subirArchivo,modificarPaginaWeb,actualizarDominio ,dominiosDisponibles, agregarPagina,  registrarPaginaWeb, registrarPaginaWebArchivo, dominiosDisponiblesSinRegistro, modificarDominio, cancelarDominio, crearTicket, vistaTicket

urlpatterns = [
    #path("", consulta_clientes, name='consultaClientes'),
    #path("prueba", consulta_cliente, name='consultaCliente'),
    #path("<int:id_cliente>/delete", eliminar_cliente, name='eliminarCliente'),
    path("<int:id_cliente>/modificar", editar_cliente, name='editarCliente'),
    path("medioPago",cambiar_tarjeta, name = 'cambiarTarjeta'),
    path("crearTicket",crearTicket, name = 'crearTicket'),
    path("registrarDominio", registrarDominio, name='registrarDominio'),
    path("dominiosDisponibles/<str:dominio>/<int:flag>", dominiosDisponibles, name='dominiosDisponibles'),
    path("<int:id_cliente>/registrarPagina", agregarPagina, name='registrarPagina'),
    path('crear_sitio_web/', registrarPaginaWeb, name='crear_sitio_web'),
    path('crear_sitio_web_a/', registrarPaginaWebArchivo, name='crear_sitio_web_a'),
    path("modificar/<int:webId>", modificarPaginaWeb, name='modificarPagina'),
    path("modificarD/<int:dominioId>", modificarDominio, name='modificarDominio'),
    path("cancelarD/<int:dominioId>", cancelarDominio, name='cancelar_dominio'),
    path("modificar/archivo", subirArchivo, name='subirArchivo'),
    path("consultarDominio/<str:dominio>", dominiosDisponiblesSinRegistro, name="dominioSinRegistro"),
    path('agregarPlan', agregarPlan, name='agregarPlan'),
    path('actuDominio', actualizarDominio, name='actuDominio'),
    path("consultaticket/<int:ticket_id>",vistaTicket, name="consultaTicketCli" ),
    #path('dashboard', dashboard_view, name='dashboard'),
]