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

