import streamlit as st
from streamlit_tree_select import tree_select
import pandas as pd
from datetime import date

def filtro_periodo(coluna_data: str):
    data_inicio = st.date_input("Data início", value=None)
    data_fim = st.date_input("Data fim", value=None)

    if not data_inicio and not data_fim:
        return None

    return {
        "coluna_data": coluna_data,
        "data_inicio": data_inicio,
        "data_fim": data_fim
    }

def render_filtro_periodo(df, col_data, chave_unica, titulo_expander="Período"):
    datas_validas = pd.to_datetime(df[col_data]).dt.date.dropna()
    min_base = datas_validas.min() if not datas_validas.empty else date.today()
    max_base = datas_validas.max() if not datas_validas.empty else date.today()

    if min_base == max_base:
        with st.sidebar.expander(titulo_expander):
            st.info("Apenas uma data disponível.")
        return min_base, max_base

    key_slider = f"slider_{chave_unica}"
    key_ini = f"ini_{chave_unica}"
    key_fim = f"fim_{chave_unica}"

    def sync_slider_to_inputs():
        st.session_state[key_ini] = st.session_state[key_slider][0]
        st.session_state[key_fim] = st.session_state[key_slider][1]

    def sync_inputs_to_slider():
        st.session_state[key_slider] = (st.session_state[key_ini], st.session_state[key_fim])

    if key_slider not in st.session_state:
        st.session_state[key_slider] = (min_base, max_base)
    if key_ini not in st.session_state:
        st.session_state[key_ini] = min_base
    if key_fim not in st.session_state:
        st.session_state[key_fim] = max_base

    with st.expander(titulo_expander, expanded=False):
        st.slider(
            "Arraste para ajustar o período",
            min_value=min_base,
            max_value=max_base,
            key=key_slider,
            on_change=sync_slider_to_inputs,
            format="DD/MM/YYYY"
        )

        c1, c2 = st.columns(2)
        with c1:
            st.date_input("Início", key=key_ini, on_change=sync_inputs_to_slider, 
                         min_value=min_base, max_value=max_base)
        with c2:
            st.date_input("Fim", key=key_fim, on_change=sync_inputs_to_slider,
                         min_value=min_base, max_value=max_base)

    return st.session_state[key_slider]

def render_filtro_multiselect(df, col, label, titulo_expander=None, chave="filtro_multi"):
    opcoes = sorted([str(x) for x in df[col].dropna().unique()])
    
    if titulo_expander:
        with st.expander(titulo_expander):
            return st.multiselect(label, options=opcoes, default=opcoes, key=chave)
    else:
        return st.multiselect(label, options=opcoes, default=opcoes, key=chave)

def render_filtro_selectbox(df, col, label, incluir_todos=True, chave="filtro_select"):
    opcoes = sorted([str(x) for x in df[col].dropna().unique()])
    if incluir_todos:
        opcoes = ["Todos"] + opcoes
    return st.selectbox(label, options=opcoes, key=chave)

def render_filtro_radio(label, opcoes, chave="filtro_radio"):
    return st.radio(label, options=opcoes, key=chave)

def render_filtro_hierarquico_clientes(df, col_status, col_cliente, chave, titulo_header="Filtros Hierárquicos"):
    st.markdown(f"**{titulo_header}**")
    
    nodes = []
    status_opcoes = sorted([str(x) for x in df[col_status].dropna().unique()])
    
    for status in status_opcoes:
        clientes_do_status = sorted([str(x) for x in df[df[col_status] == status][col_cliente].dropna().unique()])
        nodes.append({
            "label": status,
            "value": status,
            "children": [{"label": c, "value": c} for c in clientes_do_status]
        })
    
    return_select = tree_select(nodes, check_model="leaf", key=chave)
    
    return return_select.get("checked", [])