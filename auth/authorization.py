import streamlit as st
from utils.logger import setup_logger

logger = setup_logger("authz")


def usuario_tem_acesso(workspace: str) -> bool:

    status = st.session_state.get("authentication_status")

    if not status:
        return False

    workspaces = st.session_state.get("workspaces", [])

    # 🔥 ADMIN
    if "*" in workspaces:
        return True

    autorizado = workspace in workspaces

    if not autorizado:
        logger.warning(
            f"Acesso negado | user={st.session_state.get('username')} | workspace={workspace}"
        )

    return autorizado

def usuario_eh_admin() -> bool:
    return st.session_state.get("role") == "admin"