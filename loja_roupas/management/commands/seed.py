from django.core.management.base import BaseCommand

from loja_roupas.models import Roupa


class Command(BaseCommand):
    help = "Adiciona produtos de exemplo ao catálogo sem alterar dados existentes."

    produtos = [
        {
            "nome": "Camiseta Básica",
            "preco": "49.90",
            "estoque": 20,
            "tamanho": "M",
            "imagem": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?auto=format&fit=crop&w=800&q=80",
        },
        {
            "nome": "Calça Jeans",
            "preco": "129.90",
            "estoque": 12,
            "tamanho": "40",
            "imagem": "https://images.unsplash.com/photo-1602293589930-45aad59ba3ab?auto=format&fit=crop&w=800&q=80",
        },
        {
            "nome": "Vestido Floral",
            "preco": "159.90",
            "estoque": 8,
            "tamanho": "M",
            "imagem": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=800&q=80",
        },
        {
            "nome": "Moletom Unissex",
            "preco": "189.90",
            "estoque": 10,
            "tamanho": "G",
            "imagem": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?auto=format&fit=crop&w=800&q=80",
        },
        {
            "nome": "Jaqueta Corta-Vento",
            "preco": "219.90",
            "estoque": 6,
            "tamanho": "G",
            "imagem": "https://images.unsplash.com/photo-1771605884393-056bd7a70a12?auto=format&fit=crop&w=800&q=80",
        },
        {
            "nome": "Saia Midi",
            "preco": "99.90",
            "estoque": 9,
            "tamanho": "P",
            "imagem": "https://images.unsplash.com/photo-1789110854735-67c4e4737aa2?auto=format&fit=crop&w=800&q=80",
        },
        {
            "nome": "Camisa de Linho",
            "preco": "139.90",
            "estoque": 7,
            "tamanho": "M",
            "imagem": "https://images.unsplash.com/photo-1740711152088-88a009e877bb?auto=format&fit=crop&w=800&q=80",
        },
        {
            "nome": "Shorts Casual",
            "preco": "79.90",
            "estoque": 14,
            "tamanho": "42",
            "imagem": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?auto=format&fit=crop&w=800&q=80",
        },
    ]

    def handle(self, *args, **options):
        criados = 0
        imagens_atualizadas = 0

        for produto in self.produtos:
            roupa, criado = Roupa.objects.get_or_create(
                nome=produto["nome"],
                defaults=produto,
            )
            criados += criado
            if not criado and not roupa.imagem:
                roupa.imagem = produto["imagem"]
                roupa.save(update_fields=["imagem"])
                imagens_atualizadas += 1

        existentes = len(self.produtos) - criados
        self.stdout.write(
            self.style.SUCCESS(
                f"Seed concluído: {criados} produto(s) criado(s), "
                f"{existentes} já existente(s) preservado(s), "
                f"{imagens_atualizadas} imagem(ns) preenchida(s)."
            )
        )
