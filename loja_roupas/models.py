from django.conf import settings
from django.db import models

# Create your models here.

class Roupa(models.Model):
    nome = models.CharField (max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    tamanho = models.CharField(max_length=10)
    imagem = models.CharField(max_length=2048, blank=True, default="")

class Carrinho(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE,
          related_name='carrinho',
          )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrinho de {self.usuario.username}"

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(
        Carrinho,
        on_delete=models.CASCADE,
        related_name="itens",
    )
    roupa = models.ForeignKey(
        Roupa,
        on_delete=models.PROTECT,
        related_name="itens_em_carrinhos",
    )
    quantidade = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["carrinho", "roupa"],
                name="unq_roupa_por_carrinho",
            ),
            models.CheckConstraint(
                condition=models.Q(quantidade__gte=1),
                name="item_carrinho_quantidade_minima_1",
            ),
        ]

    def __str__(self):
        return f"{self.quantidade} x {self.roupa.nome}"    