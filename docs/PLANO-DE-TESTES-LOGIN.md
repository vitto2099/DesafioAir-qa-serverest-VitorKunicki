# 📋 Plano de Testes — Módulo de Login (`test_login.py`)

**Projeto:** ServeRest API — Automação de Testes  
**Arquivo de Teste:** `tests/test_login.py`  
**Endpoint Base:** `POST /login`  
**Data de Criação:** 2026-06-15  
**Autor:** Vitor Camargo Kunicki  

---

## 🎯 1. Objetivo

Validar o comportamento do endpoint `POST /login` da API ServeRest, cobrindo cenários de autenticação bem-sucedida, falhas por credenciais incorretas e validações de campos obrigatórios, garantindo que o sistema de autenticação retorne tokens e mensagens de erro corretos em todos os fluxos.

---

## 🛠️ 2. Pré-condições

- A API ServeRest deve estar acessível em `https://compassuol.serverest.dev`.
- As dependências do projeto devem estar instaladas (`pip install -r requirements.txt`).
- O ambiente Python deve estar configurado corretamente.
- A suíte utiliza dados dinâmicos (UUID) para garantir isolamento entre execuções.

---

## 📦 3. Escopo do Módulo

| Incluído | Excluído |
|---|---|
| Autenticação com credenciais válidas | Testes de performance/carga |
| Falha com senha inválida | Renovação/expiração de token |
| Falha com e-mail inexistente | Endpoints `/usuarios` e `/produtos` |
| Validação de campos em branco | Integração com outros módulos |
| Validação de contrato JSON (Schema) | |

---

## 📝 4. Casos de Teste

### CT-LOGIN-001 — Login com Credenciais Corretas

| Campo | Valor |
|---|---|
| **ID** | CT-LOGIN-001 |
| **Função de Teste** | `test_login_com_credenciais_corretas` |
| **Prioridade** | 🔴 Alta |
| **Tipo** | Funcional / Contrato |

**Pré-condição:** Cadastrar um usuário válido via `POST /usuarios` com `email_unico()` e senha `"minhasenha123"`.

**Passos:**
1. Gerar um e-mail único via `email_unico()`.
2. Cadastrar o usuário com `cadastrar_usuario(email=email, password="minhasenha123")`.
3. Chamar `fazer_login(email, "minhasenha123")`.
4. Validar a resposta contra o `SCHEMA_LOGIN_SUCESSO`.

**Resultado Esperado:**
- Status code: `200 OK`
- Corpo da resposta válido conforme `SCHEMA_LOGIN_SUCESSO` (contendo `message` e `authorization`).

**Critério de Aceite:** ✅ Passar na validação de schema + status 200.

---

### CT-LOGIN-002 — Login com Senha Errada

| Campo | Valor |
|---|---|
| **ID** | CT-LOGIN-002 |
| **Função de Teste** | `test_login_com_senha_errada` |
| **Prioridade** | 🔴 Alta |
| **Tipo** | Funcional / Negativo |

**Pré-condição:** Cadastrar um usuário válido com senha `"senha_correta"`.

**Passos:**
1. Gerar e-mail único e cadastrar usuário com senha `"senha_correta"`.
2. Chamar `fazer_login(email, "senha_errada")` com senha incorreta.
3. Verificar o status code da resposta.
4. Verificar a mensagem de erro no corpo da resposta.

**Resultado Esperado:**
- Status code: `401 Unauthorized`
- `body["message"]` == `"Email e/ou senha inválidos"`

**Critério de Aceite:** ✅ Status 401 + mensagem de erro correta.

---

### CT-LOGIN-003 — Login com E-mail Inexistente

| Campo | Valor |
|---|---|
| **ID** | CT-LOGIN-003 |
| **Função de Teste** | `test_login_com_email_inexistente` |
| **Prioridade** | 🔴 Alta |
| **Tipo** | Funcional / Negativo |

**Pré-condição:** Nenhum usuário precisa ser cadastrado. Usar e-mail gerado dinamicamente que não existe na base.

**Passos:**
1. Gerar um e-mail único via `email_unico()` (que nunca foi cadastrado).
2. Chamar `fazer_login(email_nao_cadastrado, "qualquersenha")`.
3. Verificar o status code da resposta.
4. Verificar a mensagem de erro no corpo da resposta.

**Resultado Esperado:**
- Status code: `401 Unauthorized`
- `body["message"]` == `"Email e/ou senha inválidos"`

**Critério de Aceite:** ✅ Status 401 + mensagem de erro correta.

---

### CT-LOGIN-004 — Login com Campos em Branco

| Campo | Valor |
|---|---|
| **ID** | CT-LOGIN-004 |
| **Função de Teste** | `test_login_com_campos_vazios` |
| **Prioridade** | 🟡 Média |
| **Tipo** | Validação / Negativo |

**Pré-condição:** Nenhuma. Teste independente.

**Passos (Subfluxo A — E-mail em branco):**
1. Chamar `fazer_login("", "senha123")`.
2. Verificar que o status code é `400`.
3. Verificar que a mensagem de erro menciona `"email não pode ficar em branco"`.

**Passos (Subfluxo B — Senha em branco):**
1. Chamar `fazer_login(email_unico(), "")`.
2. Verificar que o status code é `400`.
3. Verificar que a mensagem de erro menciona `"password não pode ficar em branco"`.

**Resultado Esperado:**
- Status code: `400 Bad Request` em ambos os subfluxos.
- Mensagem de erro correspondente ao campo em branco.

**Critério de Aceite:** ✅ Ambos os subfluxos retornam 400 com mensagens de validação corretas.

---

## 🏆 5. Critérios de Qualidade

| Critério | Descrição |
|---|---|
| **Cobertura** | Todos os 4 cenários devem ser executados e passar (exceto marcados como `xfail`) |
| **Asserções duplas** | Cada teste verifica status code E corpo da resposta |
| **Validação de Contrato** | CT-LOGIN-001 valida o schema JSON da resposta de sucesso |
| **Isolamento** | Dados criados por e-mails únicos (UUID) para evitar interferência entre testes |
| **Independência** | Nenhum teste depende do estado deixado por outro |

---

## 📊 6. Resumo de Cobertura

| ID | Cenário | Método | Status Esperado | Tipo |
|---|---|---|---|---|
| CT-LOGIN-001 | Credenciais corretas | POST /login | 200 | Positivo |
| CT-LOGIN-002 | Senha errada | POST /login | 401 | Negativo |
| CT-LOGIN-003 | E-mail inexistente | POST /login | 401 | Negativo |
| CT-LOGIN-004 | Campos em branco | POST /login | 400 | Validação |

**Total de casos:** 4 | **Positivos:** 1 | **Negativos:** 3
