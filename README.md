# Plano de Testes & Ajustes Realizados: API ServeRest

## 🛠️ O que Fizemos (Ajustes e Correções Recentes)

Durante a validação da suíte de testes e integração contínua (CI) via GitHub Actions, identificamos e resolvemos alguns problemas críticos para garantir que a pipeline passe com sucesso:

### 1. Correção no Teste de Produto Inexistente (`test_buscar_produto_por_id_inexistente`)
* **Problema Encontrado**: O teste tentava buscar um produto com o ID inválido `id_que_nao_existe_123`. A API do ServeRest rejeitava o formato do ID (que exige exatamente 16 caracteres alfanuméricos) retornando um erro de validação de formato. Isso causava um `KeyError` na asserção, pois o campo `message` não vinha na resposta JSON.
* **Solução**: Ajustado o ID de teste para `0000000000000000` (16 caracteres). A API agora processa a busca com sucesso e retorna corretamente o status 400 com a mensagem `"Produto não encontrado"`, fazendo o teste passar.

### 2. Resolução do erro `ModuleNotFoundError: No module named 'tests'` no GitHub Actions
* **Problema Encontrado**: Os arquivos `test_login.py`, `test_produtos.py` e `test_listar_usuarios_retorna_campos_esperados.py` continham importações com o prefixo `tests.conftest` e `tests.schemas`. Quando o pytest rodava no CI do GitHub Actions a partir do diretório raiz, ele não reconhecia a pasta `tests` como um pacote Python global, quebrando as importações durante a coleta dos testes.
* **Solução**: Removemos o prefixo `tests.` das importações de todos os arquivos. Agora eles importam localmente (`from conftest import ...` e `from schemas import ...`), o que é o padrão nativo compatível com o pytest em qualquer ambiente.

### 3. Ajuste no script de execução local `rodarTudo.py`
* **Problema Encontrado**: O arquivo chamava-se `test_rodarTudo.py`. Devido ao prefixo `test_`, o pytest tentava coletá-lo como um arquivo de testes e executava a chamada de nível de módulo do `subprocess.run(pip install...)` no momento de importação. No runner do GitHub Actions, essa instalação redundante falhava ou causava bloqueio, quebrando o pytest na fase de coleta com `exit code 2`.
* **Solução**: Renomeamos o arquivo para `rodarTudo.py` (para que o pytest não tente coletá-lo como teste) e protegemos a chamada de instalação com o bloco `if __name__ == "__main__":`.

---

## 📋 Plano de Testes Original

### 1. Objetivo da Suíte
O objetivo desta suíte de testes automatizados é garantir a qualidade, estabilidade e corretude dos principais endpoints da API pública ServeRest (`/usuarios`, `/login` e `/produtos`). A suíte deve validar respostas para dados válidos, inválidos e fluxos de negócio como autenticação e validação de perfil de administrador.


## 2. Estratégia
- **Tipo de Teste:** Testes de API (Testes de Contrato e Testes Funcionais).
- **Camada:** Back-end (Interface REST).
- **Ferramentas:** Python 3.9+, Pytest, biblioteca `requests` (para requisições HTTP) e biblioteca `jsonschema` (para validação de contratos de API).

## 3. Escopo
- **O que está coberto:** 
  - Gerenciamento de Usuários (`/usuarios`): Listagem, cadastro, busca, atualização e exclusão.
  - Autenticação (`/login`): Geração de token e validação de credenciais.
  - Catálogo de Produtos (`/produtos`): Listagem, cadastro, busca, atualização e exclusão.
- **O que ficou fora:**
  - O endpoint de Carrinhos (`/carrinhos`) não foi coberto nesta versão pois o foco inicial foi na trilha principal de cadastro e produtos.
  - Testes de performance, carga e stress da API.

## 4. Cenários a Implementar

### Endpoint `/usuarios`
- Listar usuários retorna status 200 e valida formato da resposta.
- Cadastrar usuário válido retorna 201 e ID.
- Cadastrar usuário com email duplicado retorna 400.
- Cadastrar usuário com campos obrigatórios ausentes (nome, email, password, administrador) retorna 400.
- Buscar usuário por ID existente retorna 200.
- Buscar usuário por ID inexistente retorna 400.
- Atualizar usuário com sucesso retorna 200.
- Atualizar usuário inexistente cria novo (201).
- Excluir usuário com sucesso retorna 200.
- Excluir usuário inexistente retorna 200 (mensagem apropriada).

### Endpoint `/login`
- Login com credenciais corretas retorna token e 200.
- Login com senha errada retorna 401.
- Login com email inexistente retorna 401.
- Login com campos vazios retorna 400.

### Endpoint `/produtos`
- Listar produtos retorna 200 e valida estrutura da resposta.
- Cadastrar produto com token de admin retorna 201.
- Cadastrar produto sem token (ou não-admin) retorna 401/403.
- Cadastrar produto sem campos obrigatórios retorna 400.
- Buscar produto por ID existente retorna 200.
- Buscar produto por ID inexistente retorna 400.
- Atualizar produto com token de admin retorna 200.
- Excluir produto com token de admin retorna 200.

## 5. Critérios de Qualidade (Definition of Done)
- O código do teste deve seguir o padrão de nomenclatura `test_<acao>_<resultado_esperado>.py`.
- Cada teste deve conter asserções (`assert`) claras, verificando tanto o status code HTTP quanto campos relevantes do corpo da resposta (JSON).
- As rotinas de preparação e limpeza de dados (setup/teardown) devem ser isoladas, preferencialmente usando fixtures no `conftest.py`.
- O teste deve ser idempotente (rodar várias vezes sem falhar) utilizando geradores de dados randômicos (ex: uuid para emails e nomes).
- Validações de estrutura (JSON Schema) devem ser efetuadas em endpoints críticos (listagem e login).
- A cobertura deve abranger com sucesso e falha (caminho feliz e caminho triste).

---

# Desafio Técnico — AWS AI FDE Driven Quality Engineering

**Programa:** AI/R Fellowship (AIR Academy & Innovation Studio Quality Engineering com apoio da AWS)  
**Projeto:** Testes automatizados para a API pública  [ServeRest](https://compassuol.serverest.dev/).


## Objetivo
O objetivo deste projeto foi elevar o nível da automação de testes existente. Inicialmente cobrindo apenas a rota de usuários, o escopo foi expandido para garantir a qualidade de rotas críticas de negócio: **Login** e **Produtos**. 

Essa expansão nos permite:
- Validar as regras de autenticação e permissões de usuários (como administradores x usuários comuns).
- Garantir a integridade dos contratos de API através da validação das respostas (JSON Schema).
- Mensurar a real cobertura dos testes sobre a API.
- Executar os testes de forma automatizada em um fluxo de Integração Contínua (CI).

---

## Estrutura do projeto

```
Pytest/
│
├── tests/                                              ← pasta com todos os testes
│   ├── conftest.py                                     ← configurações e funções compartilhadas
│   ├── schemas.py                                      ← esquemas de validação (JSON Schema)
│   ├── test_login.py                                   ← testes da rota de login
│   ├── test_produtos.py                                ← testes da rota de produtos
│   └── test_*.py                                       ← testes da rota de usuários
│
├── pytest.ini                                          ← configurações do Pytest
├── requirements.txt                                    ← lista de dependências
└── README.md                                           ← este arquivo (com o plano no início)

```

---

## Como instalar e rodar

1. Instale o Python (3.9+) e as dependências:
```bash
pip install -r requirements.txt
```

2. Execute todos os testes:
```bash
python -m pytest -v
```

---

## Os 26 testes implementados

### Usuários (`/usuarios`)
1. `test_listar_usuarios_retorna_status_200`
2. `test_listar_usuarios_retorna_campos_esperados` (Valida JSON Schema)
3. `test_cadastrar_usuario_valido`
4. `test_cadastrar_usuario_com_email_duplicado`
5. `test_cadastrar_usuario_sem_campo_nome`
6. `test_cadastrar_usuario_sem_campo_email`
7. `test_cadastrar_usuario_sem_campo_password`
8. `test_buscar_usuario_por_id_existente`
9. `test_buscar_usuario_por_id_inexistente`
10. `test_atualizar_usuario_com_sucesso`
11. `test_atualizar_usuario_inexistente_cria_novo`
12. `test_excluir_usuario_com_sucesso`
13. `test_excluir_usuario_inexistente`
14. `test_cadastrar_usuario_sem_campo_administrador`

### Login (`/login`)
15. `test_login_com_credenciais_corretas` (Valida JSON Schema)
16. `test_login_com_senha_errada`
17. `test_login_com_email_inexistente`
18. `test_login_com_campos_vazios`

### Produtos (`/produtos`)
19. `test_listar_produtos_retorna_200` (Valida JSON Schema)
20. `test_cadastrar_produto_com_token_admin`
21. `test_cadastrar_produto_sem_token_admin`
22. `test_cadastrar_produto_token_ausente`
23. `test_buscar_produto_por_id_existente`
24. `test_buscar_produto_por_id_inexistente`
25. `test_atualizar_produto_existente`
26. `test_excluir_produto_existente` (Contém bug reportado na ServeRest, marcado como `xfail`)

---

## Análise de Cobertura (Coverage)

Com base na metodologia de *Path/Operator Coverage* detalhada na **Revista DTAR** (Medium), a cobertura desta suíte foi calculada comparando os endpoints testados com os endpoints totais da API ServeRest.

- **Método Utilizado**: Path Coverage / Operator Coverage (Endpoints testados / Endpoints totais da API).
- **Cálculo**:
  - Endpoints cobertos: `/usuarios` (5 rotas), `/login` (1 rota), `/produtos` (5 rotas). Total = 11 endpoints testados.
  - Endpoints totais da ServeRest: `/usuarios` (5), `/login` (1), `/produtos` (5), `/carrinhos` (4). Total = 15 endpoints totais disponíveis.
  - Cobertura atingida: `11 / 15 = 73.3%`
- **Cenários fora do escopo**:
  - O endpoint de `/carrinhos` ficou fora desta versão da suíte, pois o foco esteve em estabilizar o catálogo e o fluxo central de negócio (autenticação de usuário e gerenciamento de produto).

---

## Integração Contínua (CI)

Este projeto possui configuração de **GitHub Actions** (`.github/workflows/pytest.yml`). A cada `push` no repositório, os testes são executados automaticamente em um ambiente Ubuntu. Isso garante que nenhum commit introduza falhas no código sem que a equipe seja alertada.

---

## Bugs Encontrados na ServeRest

Durante a evolução desta suíte de testes, mapeamos os seguintes bugs (comportamentos inesperados) na API ServeRest:

### Bug 1: Exclusão de produto recém-cadastrado retorna mensagem ambígua
- **Passos:** Cadastrar um produto usando um token de administrador. Em seguida, enviar uma requisição `DELETE` para a rota `/produtos/{id_recem_criado}`.
- **Esperado:** O endpoint deveria retornar status `200 OK` com a mensagem `"Registro excluído com sucesso"`.
- **Obtido:** O endpoint deleta o produto, mas retorna a mensagem `"Nenhum registro excluído"`.
- **Severidade:** Média (o status code está correto e o item é apagado, mas a mensagem induz o cliente a acreditar que não funcionou).
- **Ação:** O teste referente a isso foi marcado como `xfail` (Expected Failure) para que a suíte saiba que é um problema mapeado.

### Bug 2: Consulta a produto inexistente retorna status code inadequado
- **Passos:** Realizar uma requisição `GET` para a rota `/produtos/{id_inexistente}`.
- **Esperado:** Em APIs REST, buscar por um recurso que não existe deveria retornar `404 Not Found`.
- **Obtido:** O endpoint retorna o status code `400 Bad Request` com a mensagem `"Produto não encontrado"`.
- **Severidade:** Baixa (a mensagem deixa claro o problema, mas foge do padrão REST).
