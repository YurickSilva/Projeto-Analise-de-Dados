import streamlit as st
import streamlit_antd_components as sac
from auth.authenticator import login
from navigation import build_menu
from router import executar_pagina
from utils.styles import apply_global_ui
from Mock.mockuser import gerar_usuario_teste

# 1. GARANTIA DE AMBIENTE:
# Verifica e gera o usuário de teste antes de carregar o sistema de login
gerar_usuario_teste()

# 2. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(layout="wide", page_title="Voyzer Dashboard")
#LOGO_PATH = ""
#apply_global_ui(LOGO_PATH)

# 3. AUTENTICAÇÃO
# O login() agora encontrará o users.yaml mesmo que seja o primeiro acesso
authenticator, nome, status, username = login()

if not status:
    st.stop()

# 4. NAVEGAÇÃO (SIDEBAR)
with st.sidebar:
    
    pagina_na_url = st.query_params.get("p", "Home")
    lista_menu = build_menu()

    from navigation import get_menu_index
    indice_atual = get_menu_index(lista_menu, pagina_na_url)

    menu = sac.menu(
        lista_menu,
        index=indice_atual,
        open_all=True,
        format_func="title",
        key="menu_navegacao"
    )

    if menu:
        st.query_params["p"] = menu

    # Espaçador para empurrar o botão de logout para baixo
    st.markdown("---")
    if st.button("Logout", use_container_width=True, type="secondary"):
        authenticator.logout(location="unrendered")
        st.rerun()

# 5. ROTEAMENTO DE PÁGINAS
executar_pagina(menu)