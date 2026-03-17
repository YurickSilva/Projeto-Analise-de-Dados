import yaml
from pathlib import Path
from utils.security import hash_senha

CONFIG_PATH = Path("config/users.yaml")

def carregar_usuarios():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def salvar_usuarios(config: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, allow_unicode=True)


def criar_usuario(username, name, senha, role, workspaces):
    config = carregar_usuarios()

    if username in config["credentials"]["usernames"]:
        raise ValueError("Usuário já existe")

    config["credentials"]["usernames"][username] = {
        "name": name,
        "password": hash_senha(senha),
        "role": role,
        "workspaces": workspaces,
    }

    salvar_usuarios(config)