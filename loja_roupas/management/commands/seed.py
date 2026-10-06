from django.core.management.base import BaseCommand

from loja_roupas.models import Roupa


class Command(BaseCommand):
    help = "Adiciona produtos de exemplo ao catálogo sem alterar dados existentes."

    produtos = [
        {"nome": "Camiseta Básica", "preco": "49.90", "estoque": 20, "tamanho": "M"},
        {"nome": "Calça Jeans", "preco": "129.90", "estoque": 12, "tamanho": "40"},
        {"nome": "Vestido Floral", "preco": "159.90", "estoque": 8, "tamanho": "M"},
        {"nome": "Moletom Unissex", "preco": "189.90", "estoque": 10, "tamanho": "G"},
        {"nome": "Jaqueta Corta-Vento", "preco": "219.90", "estoque": 6, "tamanho": "G"},
        {"nome": "Saia Midi", "preco": "99.90", "estoque": 9, "tamanho": "P"},
        {"nome": "Camisa de Linho", "preco": "139.90", "estoque": 7, "tamanho": "M"},
        {"nome": "Shorts Casual", "preco": "79.90", "estoque": 14, "tamanho": "42"},
    ]

    def handle(self, *args, **options):
        criados = 0

        for produto in self.produtos:
            _, criado = Roupa.objects.get_or_create(
                nome=produto["nome"],
                defaults=produto,
            )
            criados += criado

        existentes = len(self.produtos) - criados
        self.stdout.write(
            self.style.SUCCESS(
                f"Seed concluído: {criados} produto(s) criado(s), "
                f"{existentes} já existente(s) preservado(s)."
            )
        )
