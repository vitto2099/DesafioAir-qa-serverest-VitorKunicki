# Bug Report: Falha ao excluir produto recém-cadastrado

**Título:** O endpoint `DELETE /produtos/{id}` retorna mensagem "Nenhum registro excluído" ao tentar deletar um produto válido.

**Severidade:** Media (Tem retorno ambíguo, apesar do status code ser 200).

**Passos para reproduzir:**
1. Realizar login com usuário Administrador para obter o token de acesso.
2. Realizar POST em `/produtos` passando o token, informando os dados do produto.
3. Extrair o `_id` do produto criado a partir da resposta (ex: 201 Created).
4. Realizar DELETE em `/produtos/{id}` passando o token de administrador.

**Comportamento Esperado:**
O endpoint deveria retornar um Status Code `200 OK` com a mensagem `"Registro excluído com sucesso"`.

**Comportamento Obtido:**
O endpoint retorna Status Code `200 OK`, mas a mensagem retornada é `"Nenhum registro excluído"`.

**Evidências:**
```json
{
    "message": "Nenhum registro excluído"
}
```
*Erro ocorrido no teste automatizado `test_excluir_produto_existente` no arquivo `tests/test_produtos.py`.*
