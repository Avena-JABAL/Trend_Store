from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import Roupa
from .cart import Cart

# Create your views here.

def login(request):
    login_form = AuthenticationForm(request=request)
    cadastro_form = UserCreationForm()
    # Define qual painel fica visível ao abrir a página ou retornar com erros.
    active_form = 'login'

    if request.method == 'POST':
        # O campo oculto "acao" identifica qual formulário foi enviado.
        if request.POST.get('acao') == 'cadastro':
            active_form = 'cadastro'
            cadastro_form = UserCreationForm(request.POST)

            if cadastro_form.is_valid():
                usuario = cadastro_form.save()
                # O cadastro também inicia a sessão do novo usuário.
                auth_login(request, usuario)
                return redirect('catalogo')
        else:
            login_form = AuthenticationForm(request=request, data=request.POST)

            if login_form.is_valid():
                # O AuthenticationForm já validou as credenciais enviadas.
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
    # Encerrar sessão altera estado, então a rota só aceita POST.
    if request.method == 'POST':
        auth_logout(request)

    return redirect('catalogo')

def remover_uma_unidade(request, roupa_id):
    carrinho = request.session.get('carrinho', {})
    str_id = str(roupa_id)

    if str_id in carrinho:
        if carrinho[str_id] > 1:
            carrinho[str_id] -= 1
        else:
            del carrinho[str_id]

    request.session['carrinho'] = carrinho
    request.session.modified = True
    return redirect('carrinho')


def remover_do_carrinho(request, roupa_id):
    carrinho = request.session.get('carrinho', {})
    str_id = str(roupa_id)

    if str_id in carrinho:
        del carrinho[str_id]

    request.session['carrinho'] = carrinho
    request.session.modified = True
    return redirect('carrinho')

def remover_selecionados(request):
    if request.method == 'POST':
        carrinho = request.session.get('carrinho', {})

        ids = request.POST.getlist('produtos')

        for roupa_id in ids:
            roupa_id = str(roupa_id)

            if roupa_id in carrinho:
                del carrinho[roupa_id]

        request.session['carrinho'] = carrinho
        request.session.modified = True

    return redirect('carrinho')


def adicionar_carrinho(request, roupa_id):
    carrinho = request.session.get('carrinho', {})
    
    str_id = str(roupa_id)
    carrinho[str_id] = carrinho.get(str_id, 0) + 1

    request.session['carrinho'] = carrinho
    request.session.modified = True

    return redirect('carrinho')


def ver_carrinho(request):
    cart = Cart(request)
    produtos_adicionados = []

    for roupa_id, item_data in cart.cart.items():
        roupa = get_object_or_404(Roupa, id=roupa_id)
        produtos_adicionados.append({
            'nome': roupa.nome,
            'preco': roupa.preco,
            'imagem': roupa.imagem if roupa.imagem else '',
            'quantidade': item_data['quantity'],
            'id': roupa.id,
        })
    return render(request, 'carrinho.html', {
        'itens_carrinho' : produtos_adicionados,
        'show_actions':True
    })

@login_required
def carrinho(request):
    carrinho_sessao = request.session.get('carrinho', {})
    itens_carrinho = []
    total = 0

    for roupa_id, quantidade in carrinho_sessao.items():
        try:
            produto = Roupa.objects.get(id=int(roupa_id))
            subtotal = produto.preco * quantidade
            total += subtotal

            itens_carrinho.append({
                'produto': produto,
                'quantidade': quantidade,
                'subtotal': subtotal,
            })   
        except Roupa.DoesNotExist:
            continue 
    context = {
        'itens': itens_carrinho,
        'total': total,
    }

    return render(request, 'carrinho.html', context)


def produto(request, id):
    roupa = get_object_or_404(Roupa, id=id) 

    return render(request, 'produto.html', {
        'roupa': roupa
        })
