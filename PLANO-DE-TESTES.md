# Plano de Testes: API ServeRest

## 1. Objetivo da Suíte
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
