from auth.authorization import usuario_tem_acesso
import streamlit as st
import pandas as pd
from utils.styles import (
    apply_metric_style,
    apply_right_panel_style,
    render_page_title,
)
from components.filters import (
    render_filtro_periodo,
    render_filtro_selectbox,
    render_filtro_hierarquico_clientes,
)
from components.graphs import (
    render_kpi_total,
    render_grafico_linha,
    render_grafico_evolucao_mensal,
    render_grafico_sazonal_comparativo,
)
from metrics.ti import (
    get_tickets_tempo_base_com_filtros,
    aplicar_filtros_padrao_ti,
    kpi_contagem_coluna,
    serie_anual_ti,
    serie_trimestral_ti,
)


def render():
    st.set_page_config(layout="wide", page_title="Análise Temporal de Tickets")
    apply_metric_style()
    WORKSPACE = "ti"
    if not usuario_tem_acesso(WORKSPACE):
        st.error("🚫 Você não tem acesso a este módulo")
        st.stop()

    apply_right_panel_style()
    render_page_title("Análise Temporal de Tickets")

    df_raw = get_tickets_tempo_base_com_filtros()

    col_principal, col_filtros = st.columns([4, 1])

    with col_filtros:
        st.markdown("### ⚙️ Filtros")
        st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

        data_ini, data_fim = render_filtro_periodo(
            df_raw, "criado_em", "tempo_periodo", titulo_expander="📅 Período"
        )

        with st.expander("🌍 Estado"):
            estado = render_filtro_selectbox(df_raw, "estado", "Estado", chave="tempo_est")

        clientes_sel = render_filtro_hierarquico_clientes(
            df_raw,
            col_status="contrato",
            col_cliente="cliente",
            chave="tempo_clientes",
            titulo_header="🤝 Clientes por Contrato",
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # --- LÓGICA DE FILTRO ---
    filtros_valores = {}
    if estado != "Todos":
        filtros_valores["estado"] = estado

    df = aplicar_filtros_padrao_ti(
        df_raw,
        data_col="criado_em",
        data_ini=data_ini,
        data_fim=data_fim,
        filtros_valores=filtros_valores or None,
        clientes_sel=clientes_sel,
        col_cliente="cliente",
    )

    if df.empty:
        st.info("Nenhum dato encontrado para os filtros selecionados.")
        return

    # --- LAYOUT ---
    with col_principal:
        # --- CARTÃO: TOTAL DE TICKETS FECHADOS ---
        c1 = st.columns(1)[0]
        with c1:
            with st.expander("Tickets Fechados", expanded=True):
                render_kpi_total(f"{kpi_contagem_coluna(df, col='situacao')} Tickets Fechados")

        st.markdown("---")

        # --- PRIMEIRA FILEIRA: EVOLUÇÃO ANUAL ---
        with st.expander("Tickets por Ano", expanded=True):
            df_ano = serie_anual_ti(df, date_col="criado_em", out_col="total")
            if not df_ano.empty:
                render_grafico_linha(df_ano, "ano", "total", show_legend=False)
            else:
                st.info("Sem dados de ano disponíveis.")

        st.markdown("---")

        # --- SEGUNDA FILEIRA: EVOLUÇÃO POR TRIMESTRE ---
        with st.expander("Tickets por Trimestre", expanded=True):
            df_tri = serie_trimestral_ti(df, date_col="criado_em", out_col="total", fill_missing=True)

            if not df_tri.empty:
                render_grafico_sazonal_comparativo(df_tri, "T", "ano", altura=300)
            else:
                st.info("Sem dados de trimestre disponíveis.")

        st.markdown("---")

        # --- TERCEIRA FILEIRA: EVOLUÇÃO MENSAL ---
        with st.expander("Tickets por Mês", expanded=True):
            if not df.empty:
                render_grafico_evolucao_mensal(df, "criado_em", altura=350)
            else:
                st.info("Sem dados mensais disponíveis.")