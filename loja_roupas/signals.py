from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Carrinho


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def criar_carrinho_para_usuario(sender, instance, created, **kwargs):
    if created:
        Carrinho.objects.get_or_create(usuario=instance)