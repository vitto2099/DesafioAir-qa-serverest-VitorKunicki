# Desafio Técnico — AWS AI FDE Driven Quality Engineering

> **Programa:** AI/R Fellowship (AIR Academy & Innovation Studio Quality Engineering com apoio da AWS)  
> **Projeto:** Testes automatizados para a API pública [ServeRest](https://compassuol.serverest.dev/)
> **CI Status:** ![![CI Workflow](https://github.com/vitto2099/DesafioAir-qa-serverest-VitorKunicki/actions/workflows/pytest.yml/badge.svg)](https://github.com/vitto2099/DesafioAir-qa-serverest-VitorKunicki/actions/workflows/pytest.yml)
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

## 🐛 Bugs Encontrados na ServeRest

| Bug (ID) | Comportamento Esperado | Comportamento Obtido | Severidade | Status |
| :--- | :--- | :--- | :--- | :--- |
| **BUG-01: Instabilidade em `/usuarios`** | Testes de PUT, POST e DELETE de usuários passarem de primeira | Testes falham na 1ª tentativa e exigem reexecução automática (RERUN), sugerindo instabilidade na API. | 🟡 Média | 🔴 Aberto |
| **BUG-02: Senha exposta em `/usuarios`** | Campo `password` **nunca** deve aparecer nas respostas da API | Endpoints `GET /usuarios` e `GET /usuarios/{id}` retornam a senha do usuário em **texto puro** na resposta JSON | 🔴 Alta | 🔴 Aberto |


