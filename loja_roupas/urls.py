from django.urls import path
from .views import login, produto, carrinho, catalogo, logout

urlpatterns = [
    path('', catalogo, name='catalogo'),
    path('login', login, name='login'),
    path('carrinho', carrinho),
    path('produto', produto),
    path('logout', logout, name='logout'),

]
