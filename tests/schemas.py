SCHEMA_LISTAR_USUARIOS = {
    "type": "object",
    "properties": {
        "quantidade": {"type": "integer"},
        "usuarios": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "email": {"type": "string"},
                    "password": {"type": "string"},
                    "administrador": {"type": "string"},
                    "_id": {"type": "string"}
                },
                "required": ["nome", "email", "password", "administrador", "_id"]
            }
        }
    },
    "required": ["quantidade", "usuarios"]
}

SCHEMA_LOGIN_SUCESSO = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "authorization": {"type": "string"}
    },
    "required": ["message", "authorization"]
}

SCHEMA_LISTAR_PRODUTOS = {
    "type": "object",
    "properties": {
        "quantidade": {"type": "integer"},
        "produtos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "preco": {"type": "integer"},
                    "descricao": {"type": "string"},
                    "quantidade": {"type": "integer"},
                    "_id": {"type": "string"}
                },
                "required": ["nome", "preco", "descricao", "quantidade", "_id"]
            }
        }
    },
    "required": ["quantidade", "produtos"]
}
