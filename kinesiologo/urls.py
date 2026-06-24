from django.urls import path
from . import views

urlpatterns = [
    # Login/Logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Pacientes
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/<int:paciente_id>/', views.detalle_paciente, name='detalle_paciente'),
    path('pacientes/<int:paciente_id>/editar/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/<int:paciente_id>/eliminar/', views.eliminar_paciente, name='eliminar_paciente'),
    
    # Rutinas
    path('rutinas/', views.lista_rutinas, name='lista_rutinas'),
    path('rutinas/crear/', views.crear_rutina, name='crear_rutina'),
    path('rutinas/<int:rutina_id>/', views.detalle_rutina, name='detalle_rutina'),
    path('rutinas/<int:rutina_id>/editar/', views.editar_rutina, name='editar_rutina'),
    path('rutinas/<int:rutina_id>/eliminar/', views.eliminar_rutina, name='eliminar_rutina'),
    
    # Seguimientos
    path('seguimientos/', views.lista_seguimientos, name='lista_seguimientos'),
    path('seguimientos/crear/', views.crear_seguimiento, name='crear_seguimiento'),
    path('seguimientos/<int:seguimiento_id>/', views.detalle_seguimiento, name='detalle_seguimiento'),
    path('seguimientos/<int:seguimiento_id>/editar/', views.editar_seguimiento, name='editar_seguimiento'),
    path('seguimientos/<int:seguimiento_id>/eliminar/', views.eliminar_seguimiento, name='eliminar_seguimiento'),
    
    # Acompañantes
    path('acompanantes/', views.lista_acompanantes, name='lista_acompanantes'),
    path('acompanantes/<int:paciente_id>/', views.detalle_acompanante, name='detalle_acompanante'),
]