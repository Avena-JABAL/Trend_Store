from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Carrinho, Roupa


class SeedDataCommandTests(TestCase):
	def test_cria_produtos_de_exemplo_sem_duplicar_ao_reexecutar(self):
		call_command("seed", stdout=StringIO())
		quantidade_inicial = Roupa.objects.count()

		call_command("seed", stdout=StringIO())

		self.assertGreater(quantidade_inicial, 0)
		self.assertEqual(Roupa.objects.count(), quantidade_inicial)

	def test_preserva_produto_existente_com_nome_de_exemplo(self):
		Roupa.objects.create(
			nome="Camiseta Básica",
			preco="1.00",
			estoque=1,
			tamanho="PP",
		)

		call_command("seed", stdout=StringIO())

		produto = Roupa.objects.get(nome="Camiseta Básica")
		self.assertEqual(produto.preco, 1)
		self.assertEqual(produto.estoque, 1)
		self.assertEqual(produto.tamanho, "PP")


class CriacaoAutomaticaCarrinhoTests(TestCase):
	def test_cria_carrinho_ao_criar_usuario(self):
		usuario = get_user_model().objects.create_user(
			username="cliente_teste",
			password="Senha-forte-de-teste-123",
		)

		self.assertEqual(Carrinho.objects.filter(usuario=usuario).count(), 1)


class AutenticacaoTests(TestCase):
	def test_tela_exibe_login_e_cadastro(self):
		resposta = self.client.get(reverse("login"))

		self.assertContains(resposta, "Entrar")
		self.assertContains(resposta, "Criar conta")
		self.assertEqual(resposta.context["active_form"], "login")

	# Confirma que erros de cadastro não fazem o usuário voltar ao painel de login.
	def test_tela_mantem_cadastro_aberto_quando_dados_sao_invalidos(self):
		resposta = self.client.post(reverse("login"), {
			"acao": "cadastro",
			"username": "novo_cliente",
			"password1": "senha-invalida",
			"password2": "outra-senha",
		})

		self.assertEqual(resposta.status_code, 200)
		self.assertEqual(resposta.context["active_form"], "cadastro")

	# Além de criar a conta, o cadastro deve abrir a sessão e acionar o sinal do carrinho.
	def test_cadastro_cria_usuario_carrinho_e_inicia_sessao(self):
		senha = "Compra-Segura-2026!"
		resposta = self.client.post(reverse("login"), {
			"acao": "cadastro",
			"username": "novo_cliente",
			"password1": senha,
			"password2": senha,
		})
		usuario = get_user_model().objects.get(username="novo_cliente")

		self.assertRedirects(resposta, reverse("catalogo"))
		self.assertTrue(usuario.check_password(senha))
		self.assertTrue(Carrinho.objects.filter(usuario=usuario).exists())
		self.assertIn("_auth_user_id", self.client.session)

	def test_login_valido_inicia_sessao(self):
		senha = "Compra-Segura-2026!"
		get_user_model().objects.create_user(
			username="cliente_existente",
			password=senha,
		)

		resposta = self.client.post(reverse("login"), {
			"acao": "login",
			"username": "cliente_existente",
			"password": senha,
		})

		self.assertRedirects(resposta, reverse("catalogo"))
		self.assertIn("_auth_user_id", self.client.session)


class LogoutTests(TestCase):
	def test_botao_logout_so_aparece_para_usuario_autenticado(self):
		resposta_anonima = self.client.get(reverse("catalogo"))
		self.assertNotContains(resposta_anonima, "Sair")

		usuario = get_user_model().objects.create_user(
			username="cliente_logado",
			password="Compra-Segura-2026!",
		)
		self.client.force_login(usuario)

		resposta_logada = self.client.get(reverse("catalogo"))
		self.assertContains(resposta_logada, "Sair")

	def test_logout_encerra_sessao_e_volta_ao_catalogo(self):
		usuario = get_user_model().objects.create_user(
			username="cliente_para_sair",
			password="Compra-Segura-2026!",
		)
		self.client.force_login(usuario)

		resposta = self.client.post(reverse("logout"))

		self.assertRedirects(resposta, reverse("catalogo"))
		self.assertNotIn("_auth_user_id", self.client.session)
