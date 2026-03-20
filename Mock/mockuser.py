import os
import yaml
from pathlib import Path

def gerar_usuario_teste():
    raiz_projeto = Path(__file__).resolve().parents[1]
    config_path = raiz_projeto / "config" / "users.yaml"
    
    if not config_path.exists():
        os.makedirs(raiz_projeto / "config", exist_ok=True)
        
        default_config = {
            "cookie": {
                "expiry_days": 30,
                "key": "plataforma-bi-key-v2",
                "name": "plataforma_bi"
            },
            "credentials": {
                "usernames": {
                    "loginpadrao": {
                        "name": "Login Padrão Para Teste",
                        "password": "$2b$12$rR9HeywzpKw3alta4wQD8OGNsN9SAy3MAwAzb7mm8EHJ6bvPGtDLG",
                        "role": "admin",
                        "workspaces": ["home", "controladoria", "ti_global"]
                    }
                }
            }
        }
        
        with open(config_path, "w", encoding="utf-8") as file:
            yaml.dump(default_config, file, default_flow_style=False, allow_unicode=True)
        
        print(f"✅ Arquivo de configuração criado em: {config_path}")
    else:
        print("ℹ️ Arquivo users.yaml já existe. Nenhuma alteração feita.")

if __name__ == "__main__":
    gerar_usuario_teste()