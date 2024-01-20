from django.db import models
from musician.models import Musician

# Create your models here.

class Album(models.Model):
    albumName = models.CharField(max_length=50)
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    release = models.DateField(auto_now=False, auto_now_add=False)
    rating = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.albumName} by {self.musician.firstName}'