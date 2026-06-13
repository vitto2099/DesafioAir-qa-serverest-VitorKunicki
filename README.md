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
├── PLANO-DE-TESTES.md                                  ← documentação do planejamento
└── README.md                                           ← este arquivo
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
