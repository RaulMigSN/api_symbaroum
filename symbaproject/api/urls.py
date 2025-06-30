from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
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
]
