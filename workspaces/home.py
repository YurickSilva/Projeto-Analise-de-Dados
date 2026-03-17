def render():
    import streamlit as st
    from auth.authenticator import exigir_login
    user = exigir_login()

    nome = user["nome"]
    username = user["username"]

    workspaces = st.session_state.get("workspaces", [])
    role = st.session_state.get("role")

    st.title("🏠 Home")

    st.markdown(f"""
    ### 👋 Bem-vindo, **{nome}**
    Você está logado como **`{username}`**
    Acesse no menu à esquerda os seus relatórios.
    """)

    if role:
        st.caption(f"🔐 Papel (role): **{role}**")

    st.divider()

    # 📦 WORKSPACES DISPONÍVEIS
    st.subheader("📂 Módulos disponíveis para você")

    # 🔥 Admin (wildcard)
    if "*" in workspaces:
        st.success("✅ Você tem acesso **total** ao sistema.")
        st.markdown("""
        - 🏠 Home  
        - 📈 Controladoria  
        - 🖥 TI  
        - 🛠 Administração  
        """)
    else:
        if not workspaces:
            st.warning("⚠️ Você não possui módulos liberados no momento.")
        else:
            cols = st.columns(min(3, len(workspaces)))
            for i, ws in enumerate(workspaces):
                with cols[i % len(cols)]:
                    st.info(f"📌 **{ws.capitalize()}**")

    st.divider()
    st.caption("Em caso de dúvidas ou necessidade de acesso, entre em contato com o administrador.")