from django.urls import path
from .views import login, produto, carrinho, catalogo, logout
from . import views

urlpatterns = [
    path('', catalogo, name="catalogo"),
    path('login', login, name="login"),
    path('produto/<int:id>/', produto, name="produto"),
    path('logout', logout, name='logout'),

    # Carrinho de compras
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:roupa_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover-unidade/<int:roupa_id>/', views.remover_uma_unidade, name='remover_uma_unidade'),
    path('carrinho/remover/<int:roupa_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
]
