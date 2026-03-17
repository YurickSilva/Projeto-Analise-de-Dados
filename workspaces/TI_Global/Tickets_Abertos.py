from auth.authorization import usuario_tem_acesso

import streamlit as st

from components.filters import (
    render_filtro_multiselect,
    render_filtro_periodo,
    render_filtro_hierarquico_clientes,
)
from components.tables import render_tabela_generica
from components.graphs import render_kpi_total
from metrics.ti import filtrar_tickets_abertos, get_tickets_abertos_base
from utils.styles import apply_metric_style, apply_right_panel_style, render_page_title

def render():

    WORKSPACE = "ti"
    if not usuario_tem_acesso(WORKSPACE):
        st.error("🚫 Você não tem acesso a este módulo")
        st.stop()

    st.set_page_config(layout="wide", page_title="Tickets Abertos")
    apply_metric_style()
    apply_right_panel_style()
    render_page_title("Tickets Abertos")

    df_raw = get_tickets_abertos_base()

    # FILTRO OBRIGATÓRIO: apenas Tickets com Situação "Aberto"
    df_raw = df_raw[df_raw["Situacao"].astype(str).str.upper() == "ABERTO"].copy()

    col_principal, col_filtros = st.columns([4, 1])

    with col_filtros:
        st.markdown("### ⚙️ Filtros")
        st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

        data_ini, data_fim = render_filtro_periodo(
            df_raw,
            "Criado_em",
            "tickets_abertos_periodo",
            titulo_expander="📅 Período de Abertura",
        )

        mesas_sel = render_filtro_multiselect(
            df_raw,
            "Mesa",
            "Selecione as Mesas",
            titulo_expander="🖥️ Mesas",
            chave="tickets_abertos_mesa",
        )

        responsaveis_sel = render_filtro_multiselect(
            df_raw,
            "Responsavel",
            "Selecione os Responsáveis",
            titulo_expander="👤 Responsáveis",
            chave="tickets_abertos_responsavel_multi",
        )

        estados_sel = render_filtro_multiselect(
            df_raw,
            "Estado",
            "Selecione os Estados",
            titulo_expander="📍 Estado",
            chave="tickets_abertos_estado_multi",
        )

        clientes_sel = render_filtro_hierarquico_clientes(
            df_raw,
            col_status="Contrato",
            col_cliente="Cliente",
            chave="tickets_abertos_clientes",
            titulo_header="🤝 Clientes por Contrato",
        )

        st.markdown("</div>", unsafe_allow_html=True)

    df = filtrar_tickets_abertos(
        df_raw,
        data_ini,
        data_fim,
        estados=estados_sel,
        mesas=mesas_sel,
        responsaveis=responsaveis_sel,
        clientes_sel=clientes_sel,
    )

    with col_principal:
        total_abertos_periodo = len(df)
        
        espaco_esq, col_central, espaco_dir = st.columns([1, 1, 1])
        with col_central:
            st.markdown("<p style='text-align: center; color: gray; margin-bottom: -10px; font-weight: bold;'>TOTAL TICKETS ABERTOS</p>", unsafe_allow_html=True)
            render_kpi_total(total_abertos_periodo)

        st.markdown("---")

        if df.empty:
            st.info("Nenhum ticket encontrado para o filtro selecionado.")
            return

        # Preparar dados para a tabela
        mapeamento = {
            "Id_ticket": "ID Ticket",
            "Cliente": "Cliente",
            "Mesa": "Mesa",
            "Responsavel": "Responsável",
            "Criado_em": "Criado em",
            "Desc_ticket": "Descrição",
        }

        colunas_validas = [c for c in mapeamento.keys() if c in df.columns]

        with st.expander("Lista de Tickets Abertos", expanded=True):
            render_tabela_generica(
                df[colunas_validas],
                mapeamento_nomes=mapeamento,
                colunas_wrap=["Desc_ticket"],
                altura=600,
            )