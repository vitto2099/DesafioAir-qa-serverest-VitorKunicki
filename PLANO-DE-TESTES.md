# 📋 Plano de Testes — ServeRest

Este documento descreve os objetivos, a estratégia, o escopo, os cenários de testes planejados/implementados e os critérios de qualidade para a suíte de testes automatizados da API ServeRest.

---

## 🎯 1. Objetivo da Suíte
Garantir a corretude, confiabilidade e estabilidade dos principais fluxos de negócio expostos pela API pública ServeRest (Endpoints: `/usuarios`, `/login` e `/produtos`), assegurando que regras de validação, autenticação, controle de acesso e manipulação de dados funcionem conforme esperado.

---

## 🛠️ 2. Estratégia de Testes
- **Tipo de Teste:** Testes de API funcionais e de contrato.
- **Camada:** Back-end/API.
- **Ferramentas:**
  - **Linguagem:** Python 3.9+
  - **Framework de Testes:** Pytest (estrutura, parametrização e execução).
  - **Requisições HTTP:** Biblioteca `requests`.
  - **Validação de Contrato:** Biblioteca `jsonschema` para validação estrutural das respostas em endpoints críticos.
  - **Massa de Dados Dinâmica:** Uso de UUIDs nativos do Python para garantir e-mails e nomes exclusivos a cada execução, promovendo idempotência.

---

## 📦 3. Escopo
- **Em Escopo:**
  - Rota `/usuarios`: CRUD completo, cenários de erro e validações de campos obrigatórios.
  - Rota `/login`: Autenticação com credenciais corretas, inválidas, inexistentes e validação de campos obrigatórios/em branco.
  - Rota `/produtos`: CRUD completo, controle de permissão (administrador vs usuário comum), busca e validação de existência.
- **Fora do Escopo:**
  - Rota `/carrinhos` (futura expansão).
  - Testes não funcionais (Carga, Stress, Performance e Segurança).

---

## 📝 4. Cenários de Teste por Endpoint

### Rota `/usuarios`
- [x] **GET `/usuarios`** - Listar usuários cadastrados com sucesso (Status 200).
- [x] **GET `/usuarios`** - Validar se a resposta de listagem contém as propriedades estruturais necessárias (`quantidade`, `usuarios`).
- [x] **POST `/usuarios`** - Cadastrar usuário válido com sucesso (Status 211).
- [x] **POST `/usuarios`** - Impedir cadastro de e-mail duplicado (Status 400).
- [x] **POST `/usuarios`** - Impedir cadastro sem o campo `nome` (Status 400).
- [x] **POST `/usuarios`** - Impedir cadastro sem o campo `email` (Status 400).
- [x] **POST `/usuarios`** - Impedir cadastro sem o campo `password` (Status 400).
- [x] **POST `/usuarios`** - Impedir cadastro sem o campo `administrador` (Status 400).
- [x] **GET `/usuarios/{id}`** - Buscar usuário por ID cadastrado com sucesso (Status 200).
- [x] **GET `/usuarios/{id}`** - Retornar erro adequado para usuário não encontrado (Status 400).
- [x] **PUT `/usuarios/{id}`** - Atualizar dados de um usuário existente com sucesso (Status 200).
- [x] **PUT `/usuarios/{id}`** - Criar um novo usuário quando o ID informado não existir (Status 201).
- [x] **DELETE `/usuarios/{id}`** - Excluir um usuário existente com sucesso (Status 200).
- [x] **DELETE `/usuarios/{id}`** - Retornar mensagem apropriada ao tentar excluir ID inexistente (Status 200).

### Rota `/login`
- [x] **POST `/login`** - Autenticação com credenciais corretas, retornando token Bearer (Status 200).
- [x] **POST `/login`** - Falha na autenticação ao enviar senha errada (Status 401).
- [x] **POST `/login`** - Falha na autenticação ao enviar e-mail inexistente (Status 401).
- [x] **POST `/login`** - Falha na autenticação com campos em branco (Status 400).

### Rota `/produtos`
- [x] **GET `/produtos`** - Listar produtos com sucesso (Status 200).
- [x] **POST `/produtos`** - Cadastrar produto com sucesso utilizando token de administrador (Status 201).
- [x] **POST `/produtos`** - Impedir cadastro de produto utilizando token de usuário sem privilégios de administrador (Status 403).
- [x] **POST `/produtos`** - Impedir cadastro de produto sem enviar token de autorização (Status 401).
- [x] **GET `/produtos/{id}`** - Buscar detalhes de produto existente (Status 200).
- [x] **GET `/produtos/{id}`** - Retornar erro de produto não encontrado para ID de 16 caracteres inexistente (Status 400).
- [x] **PUT `/produtos/{id}`** - Atualizar dados de produto cadastrado com token de administrador (Status 200).
- [x] **PUT `/produtos/{id}`** - Cadastrar novo produto caso o ID do PUT não seja encontrado (Status 201).
- [x] **DELETE `/produtos/{id}`** - Excluir produto com token de administrador (Status 200) - *Nota: Cenário marcado como XFAIL devido a comportamento inadequado documentado da API.*
- [x] **DELETE `/produtos/{id}`** - Impedir exclusão de produto por usuário não-administrador (Status 403).
- [x] **POST `/produtos`** - Impedir cadastro de produto com nome já existente/duplicado (Status 400).
- [x] **POST `/produtos`** - Impedir cadastro enviando valores negativos ou inválidos para preço e quantidade (Status 400).
- [x] **PUT `/produtos/{id_inexistente}`** - Cadastrar um novo produto utilizando método PUT com ID inexistente (Status 201).
- [x] **DELETE `/produtos/{id}`** - Impedir exclusão de produto sem enviar token de acesso (Status 401).


---

## 🏆 5. Critérios de Qualidade (Definition of Done)
1. **Padrão de Nome:** Arquivos devem seguir `test_<acao>_<resultado_esperado>.py` e funções devem seguir `test_<cenario_verificado>`.
2. **Asserções Múltiplas:** Verificar tanto o status HTTP quanto o corpo da resposta (ex: mensagens de erro e chaves obrigatórias).
3. **Validação de Contrato (JSON Schema):** Validar o formato das chaves retornadas nos endpoints de Login, Listagem de Usuários e Listagem de Produtos.
4. **Isolamento de Dados:** Cada teste deve gerar e limpar seus próprios dados ou utilizar fixtures para teardown automático, garantindo que um teste não interfira em outro.
5. **Independência de Ambiente:** A suíte deve rodar localmente e em ambiente de Integração Contínua (GitHub Actions) sem alterações manuais de variáveis.
