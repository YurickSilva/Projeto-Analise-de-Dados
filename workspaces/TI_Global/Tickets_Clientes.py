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
    render_filtro_multiselect,
    render_filtro_hierarquico_clientes,
)
from components.graphs import (
    render_kpi_total,
    render_grafico_barras_ranking,
    render_grafico_ranking,
    render_grafico_donut,
    render_grafico_evolucao_mensal,
)
from metrics.ti import (
    get_tickets_geral_base,
    aplicar_filtro_pagina_mesa,
    aplicar_filtro_pagina_situacao_fechado,
    aplicar_filtros_padrao_ti,
    kpi_contagem_coluna,
    ranking_ti,
)


def render():
    WORKSPACE = "ti"
    if not usuario_tem_acesso(WORKSPACE):
        st.error("🚫 Você não tem acesso a este módulo")
        st.stop()

    st.set_page_config(layout="wide", page_title="Tickets por Clientes")
    apply_metric_style()
    apply_right_panel_style()
    render_page_title("Tickets por Clientes")

    # Base padronizada (mesa/cliente/estado/contrato/situacao/avaliacao/criado_em/fechado_em)
    df_raw = get_tickets_geral_base()

    # Filtros obrigatórios de nível página (como métricas em metrics/ti.py)
    df_raw = aplicar_filtro_pagina_mesa(df_raw, col_mesa="mesa")
    df_raw = aplicar_filtro_pagina_situacao_fechado(df_raw, col_situacao="situacao")

    col_principal, col_filtros = st.columns([4, 1])

    with col_filtros:
        st.markdown("### ⚙️ Filtros")
        st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

        data_ini, data_fim = render_filtro_periodo(
            df_raw,
            "fechado_em",
            "tickets_clientes_periodo",
            titulo_expander="📅 Período",
        )

        estados_sel = render_filtro_multiselect(
            df_raw,
            "estado",
            "Selecione os Estados",
            titulo_expander="📍 Estado",
            chave="tickets_clientes_estados",
        )

        clientes_sel = render_filtro_hierarquico_clientes(
            df_raw,
            col_status="contrato",
            col_cliente="cliente",
            chave="tickets_clientes_clientes",
            titulo_header="🤝 Clientes por Contrato",
        )

        st.markdown("</div>", unsafe_allow_html=True)

    filtros_valores = {}
    if estados_sel:
        filtros_valores["estado"] = [str(x) for x in estados_sel]

    df = aplicar_filtros_padrao_ti(
        df_raw,
        data_col="fechado_em",
        data_ini=data_ini,
        data_fim=data_fim,
        filtros_valores=filtros_valores or None,
        clientes_sel=clientes_sel,
        col_cliente="cliente",
    )

    if df.empty:
        st.info("Nenhum dado encontrado para os filtros selecionados.")
        return

    with col_principal:
        # --- KPI TOPO: Contagem de Situação (linhas com situacao preenchida) ---
        with st.expander("Tickets Fechados", expanded=True):
            render_kpi_total(kpi_contagem_coluna(df, col="situacao"))

        st.markdown("---")

        # --- 1ª FILEIRA: Ranking por Mesa + Ranking por Entidade ---
        g1, g2 = st.columns(2)

        with g1:
            with st.expander("Ranking de Tickets por Mesa", expanded=True):
                if {"mesa", "cliente"}.issubset(df.columns):
                    df_mesa = ranking_ti(df, by="mesa", value_col="cliente", how="count", out_col="total_tickets")
                    df_mesa = df_mesa.sort_values("total_tickets", ascending=False).reset_index(drop=True)
                    render_grafico_barras_ranking(df_mesa, "mesa", "total_tickets", altura=380)
                else:
                    st.info("Colunas 'mesa' e/ou 'cliente' não disponíveis.")

        with g2:
            with st.expander("Ranking de Tickets por Cliente", expanded=True):
                if {"cliente", "situacao"}.issubset(df.columns):
                    df_cliente = ranking_ti(df, by="cliente", value_col="situacao", how="count", out_col="total_tickets")
                    df_cliente = df_cliente.sort_values("total_tickets", ascending=False).reset_index(drop=True)
                    render_grafico_ranking(df_cliente, "total_tickets", "cliente", altura=380)
                else:
                    st.info("Colunas 'cliente' e/ou 'situacao' não disponíveis.")

        st.markdown("---")

        # --- 2ª FILEIRA: Rosca por Mesa + Ranking de Avaliação ---
        g3, g4 = st.columns(2)

        with g3:
            with st.expander("Tickets por Mesa", expanded=True):
                if "mesa" in df.columns:
                    render_grafico_donut(df, "mesa", "Mesa", hole=0.6)
                else:
                    st.info("Coluna 'mesa' não disponível.")

        with g4:
            with st.expander("Avaliação dos Tickets", expanded=True):
                if "avaliacao" in df.columns and not df["avaliacao"].dropna().empty:
                    df_aval = ranking_ti(df, by="avaliacao", value_col="avaliacao", how="count", out_col="total")
                    df_aval = df_aval.sort_values("total", ascending=False).reset_index(drop=True)
                    render_grafico_barras_ranking(df_aval, "avaliacao", "total", altura=380)
                else:
                    st.info("Coluna 'avaliacao' não disponível ou sem dados.")

        st.markdown("---")

        # --- 3ª FILEIRA: Evolução Mensal ---
        with st.expander("Evolução Mensal do Total de Tickets", expanded=True):
            if "fechado_em" in df.columns and not df.empty:
                render_grafico_evolucao_mensal(df, "fechado_em", altura=380)
            else:
                st.info("Coluna 'fechado_em' não disponível.")