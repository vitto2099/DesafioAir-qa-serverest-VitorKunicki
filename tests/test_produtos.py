import pytest
import requests
from jsonschema import validate
from tests.conftest import BASE_URL, cadastrar_produto, email_unico, cadastrar_usuario, fazer_login
from tests.schemas import SCHEMA_LISTAR_PRODUTOS


def test_listar_produtos_retorna_200():
    resposta = requests.get(f"{BASE_URL}/produtos")
    assert resposta.status_code == 200
    corpo = resposta.json()
    
    validate(instance=corpo, schema=SCHEMA_LISTAR_PRODUTOS)


def test_cadastrar_produto_com_token_admin(token_admin):
    resposta = cadastrar_produto(token_admin)
    corpo = resposta.json()
    
    assert resposta.status_code == 201
    assert corpo["message"] == "Cadastro realizado com sucesso"
    assert "_id" in corpo


def test_cadastrar_produto_sem_token_admin():
    email = email_unico()
    senha = "senha123"
    cadastrar_usuario(email=email, password=senha, administrador="false")
    token_comum = fazer_login(email, senha).json()["authorization"]
    
    resposta = cadastrar_produto(token_comum)
    assert resposta.status_code == 403
    assert resposta.json()["message"] == "Rota exclusiva para administradores"


def test_cadastrar_produto_token_ausente():
    payload = {
        "nome": "Produto sem token",
        "preco": 100,
        "descricao": "Desc",
        "quantidade": 1
    }
    resposta = requests.post(f"{BASE_URL}/produtos", json=payload)
    assert resposta.status_code == 401
    assert resposta.json()["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


def test_buscar_produto_por_id_existente(token_admin):
    resposta_cadastro = cadastrar_produto(token_admin)
    id_produto = resposta_cadastro.json()["_id"]
    
    resposta_busca = requests.get(f"{BASE_URL}/produtos/{id_produto}")
    assert resposta_busca.status_code == 200
    assert resposta_busca.json()["_id"] == id_produto


def test_buscar_produto_por_id_inexistente():
    resposta = requests.get(f"{BASE_URL}/produtos/id_que_nao_existe_123")
    assert resposta.status_code == 400
    assert resposta.json()["message"] == "Produto não encontrado"


def test_atualizar_produto_existente(token_admin):
    resposta_cadastro = cadastrar_produto(token_admin)
    id_produto = resposta_cadastro.json()["_id"]
    
    payload_atualizado = {
        "nome": f"Produto Atualizado {id_produto}",
        "preco": 250,
        "descricao": "Nova desc",
        "quantidade": 20
    }
    headers = {"Authorization": token_admin}
    
    resposta_atualizacao = requests.put(f"{BASE_URL}/produtos/{id_produto}", json=payload_atualizado, headers=headers)
    assert resposta_atualizacao.status_code == 200
    assert resposta_atualizacao.json()["message"] == "Registro alterado com sucesso"


@pytest.mark.xfail(reason="Bug na ServeRest: retorna 'Nenhum registro excluído' mesmo para produto existente")
def test_excluir_produto_existente(token_admin):
    resposta_cadastro = cadastrar_produto(token_admin)
    id_produto = resposta_cadastro.json()["_id"]
    
    headers = {"Authorization": token_admin}
    resposta_exclusao = requests.delete(f"{BASE_URL}/produtos/{id_produto}", headers=headers)
    
    assert resposta_exclusao.status_code == 200
    assert resposta_exclusao.json()["message"] == "Registro excluído com sucesso"
