# Tournament-Manager

## Descripción

Una pequeña aplicación wbe que desarrollé como proyecto final de curso para gestionar torneos de videojuegos con Django. Contiene autenticación de usuarios, roles diferenciados entre Jugadores y Organizadores, gestión de torneos, inscripciones y estadísticas.

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

---

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
/venv/Scripts/activate

(Linux/Mac)
source venv/bin/activate

### 4. Instalar dependencias
pip install -r requirements.txt

### 5. Aplicar migraciones
python manage.py migrate

### 6. Iniciar servidor
python manage.py runserver

La aplicación estará disponible en: http://127.0.0.1:8000/

---

## Código para Organizadores

Solo los organizadores pueden crear, modificar, editar puntuaciones y eliminar torneos. Eso es demasiado poder para un usuario corriente, así que está delimitado solo a los Organizadores los cuales tendrán que poner la clave "TORNEO2026" para poder ser identificados como tales.

---

## Posible mejoras futuras

- API REST
- Docker
- Notificaciones
- Panel de administración ampliado