from django.urls import path
from .views import login, produto, carrinho, catalogo

urlpatterns = [
    path('', catalogo),
    path('login', login),
    path('carrinho', carrinho),
    path('produto', produto),

]
