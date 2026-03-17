import yaml
from pathlib import Path
import streamlit_authenticator as stauth
import streamlit as st
from utils.logger import setup_logger

logger = setup_logger("auth")

CONFIG_PATH = Path("config/users.yaml")

def carregar_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def criar_authenticator():
    config = carregar_config()

    return stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )

def login():
    config = carregar_config()
    authenticator = criar_authenticator()

    authenticator.login(
        location="main",
        key="login_form"  
    )

    status = st.session_state.get("authentication_status")
    nome = st.session_state.get("name")
    username = st.session_state.get("username")

    # Estado zumbi
    if status and username not in config["credentials"]["usernames"]:
        authenticator.logout(location="unrendered")
        st.session_state.clear()
        st.rerun()

    # LOGIN INVÁLIDO (somente após tentativa)
    if status is False:
        st.error("❌ Usuário ou senha inválidos")
        logger.warning("Tentativa de login inválida")
        
    if status:
        user_cfg = config["credentials"]["usernames"][username]

        role = user_cfg.get("role", "user")
        workspaces = user_cfg.get("workspaces", [])

        # ADMIN IGNORA WORKSPACES
        if role == "admin":
            workspaces = ["*"]  # wildcard

        st.session_state["role"] = role
        st.session_state["workspaces"] = workspaces

        logger.info(
            f"Login efetuado | user={username} | role={role} | workspaces={workspaces}"
        )

    return authenticator, nome, status, username

def exigir_login():
    if not st.session_state.get("authentication_status"):
        st.warning("Faça login para acessar esta página.")
        st.stop()

    return {
        "nome": st.session_state.get("name"),
        "username": st.session_state.get("username"),
    }
