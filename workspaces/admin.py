def render():
    import streamlit as st
    from auth.authorization import usuario_eh_admin, usuario_tem_acesso
    from services.users_service import carregar_usuarios, criar_usuario
    from utils.logger import setup_logger

    logger = setup_logger("admin")
    # 🔐 Segurança
    if not usuario_eh_admin() or not usuario_tem_acesso("admin"):
        st.error("🚫 Acesso restrito a administradores")
        st.stop()

    st.title("🛠 Administração de Usuários")

    config = carregar_usuarios()
    users = config["credentials"]["usernames"]

    # 🔍 LISTAGEM
    st.subheader("👥 Usuários existentes")
    st.dataframe([
        {
            "username": u,
            "name": d["name"],
            "role": d.get("role"),
            "workspaces": ", ".join(d.get("workspaces", [])),
        }
        for u, d in users.items()
    ])

    st.divider()

    # ➕ CRIAR USUÁRIO
    st.subheader("➕ Criar novo usuário")

    with st.form("novo_usuario"):
        username = st.text_input("Username (login)")
        name = st.text_input("Nome")
        senha = st.text_input("Senha", type="password")
        role = st.selectbox("Role", ["user", "admin"])
        workspaces = st.multiselect(
            "Workspaces",
            ["home", "controladoria", "ti", "admin"]
        )

        submit = st.form_submit_button("Criar usuário")

    if submit:
        try:
            criar_usuario(username, name, senha, role, workspaces)
            logger.info(f"Usuário criado | user={username}")
            st.success("Usuário criado com sucesso")
            st.rerun()
        except Exception as e:
            st.error(str(e))