import streamlit as st
import streamlit_antd_components as sac
from auth.authenticator import login
from navigation import build_menu
from router import executar_pagina
from utils.styles import apply_global_ui

st.set_page_config(layout="wide", page_title="Voyzer Dashboard")
LOGO_PATH = "visual/Vz_logo1.png"
apply_global_ui(LOGO_PATH)

# 🔐 LOGIN
authenticator, nome, status, username = login()
if not status:
    st.stop()
    
# 📌 MENU
with st.sidebar:
    st.logo(LOGO_PATH)
    
    # 1. Busca qual página está na URL. Se não tiver nada, assume 'Home'
    pagina_na_url = st.query_params.get("p", "Home")

    # 2. Constrói a lista do menu
    lista_menu = build_menu()

    # 3. Descobre qual o índice numérico dessa página na lista
    from navigation import get_menu_index
    indice_atual = get_menu_index(lista_menu, pagina_na_url)

    # 4. Renderiza o menu usando o index correto
    menu = sac.menu(
        lista_menu,
        index=indice_atual, # <--- ISSO mantém a seleção visual
        open_all=True,
        format_func="title",
        key="menu_navegacao"
    )

    # 5. Salva na URL a nova escolha (para o próximo refresh)
    if menu:
        st.query_params["p"] = menu

    if st.button("🚪 Logout", use_container_width=True):
        authenticator.logout(location="unrendered")
        st.rerun()

# 🧭 ROUTER
executar_pagina(menu)