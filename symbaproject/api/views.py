from rest_framework.exceptions  import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .models import ArmaBase, ArmaduraBase, ArtefatoBase, EquipamentoBase, JogadorPerfil, Habilidade, DescricaoHabilidade, Qualidade, Equipamento, Elixir, Arma, Armadura, Artefato, Poder, Personagem, Aprende
from .serializers import ArmaBaseSerializer, ArmaduraBaseSerializer, ArtefatoBaseSerializer, EquipamentoBaseSerializer, UsuarioCadastroSerializer, JogadorPerfilSerializer, HabilidadeSerializer, DescricaoHabilidadeSerializer, QualidadeSerializer, EquipamentoSerializer, ElixirSerializer, ArmaSerializer, ArmaduraSerializer, ArtefatoSerializer, PoderSerializer, PersonagemSerializer, AprendeSerializer, CustomTokenObtainPairSerializer

"""Uso do ModelViewSet transforma todas as views no que queremos, onde cada view dará acesso a o CRUD facilmente, ou seja, os ViewsSets irão herdar automaticamente todas as
operações REST padrão, ou seja, GET, POST, GET(por id), PUT/PATCH e DELETE"""

# Retorna somente o equipamento do usuário que fez a requisição, utilizando o filtro em todas as.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UsuarioCadastroViewSet(ModelViewSet):
    serializer_class = UsuarioCadastroSerializer
    http_method_names = ['post'] # Somente post para cadastro de usuário
    
class PersonagemScopedViewSet(ModelViewSet):
    queryset = None # Será definido em cada view que herda de PersonagemScopedViewSet
    
    def get_personagem(self):
        personagem_id = self.request.data.get('personagem') or self.request.query_params.get('personagem')
        if not personagem_id:
            raise ValidationError("ID do personagem é obrigatório.")
        try:
            return Personagem.objects.get(
                id=personagem_id,
                jogador__usuario=self.request.user
            )
        except Personagem.DoesNotExist:
            raise ValidationError("Personagem não encontrado.")

    def perform_create(self, serializer):
        serializer.save(personagem=self.get_personagem())

    def get_queryset(self):
        if self.queryset is None:
            return self.queryset
        return self.queryset.filter(personagem=self.get_personagem())

class JogadorPerfilViewSet(ModelViewSet):
    serializer_class = JogadorPerfilSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JogadorPerfil.objects.filter(usuario=self.request.user)

class PersonagemViewSet(ModelViewSet):
    queryset = Personagem.objects.all()
    serializer_class = PersonagemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Personagem.objects.filter(jogador__usuario=self.request.user)
    
class HabilidadeViewSet(ModelViewSet):
    queryset = Habilidade.objects.all()
    serializer_class = HabilidadeSerializer

class DescricaoHabilidadeViewSet(ModelViewSet):
    queryset = DescricaoHabilidade.objects.all()
    serializer_class = DescricaoHabilidadeSerializer

class QualidadeViewSet(ModelViewSet):
    queryset = Qualidade.objects.all()
    serializer_class = QualidadeSerializer

class EquipamentoBaseViewSet(ModelViewSet):
    queryset = EquipamentoBase.objects.all()
    serializer_class = EquipamentoBaseSerializer

class EquipamentoViewSet(PersonagemScopedViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    permission_classes = [IsAuthenticated]

class ElixirViewSet(PersonagemScopedViewSet):
    queryset = Elixir.objects.all()
    serializer_class = ElixirSerializer
    permission_classes = [IsAuthenticated]

class ArmaBaseViewSet(ModelViewSet):
    queryset = ArmaBase.objects.all()
    serializer_class = ArmaBaseSerializer

class ArmaViewSet(PersonagemScopedViewSet):
    serializer_class = ArmaSerializer
    queryset = Arma.objects.all()
    permission_classes = [IsAuthenticated]

class ArmaduraBaseViewSet(ModelViewSet):
    queryset = ArmaduraBase.objects.all()
    serializer_class = ArmaduraBaseSerializer

class ArmaduraViewSet(PersonagemScopedViewSet):
    serializer_class = ArmaduraSerializer
    queryset = Armadura.objects.all()
    permission_classes = [IsAuthenticated]

class ArtefatoBaseViewSet(ModelViewSet):
    queryset = ArtefatoBase.objects.all()
    serializer_class = ArtefatoBaseSerializer

class ArtefatoViewSet(PersonagemScopedViewSet):
    queryset = Artefato.objects.all()
    serializer_class = ArtefatoSerializer
    permission_classes = [IsAuthenticated]
    
class PoderViewSet(ModelViewSet):
    queryset = Poder.objects.all()
    serializer_class = PoderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Poder.objects.filter(
            artefato__personagem__jogador__usuario=self.request.user
        )
    
class AprendeViewSet(ModelViewSet):
    queryset = Aprende.objects.all()
    serializer_class = AprendeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Aprende.objects.filter(
            personagem__jogador__usuario=self.request.user
        )