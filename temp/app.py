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

authenticator.logout("Logout", "sidebar")
st.sidebar.success(f"Bem-vindo, {nome}")

# 📌 MENU
with st.sidebar:

    st.image(LOGO_PATH, use_container_width=True)
    st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
    st.success(f"Bem-vindo, {nome}")
    
    menu = sac.menu(
        build_menu(),
        open_all=True,
        format_func="title",
    )

# 🧭 ROUTER
executar_pagina(menu)