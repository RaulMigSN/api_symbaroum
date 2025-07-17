import pytest
from api.models import *

@pytest.mark.django_db
def test_usuario_model():
    usuario = Usuario.objects.create_user(
        login="testuser",
        email="testuser@example.com",
        senha="testpassword"
    )
    assert usuario.login == "testuser"
    assert usuario.email == "testuser@example.com"
    assert usuario.check_password("testpassword")

