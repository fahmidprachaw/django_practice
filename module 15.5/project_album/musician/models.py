from django.db import models

# Create your models here.

class Musician(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    number = models.CharField(max_length=12)
    instrument = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.firstName