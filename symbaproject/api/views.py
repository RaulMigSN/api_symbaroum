from django.shortcuts import render
from rest_framework import generics
from .models import Usuario, Jogador, Habilidade, DescricaoHabilidade, Qualidade, Equipamento, Elixir, Arma, Armadura, Artefato, Poder, Personagem, Aprende
from .serializers import UsuarioSerializer, JogadorSerializer, HabilidadeSerializer, DescricaoHabilidadeSerializer, QualidadeSerializer, EquipamentoSerializer, ElixirSerializer, ArmaSerializer, ArmaduraSerializer, ArtefatoSerializer, PoderSerializer, PersonagemSerializer, AprendeSerializer

class JogadorListCreateView(generics.ListCreateAPIView):
    """View para listar e criar Jogadores."""
    queryset = Jogador.objects.all()
    serializer_class = JogadorSerializer
    
class UsuarioListCreateView(generics.ListCreateAPIView):
    """View para listar e criar Usuários."""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer