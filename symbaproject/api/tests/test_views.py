import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import Usuario, JogadorPerfil

@pytest.mark.django_db
def test_cadastro_usuario():
    client = APIClient()
    url = reverse("cadastro-list")
    response = client.post(url, {
        "login": "novo_user",
        "email": "novo@exemplo.com",
        "senha": "senha123",
        "confirmar_senha": "senha123",
        "tipo": "JOGADOR"
    })
    assert response.status_code == 201
    assert response.data["login"] == "novo_user"


@pytest.mark.django_db
def test_criar_e_listar_personagem():
    # Criar o usuário primeiro
    usuario = Usuario.objects.create_user(
        login="testuser",
        email="testuser@example.com",
        senha="testpassword",
    )
    # Criar o perfil do jogador
    perfil = JogadorPerfil.objects.create(
        usuario=usuario,
        biografia="Biografia do Jogador etc etc...",
    )

    # Autenticação e obter o token
    client = APIClient()
    url_login = reverse("token_obtain_pair")
    resp = client.post(url_login, {"login": "testuser", "password": "testpassword"})
    assert resp.status_code == 200
    token = resp.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    #Criação do personagem
    url_personagem = reverse("personagem-list")
    data = {
        "jogador": perfil.id,
        "nome": "Personagem Teste",
        "idade": 20,
        "sexo": "M",
        "altura": 1.75,
        "peso": 70,
        "raca": "HA",
        "ocupacao": "Guerreiro",
        "nivel": 1,
        "experiencia": 0,
        "vitalidade_atual": 8,
        "vitalidade_maxima": 8,
        "limiar_de_dor": 4,
        "corrupcao_permanente": 0,
        "corrupcao_temporaria": 0,
        "limiar_de_corrupcao": 4,
        "sombra": "Sombra do Personagem Teste",
        "citacao": "Citacao do Personagem Teste",

        # Atributos
        "astuto": 10,
        "discreto": 10,
        "persuasivo": 10,
        "preciso": 10,
        "rapido": 10,
        "resoluto": 10,
        "vigilante": 10,
        "vigoroso": 10,
    }

    resp = client.post(url_personagem, data)
    assert resp.status_code == 201
    assert resp.data["nome"] == "Personagem Teste"

    # Listagem dos personagens
    resp = client.get(url_personagem)
    assert resp.status_code == 200
    assert any(p["nome"] == "Personagem Teste" for p in resp.data)