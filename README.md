# Tournament-Manager

## Descripción

Aplicación web desarrollada con Django para gestionar torneos de videojuegos. Permite el registro de usuarios, la gestión de torneos y la diferenciación de roles entre jugadores y organizadores.

## Tecnologías

- Python 3.14
- Django
- SQLite
- HTML
- CSS
- JavaScript

---

## Funcionalidades

- Registro e inicio de sesión
- Roles de usuario
- Gestión de torneos
- Inscripciones
- Gestión de puntuaciones
- Estadísticas de jugadores

## Instalación

### 1. Clonar el repositorio
git clone https://github.com/Lubreco-20/Tournament-Manager.git

cd Tournament-Manager

### 2. Crear el entorno virtual
python -m venv venv

### 3. Activar el entorno virtual
(Powershell)
./venv/Scripts/Activate.ps1

(Windows CMD)
venv/Scripts/activate

(Linux/Mac)
source venv/bin/activate

### 4. Instalar dependencias
cd apptorneo

pip install -r requirements.txt

### 5. Aplicar migraciones
python manage.py migrate

### 6. Iniciar servidor
python manage.py runserver

La aplicación estará disponible en: http://127.0.0.1:8000/

---

## Código para Organizadores

Para facilitar las pruebas del proyecto, la creación de cuentas con rol de organizador requiere un código de autorización.

Código de organizador: TORNEO2026

---

## Posible mejoras a futuro

- API REST
- Despliegue en Docker
- Notificaciones
- Panel de administración ampliado
- Sistema de recuperación de contraseñas
- Integración con correo electrónico
- Autenticación mediante JWT