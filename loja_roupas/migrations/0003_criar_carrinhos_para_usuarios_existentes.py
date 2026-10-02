from django.conf import settings
from django.db import migrations


def criar_carrinhos_para_usuarios_existentes(apps, schema_editor):
    database = schema_editor.connection.alias
    usuario_model = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    carrinho_model = apps.get_model("loja_roupas", "Carrinho")

    for usuario in usuario_model.objects.using(database).iterator():
        carrinho_model.objects.using(database).get_or_create(usuario_id=usuario.pk)


class Migration(migrations.Migration):
    dependencies = [
        ("loja_roupas", "0002_carrinho_itemcarrinho"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(
            criar_carrinhos_para_usuarios_existentes,
            migrations.RunPython.noop,
        ),
    ]