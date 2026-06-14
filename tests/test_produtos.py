import pytest
import requests
from jsonschema import validate
from conftest import BASE_URL, cadastrar_produto, email_unico, cadastrar_usuario, fazer_login
from schemas import SCHEMA_LISTAR_PRODUTOS, SCHEMA_CADASTRO_PRODUTO_SUCESSO, SCHEMA_PRODUTO_DETALHE


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
    
    validate(instance=corpo, schema=SCHEMA_CADASTRO_PRODUTO_SUCESSO)


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
    
    validate(instance=resposta_busca.json(), schema=SCHEMA_PRODUTO_DETALHE)


def test_buscar_produto_por_id_inexistente():
    resposta = requests.get(f"{BASE_URL}/produtos/0000000000000000")
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


def test_excluir_produto_sem_token_admin(token_admin):
    resposta_cadastro = cadastrar_produto(token_admin)
    id_produto = resposta_cadastro.json()["_id"]
    
    email = email_unico()
    senha = "senha123"
    cadastrar_usuario(email=email, password=senha, administrador="false")
    token_comum = fazer_login(email, senha).json()["authorization"]
    
    headers = {"Authorization": token_comum}
    resposta_exclusao = requests.delete(f"{BASE_URL}/produtos/{id_produto}", headers=headers)
    
    assert resposta_exclusao.status_code == 403
    assert resposta_exclusao.json()["message"] == "Rota exclusiva para administradores"


def test_cadastrar_produto_com_nome_duplicado(token_admin):
    nome_produto = f"Produto Repetido {email_unico()}"
    
    # Primeiro cadastro
    cadastrar_produto(token_admin, nome=nome_produto)
    
    # Segundo cadastro com o mesmo nome
    resposta_duplicada = cadastrar_produto(token_admin, nome=nome_produto)
    assert resposta_duplicada.status_code == 400
    assert resposta_duplicada.json()["message"] == "Já existe produto com esse nome"


def test_cadastrar_produto_valores_invalidos(token_admin):
    # Enviar preço negativo e quantidade string/negativa
    payload = {
        "nome": f"Produto Invalido {email_unico()}",
        "preco": -50,
        "descricao": "Descricao",
        "quantidade": -5
    }
    headers = {"Authorization": token_admin}
    resposta = requests.post(f"{BASE_URL}/produtos", json=payload, headers=headers)
    
    # ServeRest retorna 400 Bad Request se houver validação de inteiros positivos
    assert resposta.status_code == 400
    corpo = resposta.json()
    assert "preco deve ser um número positivo" in corpo.get("preco", "") or "preco deve ser maior ou igual a 0" in corpo.get("preco", "") or "quantidade deve ser maior ou igual a 0" in corpo.get("quantidade", "")


def test_atualizar_produto_inexistente_cria_novo(token_admin):
    id_inexistente = "0000000000000000"
    payload = {
        "nome": f"Produto Criado no Put {email_unico()}",
        "preco": 300,
        "descricao": "Produto cadastrado via PUT",
        "quantidade": 15
    }
    headers = {"Authorization": token_admin}
    resposta = requests.put(f"{BASE_URL}/produtos/{id_inexistente}", json=payload, headers=headers)
    
    assert resposta.status_code == 201
    assert resposta.json()["message"] == "Cadastro realizado com sucesso"


def test_excluir_produto_token_ausente(token_admin):
    resposta_cadastro = cadastrar_produto(token_admin)
    id_produto = resposta_cadastro.json()["_id"]
    
    resposta_exclusao = requests.delete(f"{BASE_URL}/produtos/{id_produto}")
    assert resposta_exclusao.status_code == 401
    assert resposta_exclusao.json()["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


