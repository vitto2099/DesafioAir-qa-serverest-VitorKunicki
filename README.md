# Desafio Técnico — AWS AI FDE Driven Quality Engineering

> **Programa:** AI/R Fellowship (AIR Academy & Innovation Studio Quality Engineering com apoio da AWS)  
> **Projeto:** Testes automatizados para a API pública [ServeRest](https://compassuol.serverest.dev/)
> **CI Status:** ![![CI Workflow](https://github.com/vitto2099/DesafioAir-qa-serverest-VitorKunicki/actions/workflows/pytest.yml/badge.svg)](https://github.com/vitto2099/DesafioAir-qa-serverest-VitorKunicki/actions/workflows/pytest.yml)
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

## 🐛 Bugs Encontrados na ServeRest

| Bug (ID) | Comportamento Esperado | Comportamento Obtido | Severidade | Status |
| :--- | :--- | :--- | :--- | :--- |
| **BUG-01: Instabilidade em `/usuarios`** | Testes de PUT, POST e DELETE de usuários passarem de primeira | Testes falham na 1ª tentativa e exigem reexecução automática (RERUN), sugerindo instabilidade na API. | 🟡 Média | 🔴 Aberto |
| **BUG-02: Senha exposta em `/usuarios`** | Campo `password` **nunca** deve aparecer nas respostas da API | Endpoints `GET /usuarios` e `GET /usuarios/{id}` retornam a senha do usuário em **texto puro** na resposta JSON | 🔴 Alta | 🔴 Aberto |


