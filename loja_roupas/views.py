from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import Roupa, Carrinho, ItemCarrinho
# Create your views here.

def login(request):
    login_form = AuthenticationForm(request=request)
    cadastro_form = UserCreationForm()
    active_form = 'login'

    if request.method == 'POST':
        if request.POST.get('acao') == 'cadastro':
            active_form = 'cadastro'
            cadastro_form = UserCreationForm(request.POST)

            if cadastro_form.is_valid():
                usuario = cadastro_form.save()
                auth_login(request, usuario)
                return redirect('catalogo')
        else:
            login_form = AuthenticationForm(request=request, data=request.POST)

            if login_form.is_valid():
                auth_login(request, login_form.get_user())
                return redirect('catalogo')

    return render(request, 'login.html', {
        'login_form': login_form,
        'cadastro_form': cadastro_form,
        'active_form': active_form,
    })


def catalogo(request):
    roupas = Roupa.objects.all()

    return render(request, 'catalogo.html', {
        'roupas': roupas
    })


def logout(request):
    if request.method == 'POST':
        auth_logout(request)

    return redirect('catalogo')

@login_required
def remover_uma_unidade(request, roupa_id):
    carrinho = get_object_or_404(
        Carrinho,
        usuario=request.user
    )

    item = get_object_or_404(
        ItemCarrinho,
        carrinho=carrinho,
        roupa_id=roupa_id
    )

    if item.quantidade > 1:
        item.quantidade -= 1
        item.save(update_fields=['quantidade'])
    else:
        item.delete()

    return redirect('carrinho')


@login_required
def remover_do_carrinho(request, roupa_id):
    carrinho = get_object_or_404(
        Carrinho,
        usuario=request.user
    )

    item = get_object_or_404(
        ItemCarrinho,
        carrinho=carrinho,
        roupa_id=roupa_id
    )

    item.delete()

    return redirect('carrinho')

@login_required
def remover_selecionados(request):
    if request.method == 'POST':
        carrinho = get_object_or_404(
            Carrinho,
            usuario=request.user
        )

        ids = request.POST.getlist('produtos')

        ItemCarrinho.objects.filter(
            carrinho=carrinho,
            roupa_id__in=ids
        ).delete()

    return redirect('carrinho')

@login_required
def adicionar_carrinho(request, roupa_id):
    roupa = get_object_or_404(Roupa, id=roupa_id)

    carrinho, created = Carrinho.objects.get_or_create(
        usuario=request.user
    )

    item, created = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        roupa=roupa,
        defaults={'quantidade': 1}
    )

    if not created:
        item.quantidade += 1
        item.save(update_fields=['quantidade'])

    return redirect('carrinho')


@login_required
def carrinho(request):
    carrinho, created = Carrinho.objects.get_or_create(
        usuario=request.user
    )

    itens_carrinho = carrinho.itens.select_related('roupa')

    total = sum(
        item.roupa.preco * item.quantidade
        for item in itens_carrinho
    )

    return render(request, 'carrinho.html', {
        'itens': itens_carrinho,
        'total': total,
    })


def produto(request, id):
    roupa = get_object_or_404(Roupa, id=id) 

    return render(request, 'produto.html', {
        'roupa': roupa
        })
