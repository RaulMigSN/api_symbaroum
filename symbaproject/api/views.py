from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .models import Usuario, Jogador, Habilidade, DescricaoHabilidade, Qualidade, Equipamento, Elixir, Arma, Armadura, Artefato, Poder, Personagem, Aprende
from .serializers import UsuarioSerializer, JogadorSerializer, HabilidadeSerializer, DescricaoHabilidadeSerializer, QualidadeSerializer, EquipamentoSerializer, ElixirSerializer, ArmaSerializer, ArmaduraSerializer, ArtefatoSerializer, PoderSerializer, PersonagemSerializer, AprendeSerializer, CustomTokenObtainPairSerializer

"""Uso do ModelViewSet transforma todas as views no que queremos, onde cada view dará acesso a o CRUD facilmente, ou seja, os ViewsSets irão herdar automaticamente todas as
operações REST padrão, ou seja, GET, POST, GET(por id), PUT/PATCH e DELETE"""

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class JogadorViewSet(ModelViewSet):
    queryset = Jogador.objects.all()
    serializer_class = JogadorSerializer
    permission_classes = [IsAuthenticated]

class PersonagemViewSet(ModelViewSet):
    queryset = Personagem.objects.all()
    serializer_class = PersonagemSerializer
    permission_classes = [IsAuthenticated]
    
class HabilidadeViewSet(ModelViewSet):
    queryset = Habilidade.objects.all()
    serializer_class = HabilidadeSerializer

class DescricaoHabilidadeViewSet(ModelViewSet):
    queryset = DescricaoHabilidade.objects.all()
    serializer_class = DescricaoHabilidadeSerializer

class QualidadeViewSet(ModelViewSet):
    queryset = Qualidade.objects.all()
    serializer_class = QualidadeSerializer

class EquipamentoViewSet(ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    permission_classes = [IsAuthenticated]

class ElixirViewSet(ModelViewSet):
    queryset = Elixir.objects.all()
    serializer_class = ElixirSerializer

class ArmaViewSet(ModelViewSet):
    queryset = Arma.objects.all()
    serializer_class = ArmaSerializer
    permission_classes = [IsAuthenticated]

class ArmaduraViewSet(ModelViewSet):
    queryset = Armadura.objects.all()
    serializer_class = ArmaduraSerializer
    permission_classes = [IsAuthenticated]

class ArtefatoViewSet(ModelViewSet):
    queryset = Artefato.objects.all()
    serializer_class = ArtefatoSerializer
    permission_classes = [IsAuthenticated]
    
class PoderViewSet(ModelViewSet):
    queryset = Poder.objects.all()
    serializer_class = PoderSerializer
    permission_classes = [IsAuthenticated]
    
class AprendeViewSet(ModelViewSet):
    queryset = Aprende.objects.all()
    serializer_class = AprendeSerializer
    permission_classes = [IsAuthenticated]