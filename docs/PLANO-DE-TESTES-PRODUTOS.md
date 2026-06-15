# 📋 Plano de Testes — Módulo de Produtos (`test_produtos.py`)
---

## 🎯 1. Objetivo

Validar o comportamento completo do CRUD do endpoint `/produtos` da API ServeRest, cobrindo operações de listagem, cadastro, busca, atualização e exclusão de produtos. Também são verificados os controles de acesso (token de administrador vs. usuário comum vs. sem token), validações de regras de negócio e um bug documentado no endpoint de exclusão.

---

## 🛠️ 2. Pré-condições

- A API ServeRest deve estar acessível em `https://compassuol.serverest.dev`.
- As dependências do projeto devem estar instaladas (`pip install -r requirements.txt`).
- A fixture `token_admin` (definida em `conftest.py`) deve criar um usuário administrador e retornar seu token Bearer.
- A suíte utiliza dados dinâmicos (UUID) para garantir isolamento entre execuções.

---

## 📦 3. Escopo do Módulo

| Incluído | Excluído |
|---|---|
| Listagem de produtos com validação de schema | Testes de performance/carga |
| Cadastro com token de admin | Rota `/carrinhos` |
| Bloqueio por falta de permissão de admin | Testes de segurança avançados |
| Bloqueio por ausência de token | |
| Busca de produto por ID (existente e inexistente) | |
| Atualização de produto existente | |
| Cadastro via PUT com ID inexistente | |
| Exclusão com token admin | |
| Bloqueio de exclusão por usuário comum | |
| Bloqueio de exclusão sem token | |
| Cadastro de produto com nome duplicado | |
| Cadastro com valores inválidos (negativos) | |

---

## 📝 4. Casos de Teste

### CT-PROD-001 — Listar Produtos retorna Status 200

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-001 |
| **Função de Teste** | `test_listar_produtos_retorna_200` |
| **Prioridade** | 🔴 Alta |
| **Tipo** | Funcional / Contrato |

**Pré-condição:** Nenhuma. Endpoint público.

**Passos:**
1. Fazer `GET /produtos` sem autenticação.
2. Verificar o status code.
3. Validar o corpo da resposta contra `SCHEMA_LISTAR_PRODUTOS`.

**Resultado Esperado:**
- Status code: `200 OK`
- Corpo válido conforme `SCHEMA_LISTAR_PRODUTOS` (contendo `quantidade` e `produtos`).

**Critério de Aceite:** ✅ Status 200 + schema válido.

---

### CT-PROD-002 — Cadastrar Produto com Token de Administrador

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-002 |
| **Função de Teste** | `test_cadastrar_produto_com_token_admin` |
| **Prioridade** | 🔴 Alta |
| **Tipo** | Funcional / Positivo |
| **Fixture** | `token_admin` |

**Pré-condição:** Fixture `token_admin` deve fornecer um token Bearer válido de administrador.

**Passos:**
1. Chamar `cadastrar_produto(token_admin)` com dados gerados automaticamente.
2. Verificar o status code da resposta.
3. Verificar a mensagem de sucesso e a presença de `_id`.
4. Validar o corpo contra `SCHEMA_CADASTRO_PRODUTO_SUCESSO`.

**Resultado Esperado:**
- Status code: `201 Created`
- `body["message"]` == `"Cadastro realizado com sucesso"`
- `"_id"` presente no corpo
- Schema JSON válido.

**Critério de Aceite:** ✅ Status 201 + mensagem + `_id` + schema válido.

---

### CT-PROD-003 — Bloquear Cadastro sem Permissão de Administrador

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-003 |
| **Função de Teste** | `test_cadastrar_produto_sem_token_admin` |
| **Prioridade** | 🔴 Alta |
| **Tipo** | Controle de Acesso / Negativo |

**Pré-condição:** Cadastrar um usuário com `administrador="false"` e obter seu token.

**Passos:**
1. Cadastrar usuário comum com `administrador="false"`.
2. Fazer login e obter `token_comum`.
3. Tentar `POST /produtos` com `token_comum`.
4. Verificar status e mensagem de erro.

**Resultado Esperado:**
- Status code: `403 Forbidden`
- `body["message"]` == `"Rota exclusiva para administradores"`

**Critério de Aceite:** ✅ Status 403 + mensagem de acesso negado.

---

### CT-PROD-004 — Bloquear Cadastro sem Token de Autorização

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-004 |
| **Função de Teste** | `test_cadastrar_produto_token_ausente` |
| **Prioridade** | 🔴 Alta |
| **Tipo** | Controle de Acesso / Negativo |

**Pré-condição:** Nenhuma.

**Passos:**
1. Fazer `POST /produtos` com payload válido, mas sem header `Authorization`.
2. Verificar o status code e a mensagem de erro.

**Resultado Esperado:**
- Status code: `401 Unauthorized`
- `body["message"]` == `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"`

**Critério de Aceite:** ✅ Status 401 + mensagem de token ausente.

---

### CT-PROD-005 — Buscar Produto por ID Existente

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-005 |
| **Função de Teste** | `test_buscar_produto_por_id_existente` |
| **Prioridade** | 🟡 Média |
| **Tipo** | Funcional / Contrato |
| **Fixture** | `token_admin` |

**Pré-condição:** Produto deve ser cadastrado previamente via fixture.

**Passos:**
1. Cadastrar produto e extrair `_id` da resposta.
2. Fazer `GET /produtos/{_id}`.
3. Verificar status code e confirmar que o `_id` retornado é o mesmo.
4. Validar corpo contra `SCHEMA_PRODUTO_DETALHE`.

**Resultado Esperado:**
- Status code: `200 OK`
- `body["_id"]` == ID do produto cadastrado
- Schema JSON válido.

**Critério de Aceite:** ✅ Status 200 + ID correto + schema válido.

---

### CT-PROD-006 — Buscar Produto por ID Inexistente

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-006 |
| **Função de Teste** | `test_buscar_produto_por_id_inexistente` |
| **Prioridade** | 🟡 Média |
| **Tipo** | Funcional / Negativo |

**Pré-condição:** Nenhuma.

**Passos:**
1. Fazer `GET /produtos/0000000000000000` (ID de 16 zeros, inexistente).
2. Verificar o status code e a mensagem de erro.

**Resultado Esperado:**
- Status code: `400 Bad Request`
- `body["message"]` == `"Produto não encontrado"`

**Critério de Aceite:** ✅ Status 400 + mensagem de não encontrado.

---

### CT-PROD-007 — Atualizar Produto Existente

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-007 |
| **Função de Teste** | `test_atualizar_produto_existente` |
| **Prioridade** | 🔴 Alta |
| **Tipo** | Funcional / Positivo |
| **Fixture** | `token_admin` |

**Pré-condição:** Produto deve ser cadastrado previamente.

**Passos:**
1. Cadastrar produto e extrair `_id`.
2. Fazer `PUT /produtos/{_id}` com payload atualizado e token de admin.
3. Verificar status code e mensagem de sucesso.

**Resultado Esperado:**
- Status code: `200 OK`
- `body["message"]` == `"Registro alterado com sucesso"`

**Critério de Aceite:** ✅ Status 200 + mensagem de alteração com sucesso.

---

### CT-PROD-008 — Excluir Produto Existente ⚠️ XFAIL (Bug Documentado)

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-008 |
| **Função de Teste** | `test_excluir_produto_existente` |
| **Prioridade** | 🔴 Alta |
| **Tipo** | Funcional / Bug Documentado |
| **Fixture** | `token_admin` |
| **Marcação** | `@pytest.mark.xfail` |

> ⚠️ **ATENÇÃO:** Este teste está marcado como `xfail` devido a um **bug confirmado na API ServeRest**. Ver `BUG-REPORT.md` para detalhes completos.

**Pré-condição:** Produto cadastrado previamente com token admin.

**Passos:**
1. Cadastrar produto e extrair `_id`.
2. Fazer `DELETE /produtos/{_id}` com token de admin.
3. Verificar status code e mensagem de exclusão.

**Resultado Esperado (correto, quando bug for corrigido):**
- Status code: `200 OK`
- `body["message"]` == `"Registro excluído com sucesso"`

**Comportamento Atual (bugado):**
- Status code: `200 OK`
- `body["message"]` == `"Nenhum registro excluído"` ← **BUG**

**Critério de Aceite:** ✅ Teste marcado como xfail passa enquanto o bug existir. Deve ser removido do xfail quando o bug for corrigido.

---

### CT-PROD-009 — Bloquear Exclusão por Usuário Não-Administrador

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-009 |
| **Função de Teste** | `test_excluir_produto_sem_token_admin` |
| **Prioridade** | 🔴 Alta |
| **Tipo** | Controle de Acesso / Negativo |
| **Fixture** | `token_admin` |

**Pré-condição:** Produto cadastrado com admin. Usuário comum criado separadamente.

**Passos:**
1. Cadastrar produto com `token_admin` e extrair `_id`.
2. Criar usuário comum e obter `token_comum`.
3. Fazer `DELETE /produtos/{_id}` com `token_comum`.
4. Verificar status code e mensagem.

**Resultado Esperado:**
- Status code: `403 Forbidden`
- `body["message"]` == `"Rota exclusiva para administradores"`

**Critério de Aceite:** ✅ Status 403 + mensagem de acesso negado.

---

### CT-PROD-010 — Bloquear Cadastro de Produto com Nome Duplicado

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-010 |
| **Função de Teste** | `test_cadastrar_produto_com_nome_duplicado` |
| **Prioridade** | 🟡 Média |
| **Tipo** | Validação de Regra de Negócio / Negativo |
| **Fixture** | `token_admin` |

**Pré-condição:** Token de admin disponível.

**Passos:**
1. Definir `nome_produto` único.
2. Cadastrar produto com esse nome (1ª vez) — deve retornar 201.
3. Tentar cadastrar produto com o **mesmo nome** (2ª vez).
4. Verificar status code e mensagem de erro.

**Resultado Esperado:**
- Status code: `400 Bad Request`
- `body["message"]` == `"Já existe produto com esse nome"`

**Critério de Aceite:** ✅ Status 400 + mensagem de duplicidade.

---

### CT-PROD-011 — Bloquear Cadastro com Valores Inválidos (Negativos)

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-011 |
| **Função de Teste** | `test_cadastrar_produto_valores_invalidos` |
| **Prioridade** | 🟡 Média |
| **Tipo** | Validação / Negativo |
| **Fixture** | `token_admin` |

**Pré-condição:** Token de admin disponível.

**Passos:**
1. Montar payload com `preco: -50` e `quantidade: -5`.
2. Fazer `POST /produtos` com token admin e payload inválido.
3. Verificar que a API rejeita a requisição.

**Resultado Esperado:**
- Status code: `400 Bad Request`
- Corpo contendo mensagem de validação de `preco` ou `quantidade`.

**Critério de Aceite:** ✅ Status 400 + ao menos uma mensagem de validação de campo numérico.

---

### CT-PROD-012 — Cadastrar Novo Produto via PUT com ID Inexistente

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-012 |
| **Função de Teste** | `test_atualizar_produto_inexistente_cria_novo` |
| **Prioridade** | 🟡 Média |
| **Tipo** | Funcional / Comportamento de Upsert |
| **Fixture** | `token_admin` |

**Pré-condição:** Token de admin disponível.

**Passos:**
1. Fazer `PUT /produtos/0000000000000000` com payload de novo produto e token admin.
2. Verificar que a API cria o produto (upsert).

**Resultado Esperado:**
- Status code: `201 Created`
- `body["message"]` == `"Cadastro realizado com sucesso"`

**Critério de Aceite:** ✅ Status 201 + mensagem de cadastro realizado.

---

### CT-PROD-013 — Bloquear Exclusão de Produto sem Token

| Campo | Valor |
|---|---|
| **ID** | CT-PROD-013 |
| **Função de Teste** | `test_excluir_produto_token_ausente` |
| **Prioridade** | 🔴 Alta |
| **Tipo** | Controle de Acesso / Negativo |
| **Fixture** | `token_admin` |

**Pré-condição:** Produto cadastrado com admin.

**Passos:**
1. Cadastrar produto e extrair `_id`.
2. Fazer `DELETE /produtos/{_id}` **sem** header `Authorization`.
3. Verificar status code e mensagem de erro.

**Resultado Esperado:**
- Status code: `401 Unauthorized`
- `body["message"]` == `"Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"`

**Critério de Aceite:** ✅ Status 401 + mensagem de token ausente.

---

## 🏆 5. Critérios de Qualidade

| Critério | Descrição |
|---|---|
| **Cobertura** | Todos os 13 cenários executados (CT-PROD-008 pode falhar por xfail esperado) |
| **Asserções duplas** | Cada teste verifica status code E corpo da resposta |
| **Validação de Contrato** | CT-PROD-001, CT-PROD-002, CT-PROD-005 validam schema JSON |
| **Controle de Acesso** | Cenários 003, 004, 009, 013 cobrem todos os perfis de autorização |
| **Isolamento** | Produtos e usuários criados com dados únicos (UUID) por execução |
| **Fixture com Teardown** | `token_admin` faz limpeza do usuário admin após cada teste |

---

## 📊 6. Resumo de Cobertura

| ID | Cenário | Método | Endpoint | Status Esperado | Tipo |
|---|---|---|---|---|---|
| CT-PROD-001 | Listar produtos | GET | /produtos | 200 | Positivo |
| CT-PROD-002 | Cadastrar com admin | POST | /produtos | 201 | Positivo |
| CT-PROD-003 | Cadastrar sem admin | POST | /produtos | 403 | Negativo |
| CT-PROD-004 | Cadastrar sem token | POST | /produtos | 401 | Negativo |
| CT-PROD-005 | Buscar por ID existente | GET | /produtos/{id} | 200 | Positivo |
| CT-PROD-006 | Buscar por ID inexistente | GET | /produtos/{id} | 400 | Negativo |
| CT-PROD-007 | Atualizar existente | PUT | /produtos/{id} | 200 | Positivo |
| CT-PROD-008 | Excluir existente (bug) | DELETE | /produtos/{id} | 200 | XFAIL |
| CT-PROD-009 | Excluir sem admin | DELETE | /produtos/{id} | 403 | Negativo |
| CT-PROD-010 | Nome duplicado | POST | /produtos | 400 | Negativo |
| CT-PROD-011 | Valores negativos | POST | /produtos | 400 | Negativo |
| CT-PROD-012 | PUT com ID inexistente | PUT | /produtos/{id} | 201 | Positivo |
| CT-PROD-013 | Excluir sem token | DELETE | /produtos/{id} | 401 | Negativo |

**Total de casos:** 13 | **Positivos:** 5 | **Negativos:** 7 | **XFAIL:** 1
