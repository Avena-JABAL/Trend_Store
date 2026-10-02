from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Carrinho


class CriacaoAutomaticaCarrinhoTests(TestCase):
	def test_cria_carrinho_ao_criar_usuario(self):
		usuario = get_user_model().objects.create_user(
			username="cliente_teste",
			password="Senha-forte-de-teste-123",
		)

		self.assertEqual(Carrinho.objects.filter(usuario=usuario).count(), 1)
