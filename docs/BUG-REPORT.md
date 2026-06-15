# 🐛 Bug Report — ServeRest API

---

## Sumário de Bugs Identificados

| ID | Título Resumido | Severidade | Status | Endpoint |
|---|---|---|---|---|
| BUG-01 | Testes de usuários apresentam instabilidade (RERUN automático) | 🟡 Média | 🔴 Aberto | `PUT /usuarios/{id}`, `POST /usuarios`, `DELETE /usuarios/{id}` |
| BUG-02 | Senha retornada em texto puro nas respostas da API de usuários | 🔴 Alta | 🔴 Aberto | `GET /usuarios`, `GET /usuarios/{id}`, `POST /usuarios`, `DELETE /usuarios/{id}` |

---

## BUG-01 — Instabilidade em Testes de Usuários (RERUN automático)

| Campo | Valor |
|---|---|
| **ID** | BUG-01 |
| **Título** | Três testes de usuários falham na primeira tentativa e necessitam de reexecução automática (RERUN) |
| **Severidade** | 🟡 Média |
| **Prioridade** | 🔴 Alta |
| **Status** | 🔴 Aberto |
| **Ambiente** | `https://compassuol.serverest.dev` |
| **Endpoints Afetados** | `PUT /usuarios/{id}`, `POST /usuarios`, `DELETE /usuarios/{id}` |
| **Arquivo de Teste** | Testes individuais em `tests/` |
| **Tipo de Resultado** | `RERUN` (retry automático ativado) |

---

### 📋 Contexto

Na execução completa da suíte (salva em `test_output.txt`), três testes de usuários precisaram de **reexecução automática** (RERUN), configurada pelo plugin `pytest-rerunfailures`. Isso indica que os testes **falharam na primeira tentativa** mas passaram na reexecução, caracterizando testes **flaky** (instáveis).

---

### 🔄 Testes que Geraram RERUN

```
tests/test_atualizar_usuario_com_sucesso.py::test_atualizar_usuario_com_sucesso  RERUN
tests/test_atualizar_usuario_com_sucesso.py::test_atualizar_usuario_com_sucesso  PASSED

tests/test_cadastrar_usuario_sem_campo_email.py::test_cadastrar_usuario_sem_campo_email  RERUN
tests/test_cadastrar_usuario_sem_campo_email.py::test_cadastrar_usuario_sem_campo_email  PASSED

tests/test_excluir_usuario_com_sucesso.py::test_excluir_usuario_com_sucesso  RERUN
tests/test_excluir_usuario_com_sucesso.py::test_excluir_usuario_com_sucesso  PASSED
```

---

### 🔍 Análise das Possibilidades

| Hipótese | Descrição |
|---|---|
| **A) Latência / Timeout de rede** | A API pública `compassuol.serverest.dev` apresenta picos de latência que causam timeout ou resposta lenta na primeira chamada. |
| **B) Instabilidade do servidor** | O servidor da ServeRest pode estar reiniciando ou sobrecarregado durante a execução dos testes. |
| **C) Race Condition** | Operações como `PUT /usuarios/{id}` podem ter uma janela de inconsistência logo após o cadastro (`POST /usuarios`), retornando 404 na primeira tentativa. |
| **D) Estado compartilhado** | Dados residuais de testes anteriores interferem com o estado esperado. |

---

### 📊 Padrão dos Endpoints Afetados

| Teste | Endpoint | Verbo | Operação |
|---|---|---|---|
| `test_atualizar_usuario_com_sucesso` | `/usuarios/{id}` | PUT | Atualizar usuário existente |
| `test_cadastrar_usuario_sem_campo_email` | `/usuarios` | POST | Validar campo obrigatório |
| `test_excluir_usuario_com_sucesso` | `/usuarios/{id}` | DELETE | Excluir usuário existente |

---

### 💡 Impacto

- **Confiabilidade da suíte:** Testes flaky geram desconfiança nos resultados — uma falha real pode ser ignorada como "instabilidade conhecida".
- **CI/CD:** Em pipelines sem `rerunfailures`, esses testes **quebrariam o build** desnecessariamente.
- **Tempo de execução:** O RERUN aumenta o tempo total da suíte.

---

### 🔧 Ação Recomendada

1. **Investigar logs de falha** — rodar com `--tb=long` e capturar o erro exato da primeira tentativa:
   ```bash
   python -m pytest tests/test_atualizar_usuario_com_sucesso.py tests/test_cadastrar_usuario_sem_campo_email.py tests/test_excluir_usuario_com_sucesso.py -v --tb=long -p no:rerunfailures
   ```

2. **Adicionar timeout explícito** nas chamadas `requests` do `conftest.py`:
   ```python
   # Exemplo: adicionar timeout de 10 segundos em todas as requisições
   return requests.post(f"{BASE_URL}/usuarios", json=payload, timeout=10)
   ```

3. **Avaliar se o `rerunfailures` é necessário** — se a causa for latência de rede na API pública, manter o plugin é justificado. Se for problema de isolamento de testes, corrigir o root cause.

4. **Monitorar** se os mesmos três testes continuam sendo os únicos com RERUN ou se o padrão se expande.

---

## BUG-02 — Senha Retornada em Texto Puro nas Respostas de Usuários

| Campo | Valor |
|---|---|
| **ID** | BUG-02 |
| **Título** | Campo `password` exposto em texto puro nas respostas da API de usuários |
| **Severidade** | 🔴 Alta |
| **Prioridade** | 🔴 Alta |
| **Status** | 🔴 Aberto |
| **Ambiente** | `https://compassuol.serverest.dev` |
| **Endpoints Afetados** | `GET /usuarios`, `GET /usuarios/{id}`, `POST /usuarios`, `DELETE /usuarios/{id}` |
| **Tipo** | Vulnerabilidade de Segurança — Exposição de Dados Sensíveis (CWE-312) |

---

### 📋 Contexto

A API ServeRest retorna o campo `password` em **texto puro (plaintext)** em todas as respostas que envolvem dados de usuários. Isso significa que qualquer pessoa com acesso às respostas da API — incluindo logs, proxies, ferramentas de monitoramento ou ataques man-in-the-middle — pode obter as senhas dos usuários sem nenhum esforço.

---

### 🔬 Reprodução

**Requisição:**
```http
GET https://compassuol.serverest.dev/usuarios
```

**Resposta atual (comportamento incorreto):**
```json
{
  "quantidade": 1,
  "usuarios": [
    {
      "nome": "Fulano da Silva",
      "email": "beltrano@qa.com.br",
      "password": "teste",
      "administrador": "true",
      "_id": "0uxuPY0cbmQhpEz1"
    }
  ]
}
```

> ⚠️ O campo `"password": "teste"` é retornado em **texto puro** na resposta.

O mesmo comportamento ocorre em:
- `GET /usuarios/{id}` — busca individual de usuário
- `POST /usuarios` (via corpo de requisição que é refletido no response)
- `DELETE /usuarios/{id}` (campo `password` visível no payload do body request que fica em logs)

---

### ✅ Comportamento Esperado (correto)

O campo `password` **nunca** deve ser retornado nas respostas da API. A resposta correta deveria ser:

```json
{
  "quantidade": 1,
  "usuarios": [
    {
      "nome": "Fulano da Silva",
      "email": "beltrano@qa.com.br",
      "administrador": "true",
      "_id": "0uxuPY0cbmQhpEz1"
    }
  ]
}
```

Alternativamente, se a senha precisar ser armazenada, ela deveria ser **hasheada** (ex: bcrypt) antes de ser persistida e **nunca exposta** na resposta.

---

### 💡 Impacto

| Risco | Descrição |
|---|---|
| **Exposição de credenciais** | Qualquer requisição `GET /usuarios` expõe senhas de **todos** os usuários cadastrados |
| **Reutilização de senhas** | Usuários costumam reutilizar senhas — a exposição pode comprometer outras contas (e-mail, redes sociais, etc.) |
| **Conformidade LGPD/GDPR** | Dados de autenticação são dados sensíveis — a exposição viola regulamentos de proteção de dados |
| **Ataques de escalada de privilégio** | Um usuário comum pode listar todos os usuários e obter a senha de um administrador |

---

### 🔧 Ação Recomendada

1. **Nunca retornar o campo `password`** nas respostas de listagem ou busca de usuários.
2. **Implementar hashing** de senhas no armazenamento (ex: `bcrypt`, `argon2`).
3. **Adicionar teste automatizado** para verificar que o campo `password` **não está presente** nas respostas:

```python
# Teste sugerido: verificar que password NÃO aparece na resposta
def test_listagem_usuarios_nao_expoe_senha():
    resposta = requests.get(f"{BASE_URL}/usuarios")
    assert resposta.status_code == 200
    usuarios = resposta.json()["usuarios"]
    for usuario in usuarios:
        assert "password" not in usuario, "BUG-02: Senha exposta em texto puro na listagem de usuários!"

def test_buscar_usuario_por_id_nao_expoe_senha(usuario_id):
    resposta = requests.get(f"{BASE_URL}/usuarios/{usuario_id}")
    assert resposta.status_code == 200
    assert "password" not in resposta.json(), "BUG-02: Senha exposta em texto puro na busca por ID!"
```

---

## 📊 Resumo Executivo

| ID | Endpoint | Resultado na Execução | Causa Provável | Ação |
|---|---|---|---|---|
| BUG-01 | `PUT`, `POST`, `DELETE /usuarios/{id}` | RERUN (x3) | Instabilidade de rede / race condition | Investigar com `--tb=long`, adicionar timeout |
| BUG-02 | `GET /usuarios`, `GET /usuarios/{id}` | Campo `password` exposto em plaintext | Falta de sanitização da resposta / ausência de hashing | Remover `password` das respostas; implementar hashing |

**Resultado Geral da Última Execução:** `16 passed, 1 xpassed` em `21.19s`
