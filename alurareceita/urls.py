from django.urls import path
from .views import *

urlpatterns = [
    path('index', index_receita, name='index_receita'),
    path ('<int:receita_id>', receita, name='receita'),
    path('buscar', busca, name='buscar'),
    path('cria/receita', cria_receita, name='cria_receita'),
    path('deleta/<int:receita_id>', deleta_receita, name='deleta_receita'),
    path('edita/<int:receita_id>', edita_receita, name='edita_receita'),
    path('atualiza_receita', atualiza_receita, name='atualiza_receita'),
    path('usuarios/cadastro', cadastro, name='cadastro'),
    path('usuarios/login', login, name='login'),
    path('usuarios/dashboard', dashboard, name='dashboard'),
    path('usuarios/logout', logout, name='logout'),
]