import streamlit as st
from workspaces import home, admin
from workspaces.TI_Global import Atendimentos, Clientes, Tempo_Decorrido, Tickets_Abertos, Tickets_Geral, Tickets_Tecnicos, Tickets_Tempo, Tickets_Clientes

def executar_pagina(menu_selecionado: str):
    if menu_selecionado == "Home":
        home.render()
    elif menu_selecionado == "Usuários":
        admin.render()
        # --- TI Global ---       
    elif menu_selecionado == "Atendimentos":
        Atendimentos.render()
    elif menu_selecionado == "Clientes":
        Clientes.render()
    elif menu_selecionado == "Tempo Decorrido":
        Tempo_Decorrido.render()
    elif menu_selecionado == "Tickets Abertos":
        Tickets_Abertos.render()
    elif menu_selecionado == "Tickets Geral":
        Tickets_Geral.render()
    elif menu_selecionado == "Tickets Técnicos":
        Tickets_Tecnicos.render()
    elif menu_selecionado == "Tickets Tempo":
        Tickets_Tempo.render()
    elif menu_selecionado == "Tickets Clientes":
        Tickets_Clientes.render()
    else:
        st.error(f"Página não mapeada: {menu_selecionado}")
    
