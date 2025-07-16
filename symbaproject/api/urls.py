from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from .views import *

router = DefaultRouter() #Mapeia automaticamente baseado no prefixo, ou seja a rota primária. Com isso, GET /usuarios/<id>/ está ativo sem nenhuma configuração adicional.

## Autenticação e Cadastro
router.register(r'cadastro', UsuarioCadastroViewSet, basename='cadastro')
router.register(r'perfil-jogador', JogadorPerfilViewSet, basename='perfil-jogador')

## Personagens
router.register(r'personagens', PersonagemViewSet)

# Sistemas do RPG
router.register(r'habilidades', HabilidadeViewSet)
router.register(r'descricoes-habilidade', DescricaoHabilidadeViewSet)
router.register(r'qualidades', QualidadeViewSet)
router.register(r'equipamentos-base', EquipamentoBaseViewSet)
router.register(r'armas-base', ArmaBaseViewSet)
router.register(r'armaduras-base', ArmaduraBaseViewSet)
router.register(r'artefatos-base', ArtefatoBaseViewSet)

# Específicos pra cada Personagem
router.register(r'equipamentos', EquipamentoViewSet)
router.register(r'elixires', ElixirViewSet)
router.register(r'armas', ArmaViewSet)
router.register(r'armaduras', ArmaduraViewSet)
router.register(r'artefatos', ArtefatoViewSet)
router.register(r'poderes', PoderViewSet)
router.register(r'aprendizados', AprendeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Login e Refresh endpoints (JWT)
    path('auth/token/',CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
]
