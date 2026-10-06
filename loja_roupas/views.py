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

@login_required
def adicionar_carrinho(request, roupa_id):
    cart = Cart(request)
    cart.add(roupa_id=roupa_id)
    return redirect('ver_carrinho')

def ver_carrinho(request):
    cart = Cart(request)
    produtos_adicionados = []

    for roupa_id, item_data in cart.cart.items():
        roupa = get_object_or_404(Roupa, id=roupa_id)
        produtos_adicionados.append({
            'nome': roupa.nome,
            'preco': roupa.preco,
            'imagem': roupa.imagem.url if roupa.imagem else '',
            'quantidade': item_data['quantity'],
            'id': roupa.id,
        })
    return render(request, 'carrinho.html', {
        'itens_carrinho' : produtos_adicionados,
        'show_actions':True
    })

def carrinho(request):
    itens = [  
    {
        "nome": "Vestido Longo", 
        "preco": "140,90", 
        "descricao": "Vermelho Vinho" 
     },
     {
        "nome": "Calça leve", 
        "preco": "99,99", 
        "descricao": "Calça marrom", 
     },
     {
        "nome": "Sapatilha", 
        "preco": "90,00", 
        "descricao": "Cor Prata", 
        "imagem": "https://imgs.search.brave.com/yBKyDuT2RNr41Tim4THWpXVFJs5gN5xMxSVOZEc4am8/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9tcmNh/dHN0b3JlLnZ0ZXhp/bWcuY29tLmJyL2Fy/cXVpdm9zL2lkcy8x/MTEwMzMwLTEwMDAt/MTIwMC8yYTczZDU1/NC04MjUzLTQxNzUt/OTFjMS05NWJmNDcx/ODMyYTEuanBnP3Y9/NjM5MjI3NDg1MDA4/NDAwMDAw",
     },
     ]

    return render(request, 'carrinho.html' , {
        "itens": itens
    })


def produto(request, id):
    roupa = get_object_or_404(Roupa, id=id) 

    return render(request, 'produto.html', {
        'roupa': roupa
        })
