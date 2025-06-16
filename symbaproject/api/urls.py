from django.urls import path
from . import views

urlpatterns = [
    path('jogadores/', views.JogadorListCreateView.as_view(), name='jogador-list-create-view'),
    path('usuarios/', views.UsuarioListCreateView.as_view(), name='usuario-list-create-view'),
]