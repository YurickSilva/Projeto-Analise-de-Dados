import streamlit as st
from workspaces import home, admin

def executar_pagina(menu_selecionado: str):
    if menu_selecionado == "Home":
        home.render()
    elif menu_selecionado == "Usuários":
        admin.render()
    else:
        st.error(f"Página não mapeada: {menu_selecionado}")
    
