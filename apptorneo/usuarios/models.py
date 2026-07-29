from django.db import models
from django.contrib.auth.models import AbstractUser

# Creamos un modelo de usuario personalizado para gestionar las autentificaciones a nuestra manera
class Usuario(AbstractUser):
    # Definimos los roles disponibles para los usuarios. 
    # El primer valor es el puesto en la base de datos y el segundo es el valor legible para los humanos.
    ROLE_CHOICES = [
        ('jugador', 'Jugador'),
        ('organizador', 'Organizador'),
    ]
    
    email = models.EmailField(unique=True)                      # Correo electrónico del usuario, debe ser único
    role = models.CharField(max_length=20, 
                            choices=ROLE_CHOICES, 
                            default='jugador')                  # Rol del usuario, puede ser jugador u organizador. Por defecto es jugador.
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.email}) - {self.role}"