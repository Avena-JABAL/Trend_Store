from django.db import models

# Create your models here.
class Roupa(models.Model):
    nome = models.CharField (max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    tamanho = models.CharField(max_length=10)
