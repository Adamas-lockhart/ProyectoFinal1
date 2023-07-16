from django.db import models
####
#de esta manera se puede usar el Charfield o ImageField sin tener que usar el "models."
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
####
# Create your models here.

class porto(models.Model):
    titulo = models.CharField( max_length=150)
    descripcion = models.CharField(max_length=1500)
    imagenes = models.ImageField(upload_to='porto1/images')
    url = models.URLField(blank=True)