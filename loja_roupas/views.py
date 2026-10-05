from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'login.html')
def catalogo(request):
    return render(request, 'catalogo.html')
def carrinho(request):
    return render(request, 'carrinho.html')
def produto(request):
    return render(request, 'produto.html')
