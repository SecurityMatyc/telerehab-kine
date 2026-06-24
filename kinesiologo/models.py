from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Paciente(models.Model):
    """Modelo para pacientes"""
    # Datos personales
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    direccion = models.TextField(verbose_name="Dirección")
    comuna = models.CharField(max_length=100, verbose_name="Comuna")
    
    # Datos clínicos
    diagnostico = models.TextField(verbose_name="Diagnóstico")
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name="Fecha de ingreso")
    estado = models.CharField(
        max_length=20,
        choices=[
            ('activo', 'Activo'),
            ('inactivo', 'Inactivo'),
            ('completado', 'Completado'),
        ],
        default='activo',
        verbose_name="Estado"
    )
    
    # Acompañante
    tiene_acompanante = models.BooleanField(default=False, verbose_name="¿Tiene acompañante?")
    acompanante_nombre = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre del acompañante")
    acompanante_telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono del acompañante")
    acompanante_parentesco = models.CharField(max_length=50, blank=True, null=True, verbose_name="Parentesco")
    
    # Material entregado
    material_entregado = models.CharField(
        max_length=20,
        choices=[
            ('dvd', 'DVD'),
            ('pendrive', 'Pendrive'),
            ('ninguno', 'No entregado'),
        ],
        default='ninguno',
        verbose_name="Material entregado"
    )
    
    # Asignado al kinesiólogo
    kinesiologo = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Kinesiólogo asignado"
    )
    
    def __str__(self):
        return f"{self.nombre} - {self.rut}"
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['-fecha_ingreso']


class Rutina(models.Model):
    """Modelo para rutinas de rehabilitación"""
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='rutinas',
        verbose_name="Paciente"
    )
    titulo = models.CharField(max_length=200, verbose_name="Título de la rutina")
    descripcion = models.TextField(verbose_name="Descripción")
    ejercicios = models.TextField(verbose_name="Ejercicios (descripción detallada)")
    video_url = models.URLField(blank=True, null=True, verbose_name="URL del video")
    
    # Duración y frecuencia
    duracion_minutos = models.IntegerField(default=30, verbose_name="Duración (minutos)")
    frecuencia = models.CharField(
        max_length=50,
        choices=[
            ('diaria', 'Diaria'),
            ('lunes_miercoles_viernes', 'Lunes, Miércoles y Viernes'),
            ('martes_jueves', 'Martes y Jueves'),
            ('personalizada', 'Personalizada'),
        ],
        default='diaria',
        verbose_name="Frecuencia"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    estado = models.CharField(
        max_length=20,
        choices=[
            ('activa', 'Activa'),
            ('completada', 'Completada'),
            ('pausada', 'Pausada'),
        ],
        default='activa',
        verbose_name="Estado"
    )
    
    def __str__(self):
        return f"{self.titulo} - {self.paciente.nombre}"
    
    class Meta:
        verbose_name = "Rutina"
        verbose_name_plural = "Rutinas"
        ordering = ['-fecha_creacion']


class Seguimiento(models.Model):
    """Modelo para seguimiento de pacientes"""
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='seguimientos',
        verbose_name="Paciente"
    )
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha de seguimiento")
    cumple_ejercicios = models.BooleanField(default=False, verbose_name="¿Cumplió los ejercicios?")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    # Control realizado por
    tipo_control = models.CharField(
        max_length=20,
        choices=[
            ('presencial', 'Control presencial'),
            ('telefonico', 'Control telefónico'),
            ('whatsapp', 'Vía WhatsApp'),
            ('cartilla', 'Revisión de cartilla'),
        ],
        default='presencial',
        verbose_name="Tipo de control"
    )
    
    # Registro de acompañante
    acompanante_presente = models.BooleanField(default=False, verbose_name="¿Acompañante presente?")
    
    fecha_proximo_control = models.DateField(null=True, blank=True, verbose_name="Próximo control")
    
    kinesiologo = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Kinesiólogo que realizó el seguimiento"
    )
    
    def __str__(self):
        return f"Seguimiento - {self.paciente.nombre} - {self.fecha}"
    
    class Meta:
        verbose_name = "Seguimiento"
        verbose_name_plural = "Seguimientos"
        ordering = ['-fecha']


class Nota(models.Model):
    """Modelo para notas rápidas del kinesiólogo"""
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='notas',
        verbose_name="Paciente"
    )
    contenido = models.TextField(verbose_name="Contenido de la nota")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    es_urgente = models.BooleanField(default=False, verbose_name="¿Es urgente?")
    kinesiologo = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Kinesiólogo"
    )
    
    def __str__(self):
        return f"Nota - {self.paciente.nombre} - {self.fecha_creacion.strftime('%d/%m/%Y')}"
    
    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        ordering = ['-fecha_creacion']