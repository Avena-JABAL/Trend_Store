from django.urls import path
from .views import login, produto, carrinho, catalogo, logout
from . import views

urlpatterns = [
    path('', catalogo, name="catalogo"),
    path('login', login, name="login"),
    path('produto/<int:id>/', produto, name="produto"),
    path('logout', logout, name='logout'),
    path('carrinho/', views.ver_carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
]
