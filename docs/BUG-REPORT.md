# 🐛 Bug Report — ServeRest API

---

## Sumário de Bugs Identificados

| ID | Título Resumido | Severidade | Status | Endpoint |
|---|---|---|---|---|
| BUG-01 | `DELETE /produtos/{id}` — teste marcado como `xfail` passou inesperadamente (XPASS) | 🟡 Média | 🟠 Requer Ação | `DELETE /produtos/{id}` |
| BUG-02 | Testes de usuários apresentam instabilidade (RERUN automático) | 🟡 Média | 🔴 Aberto | `PUT /usuarios/{id}`, `POST /usuarios`, `DELETE /usuarios/{id}` |

---

## BUG-01 — `DELETE /produtos/{id}`: Comportamento inesperado gera XPASS

| Campo | Valor |
|---|---|
| **ID** | BUG-01 |
| **Título** | `test_excluir_produto_existente` marcado como `xfail` passou inesperadamente (XPASS) |
| **Severidade** | 🟡 Média |
| **Prioridade** | 🟡 Média |
| **Status** | 🟠 Requer Ação (Marker desatualizado) |
| **Ambiente** | `https://compassuol.serverest.dev` |
| **Endpoint Afetado** | `DELETE /produtos/{id}` |
| **Arquivo de Teste** | `tests/test_produtos.py` |
| **Função de Teste** | `test_excluir_produto_existente` |
| **Tipo de Resultado** | `XPASS` (Expected Failure que passou) |

---

### 📋 Contexto

O teste `test_excluir_produto_existente` foi originalmente marcado com `@pytest.mark.xfail` porque a API ServeRest retornava a mensagem `"Nenhum registro excluído"` ao tentar excluir um produto recém-cadastrado — mesmo com um ID válido — em vez de retornar `"Registro excluído com sucesso"`.

Na execução atual dos testes, o teste **passou inesperadamente**, gerando um resultado `XPASS` (unexpected pass).

---

### 🔄 Saída Real da Execução dos Testes

```
tests/test_produtos.py::test_excluir_produto_existente XPASS (Bug na
ServeRest: retorna 'Nenhum registro excluído' mesmo para produto
existente)                                                         [ 70%]

======================= 16 passed, 1 xpassed in 21.19s ========================
```

---

### 🔍 Análise das Possibilidades

| Hipótese | Descrição |
|---|---|
| **A) Bug corrigido na API** | A ServeRest corrigiu o endpoint `DELETE /produtos/{id}` e agora retorna a mensagem correta. O marker `xfail` deve ser **removido**. |
| **B) Comportamento intermitente** | O endpoint apresenta comportamento inconsistente — às vezes retorna a mensagem correta, às vezes não. Indica instabilidade no backend. |
| **C) Dependência de estado** | O produto cadastrado imediatamente antes do DELETE está sendo encontrado em uma execução, mas não em outra (possível problema de sincronização). |

---

### ✅ Comportamento Esperado (correto)

```
HTTP 200 OK
{ "message": "Registro excluído com sucesso" }
```

### ❌ Comportamento Anterior (bugado — que gerou o xfail)

```
HTTP 200 OK
{ "message": "Nenhum registro excluído" }
```

---

### 💡 Impacto

- **Testes:** O resultado `XPASS` é tratado pelo Pytest como **falha implícita** se `strict=True` estiver configurado no marker. Pode quebrar pipelines de CI.
- **Confiabilidade:** O marker `@pytest.mark.xfail` está desatualizado e enganoso para a equipe.
- **Manutenção:** Qualquer desenvolvedor que ler o teste assumirá que o bug ainda existe.

---

### 🔧 Ação Recomendada

1. Executar o teste **5 vezes consecutivas** para confirmar se o comportamento é consistente.
2. Se o DELETE retornar sempre `"Registro excluído com sucesso"` → **remover o `@pytest.mark.xfail`** do teste.
3. Se o comportamento for inconsistente → documentar como `BUG-01b` (instabilidade) e manter o marker.

**Código atual (a ser ajustado):**
```python
# ANTES — remover o decorator quando o bug for confirmado como corrigido
@pytest.mark.xfail(reason="Bug na ServeRest: retorna 'Nenhum registro excluído' mesmo para produto existente")
def test_excluir_produto_existente(token_admin):
    ...
    assert resposta_exclusao.json()["message"] == "Registro excluído com sucesso"
```

```python
# DEPOIS (quando confirmado corrigido)
def test_excluir_produto_existente(token_admin):
    ...
    assert resposta_exclusao.json()["message"] == "Registro excluído com sucesso"
```

---

## BUG-02 — Instabilidade em Testes de Usuários (RERUN automático)

| Campo | Valor |
|---|---|
| **ID** | BUG-02 |
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

## 📊 Resumo Executivo

| ID | Endpoint | Resultado na Execução | Causa Provável | Ação |
|---|---|---|---|---|
| BUG-01 | `DELETE /produtos/{id}` | XPASS | Bug corrigido na API / marker desatualizado | Remover `@pytest.mark.xfail` após confirmação |
| BUG-02 | `PUT`, `POST`, `DELETE /usuarios/{id}` | RERUN (x3) | Instabilidade de rede / race condition | Investigar com `--tb=long`, adicionar timeout |

**Resultado Geral da Última Execução:** `16 passed, 1 xpassed` em `21.19s`
