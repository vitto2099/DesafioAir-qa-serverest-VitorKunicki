# ⚡ Comandos de Teste — ServeRest API

**Projeto:** ServeRest API — Automação de Testes  
**Framework:** Pytest  
**Data:** 2026-06-15  

---

## 🚀 Execução Geral

```bash
# Rodar TODA a suíte de testes
python -m pytest -v

# Rodar toda a suíte com saída resumida
python -m pytest -v --tb=short

# Rodar toda a suíte e gerar relatório no terminal
python -m pytest -v --tb=short -q
```

---

## 🔐 Módulo de Login (`test_login.py`)

```bash
# Rodar TODOS os testes de login
python -m pytest tests/test_login.py -v

# Login com credenciais corretas
python -m pytest -k "test_login_com_credenciais_corretas" -v

# Login com senha errada
python -m pytest -k "test_login_com_senha_errada" -v

# Login com e-mail inexistente
python -m pytest -k "test_login_com_email_inexistente" -v

# Login com campos em branco
python -m pytest -k "test_login_com_campos_vazios" -v
```

---

## 📦 Módulo de Produtos (`test_produtos.py`)

```bash
# Rodar TODOS os testes de produtos
python -m pytest tests/test_produtos.py -v

# Listar produtos (GET /produtos)
python -m pytest -k "test_listar_produtos_retorna_200" -v

# Cadastrar produto com token admin
python -m pytest -k "test_cadastrar_produto_com_token_admin" -v

# Cadastrar produto sem permissão de admin (403)
python -m pytest -k "test_cadastrar_produto_sem_token_admin" -v

# Cadastrar produto sem token (401)
python -m pytest -k "test_cadastrar_produto_token_ausente" -v

# Buscar produto por ID existente
python -m pytest -k "test_buscar_produto_por_id_existente" -v

# Buscar produto por ID inexistente
python -m pytest -k "test_buscar_produto_por_id_inexistente" -v

# Atualizar produto existente
python -m pytest -k "test_atualizar_produto_existente" -v

# Excluir produto existente (xfail - bug documentado)
python -m pytest -k "test_excluir_produto_existente" -v

# Excluir produto sem permissão de admin
python -m pytest -k "test_excluir_produto_sem_token_admin" -v

# Cadastrar produto com nome duplicado
python -m pytest -k "test_cadastrar_produto_com_nome_duplicado" -v

# Cadastrar produto com valores inválidos (negativos)
python -m pytest -k "test_cadastrar_produto_valores_invalidos" -v

# PUT com ID inexistente (cria novo produto)
python -m pytest -k "test_atualizar_produto_inexistente_cria_novo" -v

# Excluir produto sem token
python -m pytest -k "test_excluir_produto_token_ausente" -v
```

---

## 👤 Módulo de Usuários (arquivos individuais)

```bash
# Rodar TODOS os testes de usuários
python -m pytest tests/test_listar_usuarios_retorna_status_200.py tests/test_listar_usuarios_retorna_campos_esperados.py tests/test_cadastrar_usuario_valido.py tests/test_cadastrar_usuario_com_email_duplicado.py tests/test_cadastrar_usuario_sem_campo_nome.py tests/test_cadastrar_usuario_sem_campo_email.py tests/test_cadastrar_usuario_sem_campo_password.py tests/test_cadastrar_usuario_sem_campo_administrador.py tests/test_buscar_usuario_por_id_existente.py tests/test_buscar_usuario_por_id_inexistente.py tests/test_atualizar_usuario_com_sucesso.py tests/test_atualizar_usuario_inexistente_cria_novo.py tests/test_excluir_usuario_com_sucesso.py tests/test_excluir_usuario_inexistente.py -v

# Atualizar Usuário com Sucesso
python -m pytest -k "test_atualizar_usuario_com_sucesso" -v

# Atualizar Usuário Inexistente (Cria Novo)
python -m pytest -k "test_atualizar_usuario_inexistente_cria_novo" -v

# Buscar Usuário por ID Existente
python -m pytest -k "test_buscar_usuario_por_id_existente" -v

# Buscar Usuário por ID Inexistente
python -m pytest -k "test_buscar_usuario_por_id_inexistente" -v

# Cadastrar Usuário com Email Duplicado
python -m pytest -k "test_cadastrar_usuario_com_email_duplicado" -v

# Cadastrar Usuário sem Campo Administrador
python -m pytest -k "test_cadastrar_usuario_sem_campo_administrador" -v

# Cadastrar Usuário sem Campo Email
python -m pytest -k "test_cadastrar_usuario_sem_campo_email" -v

# Cadastrar Usuário sem Campo Nome
python -m pytest -k "test_cadastrar_usuario_sem_campo_nome" -v

# Cadastrar Usuário sem Campo Password
python -m pytest -k "test_cadastrar_usuario_sem_campo_password" -v

# Cadastrar Usuário Válido
python -m pytest -k "test_cadastrar_usuario_valido" -v

# Excluir Usuário com Sucesso
python -m pytest -k "test_excluir_usuario_com_sucesso" -v

# Excluir Usuário Inexistente
python -m pytest -k "test_excluir_usuario_inexistente" -v

# Listar Usuários Retorna Campos Esperados
python -m pytest -k "test_listar_usuarios_retorna_campos_esperados" -v

# Listar Usuários Retorna Status 200
python -m pytest -k "test_listar_usuarios_retorna_status_200" -v
```

---

## 🎯 Filtros Úteis

```bash
# Rodar apenas testes que NÃO sejam xfail
python -m pytest -v -m "not xfail"

# Ver os testes marcados como xfail (bugs documentados)
python -m pytest -v -m "xfail"

# Rodar com verbosidade máxima (útil para debug)
python -m pytest -vv

# Parar na primeira falha
python -m pytest -x -v

# Rodar os últimos testes que falharam
python -m pytest --lf -v

# Rodar e mostrar os 10 testes mais lentos
python -m pytest --durations=10 -v
```

---

## 📁 Executar por Módulo Completo

```bash
# Apenas login
python -m pytest tests/test_login.py -v

# Apenas produtos
python -m pytest tests/test_produtos.py -v

# Login + Produtos (novos módulos)
python -m pytest tests/test_login.py tests/test_produtos.py -v
```
