import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jardineando_projecto.settings')
django.setup()

from api.models import OnePieceCapituloManga as prueba

prueba.objects.all().delete()