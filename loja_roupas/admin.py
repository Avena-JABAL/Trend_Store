from django.contrib import admin
from .models import Roupa

class RoupaAdmin(admin.ModelAdmin):
    list_display = 'nome', 'preco', 'estoque', 'tamanho', 'imagem', 'id'

# Register your models here.
admin.site.register(Roupa, RoupaAdmin)