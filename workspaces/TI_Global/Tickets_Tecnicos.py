from auth.authorization import usuario_tem_acesso
import streamlit as st
import pandas as pd
from utils.styles import render_page_title, apply_metric_style, apply_right_panel_style
from components.filters import render_filtro_periodo, render_filtro_selectbox, render_filtro_multiselect
from components.graphs import (
    render_kpi_total, render_grafico_barras, 
    render_grafico_ranking, render_grafico_evolucao_mensal
)
from metrics.ti import get_tickets_tecnicos_base

def render():

    WORKSPACE = "ti"
    if not usuario_tem_acesso(WORKSPACE):
        st.error("🚫 Você não tem acesso a este módulo")
        st.stop()

    st.set_page_config(layout="wide", page_title="Performance de Tickets Técnicos")
    apply_metric_style()
    apply_right_panel_style()
    render_page_title("Performance de Tickets Técnicos")

    df_raw = get_tickets_tecnicos_base()

    col_principal, col_filtros = st.columns([4, 1])

    with col_filtros:
        st.markdown("### ⚙️ Filtros")
        st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

        data_ini, data_fim = render_filtro_periodo(df_raw, 'criado_em', 'perf_periodo', titulo_expander="📅 Período de Análise")

        with st.expander("🌍 Estado"):
            estado = render_filtro_selectbox(df_raw, 'estado', "Estado", chave="perf_est")
        with st.expander("📄 Contrato"):
            contrato = render_filtro_selectbox(df_raw, 'contrato', "Contrato", chave="perf_con")

        tecnicos_sel = render_filtro_multiselect(df_raw, 'responsavel', "Selecionar Técnicos", chave="perf_tec", titulo_expander="👤 Equipe Técnica")

        st.markdown("</div>", unsafe_allow_html=True)

    # --- LÓGICA ---
    df = df_raw.copy()
    df = df[(df['criado_em'].dt.date >= data_ini) & (df['criado_em'].dt.date <= data_fim)]
    df = df[df['responsavel'].isin(tecnicos_sel)]
    if estado != "Todos": df = df[df['estado'] == estado]
    if contrato != "Todos": df = df[df['contrato'] == contrato]

    # --- LAYOUT ---
    with col_principal:
        if not df.empty:
            df_fechados = df[df['situacao'] == 'Fechado'].copy()

            c1, c2 = st.columns(2)
            with c1:
                with st.expander("Tickets Fechados", expanded=True):
                    render_kpi_total(len(df_fechados))
            with c2:
                with st.expander("Tempo Médio de Atendimento", expanded=True):
                    render_kpi_total("138 min")

            st.markdown("---")

            r1, r2 = st.columns([1.2, 0.8])
            with r1:
                with st.expander("Ranking: Mais Tickets Fechados", expanded=True):
                    df_rank = df_fechados.groupby('responsavel').size().reset_index(name='total')
                    render_grafico_ranking(df_rank, 'total', 'responsavel')
            with r2:
                with st.expander("Tickets por Mesa", expanded=True):
                    df_mesa = df.groupby('mesa').size().reset_index(name='total')
                    render_grafico_barras(df_mesa, 'mesa', 'total')

            st.markdown("---")

            b1, b2 = st.columns(2)
            with b1:
                with st.expander("Avaliação dos Tickets", expanded=True):
                    # Agrupamos os dados existentes
                    df_aval = df_fechados.groupby('avaliacao').size().reset_index(name='qtd')
                    # Chamamos o modelo garantindo que 1, 2, 3, 4 e 5 apareçam sempre
                    render_grafico_barras(df_aval, 'avaliacao', 'qtd', categorias_fixas=[1, 2, 3, 4, 5])

            with b2:
                with st.expander("Chamados por Mês (Evolução Anual)", expanded=True):
                    render_grafico_evolucao_mensal(df, 'criado_em')
        else:
            st.info("Nenhum ticket encontrado para os filtros selecionados.")