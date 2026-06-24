from datetime import date, datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from .models import Paciente, Rutina, Seguimiento, Nota


# ==========================================
# ===== LOGIN / LOGOUT =====
# ==========================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        error = 'Usuario o contraseña incorrectos.'

    return render(request, 'kinesiologo/login.html', {'error': error})


def logout_view(request):
    auth_logout(request)
    return redirect('login')


# ==========================================
# ===== FUNCIÓN PARA CONVERTIR FECHAS =====
# ==========================================

def convertir_fecha(fecha_str):
    """Convierte una fecha en formato DD/MM/YYYY o YYYY-MM-DD a formato YYYY-MM-DD para Django"""
    if not fecha_str:
        return None
    
    # Si ya viene en formato YYYY-MM-DD, devolverla tal cual
    if '-' in fecha_str and len(fecha_str) == 10:
        try:
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return fecha_str
        except ValueError:
            pass
    
    # Intentar convertir desde formato DD/MM/YYYY
    if '/' in fecha_str:
        try:
            fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y')
            return fecha_obj.strftime('%Y-%m-%d')
        except ValueError:
            pass
    
    # Intentar convertir desde formato YYYY-MM-DD
    try:
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
        return fecha_obj.strftime('%Y-%m-%d')
    except ValueError:
        pass
    
    # Si todo falla, intentar con otros formatos comunes
    formatos = ['%d-%m-%Y', '%Y/%m/%d', '%d.%m.%Y']
    for fmt in formatos:
        try:
            fecha_obj = datetime.strptime(fecha_str, fmt)
            return fecha_obj.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    return None


# ==========================================
# ===== DASHBOARD =====
# ==========================================

@login_required(login_url='login')
def dashboard(request):
    """Vista principal del dashboard con estadísticas"""
    total_pacientes = Paciente.objects.filter(kinesiologo=request.user).count()
    pacientes_activos = Paciente.objects.filter(kinesiologo=request.user, estado='activo').count()
    rutinas_activas = Rutina.objects.filter(estado='activa').count()
    seguimientos_hoy = Seguimiento.objects.filter(fecha=date.today()).count()
    
    ultimos_pacientes = Paciente.objects.filter(kinesiologo=request.user).order_by('-fecha_ingreso')[:5]
    
    proximos_controles = Seguimiento.objects.filter(
        fecha_proximo_control__gte=date.today()
    ).order_by('fecha_proximo_control')[:5]
    
    context = {
        'total_pacientes': total_pacientes,
        'pacientes_activos': pacientes_activos,
        'rutinas_activas': rutinas_activas,
        'seguimientos_hoy': seguimientos_hoy,
        'ultimos_pacientes': ultimos_pacientes,
        'proximos_controles': proximos_controles,
    }
    return render(request, 'kinesiologo/dashboard.html', context)


# ==========================================
# ===== PACIENTES =====
# ==========================================

@login_required(login_url='login')
def lista_pacientes(request):
    """Lista de todos los pacientes del kinesiólogo"""
    pacientes = Paciente.objects.filter(kinesiologo=request.user)
    busqueda = request.GET.get('busqueda', '')
    
    if busqueda:
        pacientes = pacientes.filter(
            Q(nombre__icontains=busqueda) | 
            Q(rut__icontains=busqueda) |
            Q(diagnostico__icontains=busqueda)
        )
    
    context = {
        'pacientes': pacientes,
        'busqueda': busqueda,
    }
    return render(request, 'kinesiologo/pacientes/lista.html', context)


@login_required(login_url='login')
def detalle_paciente(request, paciente_id):
    """Ver detalle de un paciente"""
    paciente = get_object_or_404(Paciente, id=paciente_id, kinesiologo=request.user)
    rutinas = paciente.rutinas.all().order_by('-fecha_creacion')
    seguimientos = paciente.seguimientos.all().order_by('-fecha')
    notas = paciente.notas.all().order_by('-fecha_creacion')
    
    context = {
        'paciente': paciente,
        'rutinas': rutinas,
        'seguimientos': seguimientos,
        'notas': notas,
    }
    return render(request, 'kinesiologo/pacientes/detalle.html', context)


@login_required(login_url='login')
def crear_paciente(request):
    """Crear un nuevo paciente"""
    if request.method == 'POST':
        fecha_nacimiento_raw = request.POST.get('fecha_nacimiento')
        fecha_nacimiento = convertir_fecha(fecha_nacimiento_raw)
        
        if not fecha_nacimiento:
            messages.error(request, 'Formato de fecha inválido. Usa DD/MM/YYYY o YYYY-MM-DD.')
            return render(request, 'kinesiologo/pacientes/crear.html')
        
        paciente = Paciente(
            rut=request.POST.get('rut'),
            nombre=request.POST.get('nombre'),
            fecha_nacimiento=fecha_nacimiento,
            telefono=request.POST.get('telefono'),
            direccion=request.POST.get('direccion'),
            comuna=request.POST.get('comuna'),
            diagnostico=request.POST.get('diagnostico'),
            estado=request.POST.get('estado', 'activo'),
            kinesiologo=request.user,
        )
        
        tiene_acompanante = request.POST.get('tiene_acompanante') == 'on'
        paciente.tiene_acompanante = tiene_acompanante
        if tiene_acompanante:
            paciente.acompanante_nombre = request.POST.get('acompanante_nombre')
            paciente.acompanante_telefono = request.POST.get('acompanante_telefono')
            paciente.acompanante_parentesco = request.POST.get('acompanante_parentesco')
        
        paciente.material_entregado = request.POST.get('material_entregado', 'ninguno')
        paciente.save()
        
        messages.success(request, f'Paciente {paciente.nombre} creado exitosamente.')
        return redirect('lista_pacientes')
    
    return render(request, 'kinesiologo/pacientes/crear.html')


@login_required(login_url='login')
def editar_paciente(request, paciente_id):
    """Editar un paciente existente"""
    paciente = get_object_or_404(Paciente, id=paciente_id, kinesiologo=request.user)
    
    if request.method == 'POST':
        fecha_nacimiento_raw = request.POST.get('fecha_nacimiento')
        fecha_nacimiento = convertir_fecha(fecha_nacimiento_raw)
        
        if not fecha_nacimiento:
            messages.error(request, 'Formato de fecha inválido. Usa DD/MM/YYYY o YYYY-MM-DD.')
            context = {'paciente': paciente}
            return render(request, 'kinesiologo/pacientes/editar.html', context)
        
        paciente.rut = request.POST.get('rut')
        paciente.nombre = request.POST.get('nombre')
        paciente.fecha_nacimiento = fecha_nacimiento
        paciente.telefono = request.POST.get('telefono')
        paciente.direccion = request.POST.get('direccion')
        paciente.comuna = request.POST.get('comuna')
        paciente.diagnostico = request.POST.get('diagnostico')
        paciente.estado = request.POST.get('estado')
        
        tiene_acompanante = request.POST.get('tiene_acompanante') == 'on'
        paciente.tiene_acompanante = tiene_acompanante
        if tiene_acompanante:
            paciente.acompanante_nombre = request.POST.get('acompanante_nombre')
            paciente.acompanante_telefono = request.POST.get('acompanante_telefono')
            paciente.acompanante_parentesco = request.POST.get('acompanante_parentesco')
        else:
            paciente.acompanante_nombre = None
            paciente.acompanante_telefono = None
            paciente.acompanante_parentesco = None
        
        paciente.material_entregado = request.POST.get('material_entregado', 'ninguno')
        paciente.save()
        
        messages.success(request, f'Paciente {paciente.nombre} actualizado exitosamente.')
        return redirect('detalle_paciente', paciente_id=paciente.id)
    
    context = {'paciente': paciente}
    return render(request, 'kinesiologo/pacientes/editar.html', context)


@login_required(login_url='login')
def eliminar_paciente(request, paciente_id):
    """Eliminar un paciente"""
    paciente = get_object_or_404(Paciente, id=paciente_id, kinesiologo=request.user)
    
    if request.method == 'POST':
        nombre = paciente.nombre
        paciente.delete()
        messages.success(request, f'Paciente {nombre} eliminado exitosamente.')
        return redirect('lista_pacientes')
    
    context = {'paciente': paciente}
    return render(request, 'kinesiologo/pacientes/eliminar.html', context)


# ==========================================
# ===== RUTINAS =====
# ==========================================

@login_required(login_url='login')
def lista_rutinas(request):
    """Lista de todas las rutinas"""
    rutinas = Rutina.objects.all()
    paciente_id = request.GET.get('paciente')
    
    if paciente_id:
        rutinas = rutinas.filter(paciente_id=paciente_id)
    
    context = {
        'rutinas': rutinas,
        'pacientes': Paciente.objects.filter(kinesiologo=request.user),
    }
    return render(request, 'kinesiologo/rutinas/lista.html', context)


@login_required(login_url='login')
def crear_rutina(request):
    """Crear una nueva rutina"""
    if request.method == 'POST':
        rutina = Rutina(
            paciente_id=request.POST.get('paciente'),
            titulo=request.POST.get('titulo'),
            descripcion=request.POST.get('descripcion'),
            ejercicios=request.POST.get('ejercicios'),
            video_url=request.POST.get('video_url'),
            duracion_minutos=request.POST.get('duracion_minutos', 30),
            frecuencia=request.POST.get('frecuencia', 'diaria'),
            estado='activa',
        )
        rutina.save()
        messages.success(request, f'Rutina "{rutina.titulo}" creada exitosamente.')
        return redirect('lista_rutinas')
    
    context = {
        'pacientes': Paciente.objects.filter(kinesiologo=request.user),
    }
    return render(request, 'kinesiologo/rutinas/crear.html', context)


@login_required(login_url='login')
def detalle_rutina(request, rutina_id):
    """Ver detalle de una rutina"""
    rutina = get_object_or_404(Rutina, id=rutina_id)
    context = {'rutina': rutina}
    return render(request, 'kinesiologo/rutinas/detalle.html', context)


@login_required(login_url='login')
def editar_rutina(request, rutina_id):
    """Editar una rutina"""
    rutina = get_object_or_404(Rutina, id=rutina_id)
    
    if request.method == 'POST':
        rutina.titulo = request.POST.get('titulo')
        rutina.descripcion = request.POST.get('descripcion')
        rutina.ejercicios = request.POST.get('ejercicios')
        rutina.video_url = request.POST.get('video_url')
        rutina.duracion_minutos = request.POST.get('duracion_minutos', 30)
        rutina.frecuencia = request.POST.get('frecuencia', 'diaria')
        rutina.estado = request.POST.get('estado', 'activa')
        rutina.save()
        
        messages.success(request, f'Rutina "{rutina.titulo}" actualizada exitosamente.')
        return redirect('detalle_rutina', rutina_id=rutina.id)
    
    context = {
        'rutina': rutina,
        'pacientes': Paciente.objects.filter(kinesiologo=request.user),
    }
    return render(request, 'kinesiologo/rutinas/editar.html', context)


@login_required(login_url='login')
def eliminar_rutina(request, rutina_id):
    """Eliminar una rutina"""
    rutina = get_object_or_404(Rutina, id=rutina_id)
    
    if request.method == 'POST':
        titulo = rutina.titulo
        rutina.delete()
        messages.success(request, f'Rutina "{titulo}" eliminada exitosamente.')
        return redirect('lista_rutinas')
    
    context = {'rutina': rutina}
    return render(request, 'kinesiologo/rutinas/eliminar.html', context)


# ==========================================
# ===== SEGUIMIENTOS =====
# ==========================================

@login_required(login_url='login')
def lista_seguimientos(request):
    """Lista de todos los seguimientos"""
    seguimientos = Seguimiento.objects.all().order_by('-fecha')
    paciente_id = request.GET.get('paciente')
    
    if paciente_id:
        seguimientos = seguimientos.filter(paciente_id=paciente_id)
    
    context = {
        'seguimientos': seguimientos,
        'pacientes': Paciente.objects.filter(kinesiologo=request.user),
    }
    return render(request, 'kinesiologo/seguimientos/lista.html', context)


@login_required(login_url='login')
def crear_seguimiento(request):
    """Crear un nuevo seguimiento"""
    if request.method == 'POST':
        # Obtener la fecha del próximo control
        fecha_proximo_control_raw = request.POST.get('fecha_proximo_control', '')
        
        # Depuración: imprimir el valor recibido (esto se ve en la terminal)
        print(f"Fecha recibida: '{fecha_proximo_control_raw}'")
        
        # Si la fecha está vacía o es None, asignar None
        if not fecha_proximo_control_raw or fecha_proximo_control_raw.strip() == '':
            fecha_proximo_control = None
        else:
            # Intentar convertir la fecha
            fecha_proximo_control = convertir_fecha(fecha_proximo_control_raw)
            print(f"Fecha convertida: '{fecha_proximo_control}'")

        # Crear el seguimiento
        seguimiento = Seguimiento(
            paciente_id=request.POST.get('paciente'),
            cumple_ejercicios=request.POST.get('cumple_ejercicios') == 'on',
            observaciones=request.POST.get('observaciones', ''),
            tipo_control=request.POST.get('tipo_control', 'presencial'),
            acompanante_presente=request.POST.get('acompanante_presente') == 'on',
            fecha_proximo_control=fecha_proximo_control,  # <--- Aquí se asigna
            kinesiologo=request.user,
        )
        seguimiento.save()
        
        # Depuración: mostrar lo que se guardó
        print(f"Seguimiento guardado: ID={seguimiento.id}, Fecha próximo control={seguimiento.fecha_proximo_control}")
        
        messages.success(request, 'Seguimiento registrado exitosamente.')
        return redirect('lista_seguimientos')
    
    context = {
        'pacientes': Paciente.objects.filter(kinesiologo=request.user),
    }
    return render(request, 'kinesiologo/seguimientos/crear.html', context)


@login_required(login_url='login')
def editar_seguimiento(request, seguimiento_id):
    """Editar un seguimiento existente"""
    seguimiento = get_object_or_404(Seguimiento, id=seguimiento_id)
    
    if request.method == 'POST':
        # Obtener y convertir la fecha del próximo control
        fecha_proximo_control_raw = request.POST.get('fecha_proximo_control')
        fecha_proximo_control = convertir_fecha(fecha_proximo_control_raw)
        
        seguimiento.paciente_id = request.POST.get('paciente')
        seguimiento.cumple_ejercicios = request.POST.get('cumple_ejercicios') == 'on'
        seguimiento.observaciones = request.POST.get('observaciones')
        seguimiento.tipo_control = request.POST.get('tipo_control', 'presencial')
        seguimiento.acompanante_presente = request.POST.get('acompanante_presente') == 'on'
        seguimiento.fecha_proximo_control = fecha_proximo_control
        seguimiento.save()
        
        messages.success(request, 'Seguimiento actualizado exitosamente.')
        return redirect('detalle_seguimiento', seguimiento_id=seguimiento.id)
    
    context = {
        'seguimiento': seguimiento,
        'pacientes': Paciente.objects.filter(kinesiologo=request.user),
    }
    return render(request, 'kinesiologo/seguimientos/editar.html', context)


@login_required(login_url='login')
def eliminar_seguimiento(request, seguimiento_id):
    """Eliminar un seguimiento"""
    seguimiento = get_object_or_404(Seguimiento, id=seguimiento_id)
    
    if request.method == 'POST':
        seguimiento.delete()
        messages.success(request, 'Seguimiento eliminado exitosamente.')
        return redirect('lista_seguimientos')
    
    context = {'seguimiento': seguimiento}
    return render(request, 'kinesiologo/seguimientos/eliminar.html', context)


@login_required(login_url='login')
def detalle_seguimiento(request, seguimiento_id):
    """Ver detalle de un seguimiento"""
    seguimiento = get_object_or_404(Seguimiento, id=seguimiento_id)
    context = {'seguimiento': seguimiento}
    return render(request, 'kinesiologo/seguimientos/detalle.html', context)


# ==========================================
# ===== ACOMPAÑANTES =====
# ==========================================

@login_required(login_url='login')
def lista_acompanantes(request):
    """Lista de todos los acompañantes"""
    pacientes_con_acompanante = Paciente.objects.filter(
        kinesiologo=request.user,
        tiene_acompanante=True
    )
    
    context = {
        'pacientes': pacientes_con_acompanante,
    }
    return render(request, 'kinesiologo/acompanantes/lista.html', context)


@login_required(login_url='login')
def detalle_acompanante(request, paciente_id):
    """Ver detalle de un acompañante"""
    paciente = get_object_or_404(Paciente, id=paciente_id, kinesiologo=request.user)
    seguimientos = paciente.seguimientos.all().order_by('-fecha')
    
    context = {
        'paciente': paciente,
        'seguimientos': seguimientos,
    }
    return render(request, 'kinesiologo/acompanantes/detalle.html', context)