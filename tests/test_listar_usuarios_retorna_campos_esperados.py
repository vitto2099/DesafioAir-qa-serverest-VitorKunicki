import requests
from jsonschema import validate
from tests.conftest import BASE_URL
from tests.schemas import SCHEMA_LISTAR_USUARIOS


def test_listar_usuarios_retorna_campos_esperados():
    resposta = requests.get(f"{BASE_URL}/usuarios")
    corpo = resposta.json()
    
    validate(instance=corpo, schema=SCHEMA_LISTAR_USUARIOS)
