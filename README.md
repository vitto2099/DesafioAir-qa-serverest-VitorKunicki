# 🚀 Desafio Técnico — AWS AI FDE Driven Quality Engineering

> **Programa:** AI/R Fellowship (AIR Academy & Innovation Studio Quality Engineering com apoio da AWS)  
> **Projeto:** Testes automatizados para a API pública [ServeRest](https://compassuol.serverest.dev/)
> **CI Status:** ![CI Workflow](https://github.com/vitto2099/desafio-qa-serverest-VitorKunicki/actions/workflows/pytest.yml/badge.svg)

---

## 🛠️ O que Fizemos (Ajustes e Correções Recentes)

Identificamos e corrigimos alguns gargalos para garantir a estabilidade local e da pipeline de CI no GitHub Actions:

<details>
<summary><b>1. Correção no Teste de Produto Inexistente (<code>test_buscar_produto_por_id_inexistente</code>)</b></summary>

* **Problema**: O teste enviava o ID inválido `id_que_nao_existe_123` (21 caracteres). A API do ServeRest exige exatamente 16 caracteres alfanuméricos, gerando um erro de formato de ID (KeyError) ao invés da mensagem `"Produto não encontrado"`.
* **Solução**: Alterado o ID de teste para `0000000000000000` (16 caracteres). A API agora retorna corretamente o status 400 com a mensagem esperada.
</details>

<details>
<summary><b>2. Correção de Imports (<code>ModuleNotFoundError</code> no CI)</b></summary>

* **Problema**: Os arquivos de testes importavam módulos usando o prefixo `tests.conftest` e `tests.schemas`, o que falhava no ambiente de CI pois a pasta `tests` não estava no path global de execução do runner.
* **Solução**: Removemos o prefixo `tests.`, utilizando a resolução de path nativa do pytest (`from conftest ...` e `from schemas ...`).
</details>

<details>
<summary><b>3. Ajuste no Script de Execução (<code>rodarTudo.py</code>)</b></summary>

* **Problema**: O arquivo chamava-se `test_rodarTudo.py`. O pytest tentava coletá-lo como um teste e disparava um comando global `pip install` durante a varredura, o que travava a execução com `exit code 2` no CI.
* **Solução**: Renomeado para `rodarTudo.py` e protegido a execução do subprocesso de instalação dentro do bloco `if __name__ == "__main__":`.
</details>

---

## 📋 Plano de Testes

<details>
<summary>🔍 <b>Objetivo & Estratégia</b></summary>

### 1. Objetivo da Suíte
Garantir a qualidade, estabilidade e corretude dos principais endpoints da API pública ServeRest (`/usuarios`, `/login` e `/produtos`) validando respostas para dados válidos, inválidos e regras de autenticação.

### 2. Estratégia
* **Tipo de Teste**: API (Contrato e Funcionais).
* **Camada**: Back-end (Interface REST).
* **Ferramentas**: Python 3.9+, Pytest, `requests` e `jsonschema`.
</details>

<details>
<summary>🎯 <b>Escopo & Cenários Cobertos</b></summary>

### 3. Escopo
* **Coberto**: Gerenciamento de Usuários (`/usuarios`), Autenticação (`/login`) e Catálogo de Produtos (`/produtos`).
* **Não Coberto**: Endpoint de Carrinhos (`/carrinhos`) e testes de performance/carga.

### 4. Cenários Implementados
#### Rota `/usuarios`
* Listagem com validação de formato (status 200).
* Cadastro com dados válidos, e-mail duplicado e sem campos obrigatórios.
* Busca por ID existente e inexistente.
* Atualização com sucesso e criação de novo usuário caso inexistente.
* Exclusão com sucesso e exclusão de ID inexistente.

#### Rota `/login`
* Login bem-sucedido (JSON Schema verificado) e falhas por senha incorreta, e-mail inexistente e campos vazios.

#### Rota `/produtos`
* Listagem de produtos.
* Cadastro com/sem token de administrador.
* Busca, atualização e exclusão de produtos com regras de permissão.
</details>

<details>
<summary>✅ <b>Critérios de Qualidade (Definition of Done)</b></summary>

* Nomenclatura seguindo `test_<acao>_<resultado_esperado>.py`.
* Asserções explícitas de status HTTP e corpo da resposta.
* Uso de fixtures no `conftest.py` para setup/teardown isolados.
* Idempotência com geradores randômicos (ex: UUID para dados únicos).
* Validação de estrutura de resposta JSON Schema.
</details>

---

## 📂 Estrutura do Projeto

```
Pytest/
│
├── tests/                                              ← todos os testes do projeto
│   ├── conftest.py                                     ← fixtures e helpers de API
│   ├── schemas.py                                      ← esquemas JSON Schema
│   ├── test_login.py                                   ← testes de autenticação
│   ├── test_produtos.py                                ← testes de catálogo
│   └── test_*.py                                       ← testes de gerenciamento de usuários
│
├── pytest.ini                                          ← configurações do Pytest
├── requirements.txt                                    ← dependências do projeto
└── README.md                                           ← este arquivo descritivo
```

---

## 🚀 Como Instalar e Rodar

1. **Instale o Python (3.9+) e as dependências**:
```bash
pip install -r requirements.txt
```

2. **Execute os testes**:
```bash
python -m pytest -v
```

---

## 📊 Cobertura & Integração Contínua

### Método de Cálculo da Cobertura da API
Para calcular a cobertura de testes da API REST, utilizamos a abordagem baseada em **mapeamento de rotas e verbos HTTP cobertos** (conforme descrito no artigo de referência). O cálculo segue o mapeamento de todos os endpoints e verbos da API ServeRest contra o que é executado na nossa suíte de testes.

A API ServeRest possui um total de **16 rotas/verbos (endpoints)** descritos no Swagger oficial:
- **Usuários** (4): GET `/usuarios`, POST `/usuarios`, PUT `/usuarios/{id}`, DELETE `/usuarios/{id}`
- **Login** (1): POST `/login`
- **Produtos** (4): GET `/produtos`, POST `/produtos`, PUT `/produtos/{id}`, DELETE `/produtos/{id}`
- **Carrinhos** (4): GET `/carrinhos`, POST `/carrinhos`, PUT `/carrinhos/{id}`, DELETE `/carrinhos/{id}` (Fora do escopo)
- **Administração/Dashboard** (3): GET `/administracao`, etc (fora do escopo principal)

### Cobertura Atingida
* **Endpoints Cobertos:** 9 principais de 16 totais da API.
* **Percentual de Cobertura Total:** **56.25%** do total geral da API (ou **100%** do escopo proposto de Login, Usuários e Produtos).
* **Cenários Fora do Escopo & Raciocínio:**
  * O endpoint `/carrinhos` e rotas administrativas adicionais não foram incluídos por estarem explicitamente fora do escopo definido nos requisitos desta etapa de testes da API.

* **CI/CD (GitHub Actions):** Configurado em `.github/workflows/pytest.yml`, executando todos os testes automaticamente em ambiente Ubuntu a cada push/pull request nas branches `main` e `master`.

---

## 🐛 Bugs Encontrados na ServeRest

| Bug | Comportamento Esperado | Comportamento Obtido | Severidade | Status |
| :--- | :--- | :--- | :--- | :--- |
| **DELETE `/produtos/{id}`** | Deletar e retornar `"Registro excluído com sucesso"` (200 OK) | Deleta o produto mas retorna `"Nenhum registro excluído"` (200 OK) | Média | Marcado com `@pytest.mark.xfail` |
| **GET `/produtos/{id_inexistente}`** | Retornar `404 Not Found` para recurso não existente | Retorna `400 Bad Request` com a mensagem `"Produto não encontrado"` | Baixa | Validado no teste |

