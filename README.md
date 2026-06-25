# TeleRehab Kine 📚
Prototipo simple desarrollado en Junio 2026 para la asignatura de Innovación y Emprendimiento 2.
Este sistema representa una aplicación web de gestión kinesiológica enfocada en el seguimiento y administración remota de pacientes en rehabilitación de zonas rurales.

---

## 👥 Autores

**Matías Gajardo** y **Jean Pierre Avastia**

---

## 🧩 Descripción del proyecto

TeleRehab Kine es un prototipo académico funcional pero simple, creado para demostrar una solución tecnológica orientada a la rehabilitación remota. Fue desarrollado con:

- Modelado de datos relacionales en Django.
- Operaciones CRUD con vistas basadas en funciones.
- Autenticación de usuarios con Django Auth.
- Navegación por plantillas HTML con Tailwind CSS.

El sistema permite gestionar las entidades principales de un flujo de rehabilitación kinesiológica remota:

- Pacientes (con datos personales, clínicos y de acompañante).
- Rutinas de rehabilitación con ejercicios y frecuencia.
- Seguimientos clínicos con tipo de control y próxima fecha.
- Notas rápidas del kinesiólogo por paciente.
- Acompañantes vinculados a los pacientes.

---

## ✨ Características principales

- CRUD completo en interfaz web para todas las entidades del sistema.
- Autenticación con login y logout protegido por `@login_required`.
- Dashboard con estadísticas: total de pacientes, activos, rutinas y próximos controles.
- Búsqueda de pacientes por nombre, RUT o diagnóstico.
- Registro de controles presenciales, telefónicos, vía WhatsApp o por cartilla.
- Soporte para acompañantes con datos de contacto y parentesco.
- Control de material entregado al paciente (DVD, pendrive o ninguno).
- Estilos con Tailwind CSS integrado directamente en el proyecto.

---

## 🛠️ Stack tecnológico

- Python 3.x
- Django 5.1.6
- HTML, CSS y plantillas Django
- Tailwind CSS (instalado localmente vía Node.js)
- SQLite (base de datos por defecto de este repositorio)

---

## 🗂️ Estructura del proyecto

- `telerehab/`: configuración principal del proyecto (settings, urls, wsgi, asgi).
- `kinesiologo/`: app principal con modelos, vistas, plantillas y rutas.
- `kinesiologo/templates/kinesiologo/`: plantillas para login, dashboard y vistas CRUD.
- `static/css/`: archivos CSS estáticos del proyecto.
- `theme/`: configuración de Tailwind CSS.

---

## 🚀 Puesta en marcha local

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd telerehab-kine
```

### 2. Crear y activar entorno virtual (Windows PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones
```bash
python manage.py migrate
```

### 5. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 6. Iniciar servidor
```bash
python manage.py runserver
```

---

## 🌐 Rutas útiles

| Ruta | Descripción |
|------|-------------|
| `http://127.0.0.1:8000/` | Login / Página de inicio |
| `http://127.0.0.1:8000/dashboard/` | Dashboard principal |
| `http://127.0.0.1:8000/pacientes/` | Listado de pacientes |
| `http://127.0.0.1:8000/rutinas/` | Listado de rutinas |
| `http://127.0.0.1:8000/seguimientos/` | Listado de seguimientos |
| `http://127.0.0.1:8000/acompanantes/` | Listado de acompañantes |
| `http://127.0.0.1:8000/admin/` | Panel de administración Django |

---

## ☁️ Base de datos

Para facilitar la ejecución local y la revisión académica, esta versión del repositorio utiliza **SQLite** por defecto, de modo que puedas probarla rápido y sin configuraciones externas.

---

## 🎯 Contexto académico

Este repositorio corresponde a un prototipo entregado en la asignatura **Innovación y Emprendimiento 2**.
El objetivo principal fue prototipar una solución digital para un problema real: la falta de acceso a rehabilitación kinesiológica en zonas rurales. El foco estuvo en la propuesta de valor y la funcionalidad básica, no en la arquitectura de producción.

---

## 📌 Resumen

TeleRehab Kine es un prototipo académico simple para gestionar datos de rehabilitación kinesiológica remota en zonas rurales.
Fue construido por **Matías Gajardo** y **Jean Pierre Avastia** en el marco de la asignatura **Innovación y Emprendimiento 2**, como demostración funcional de una idea con impacto social.
