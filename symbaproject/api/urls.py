from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from .views import *

router = DefaultRouter() #Mapeia automaticamente baseado no prefixo, ou seja a rota primária. Com isso, GET /usuarios/<id>/ está ativo sem nenhuma configuração adicional.
router.register(r'usuarios', UsuarioViewSet)
router.register(r'jogadores', JogadorViewSet)
router.register(r'personagens', PersonagemViewSet)
router.register(r'habilidades', HabilidadeViewSet)
router.register(r'descricoes-habilidade', DescricaoHabilidadeViewSet)
router.register(r'qualidades', QualidadeViewSet)
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
    path('token/',CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
]
