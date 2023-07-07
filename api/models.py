from django.db import models
from django_extensions.db.models import (
	TimeStampedModel,
)

class OnePieceCapituloManga(TimeStampedModel, models.Model):
    capitulo = models.IntegerField(primary_key=True)
    volumen = models.IntegerField()
    titulo = models.CharField(max_length=255)
    titulo_romanizado = models.CharField(max_length=255)
    titulo_viz = models.CharField(max_length=255)
    paginas = models.IntegerField()
    fecha_publicacion = models.DateField()
    episodios = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='onepiece_covers/', blank=True, null=True)

    def __str__(self):
        return f'One Piece - Capítulo #{self.capitulo}'