from django.urls import path
from .views import login, produto, carrinho, catalogo

urlpatterns = [
    path('', catalogo, name="catalogo"),
    path('login', login, name="login"),
    path('carrinho', carrinho, name="carrinho"),
    path('produto', produto, name="produto"),

]
