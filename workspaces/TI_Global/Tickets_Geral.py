from auth.authorization import usuario_tem_acesso
import streamlit as st
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
    render_grafico_linha,
    render_grafico_donut_sla,
)
from components.tables import render_tabela_generica
from metrics.ti import (
    get_tickets_geral_base_com_filtros,
    filtrar_tickets_geral,
    kpi_contagem_coluna,
    ranking_ti,
    serie_anual_ti,
)

def render():

    WORKSPACE = "ti"
    if not usuario_tem_acesso(WORKSPACE):
        st.error("🚫 Você não tem acesso a este módulo")
        st.stop()

    st.set_page_config(layout="wide", page_title="Visão Geral de Tickets")
    apply_metric_style()
    apply_right_panel_style()
    render_page_title("Visão Geral de Tickets")

    df_raw = get_tickets_geral_base_com_filtros()

    col_principal, col_filtros = st.columns([4, 1])

    with col_filtros:
        st.markdown("### ⚙️ Filtros")
        st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

        data_ini, data_fim = render_filtro_periodo(
            df_raw, "criado_em", "geral_periodo", titulo_expander="📅 Período"
        )

        estados_sel = render_filtro_multiselect(
            df_raw,
            "estado",
            "Selecione os Estados",
            titulo_expander="📍 Estado",
            chave="geral_est_multi",
        )

        clientes_sel = render_filtro_hierarquico_clientes(
            df_raw,
            col_status="contrato",
            col_cliente="cliente",
            chave="geral_clientes",
            titulo_header="🤝 Clientes por Contrato",
        )

        st.markdown("</div>", unsafe_allow_html=True)

    df = filtrar_tickets_geral(
        df_raw,
        data_ini,
        data_fim,
        estados=estados_sel,
        clientes_sel=clientes_sel,
    )

    if df.empty:
        st.info("Nenhum dado encontrado para os filtros selecionados.")
        return

    # --- CÁLCULOS DE MÉTRICAS ---
    # KPI deve contar explicitamente a coluna situacao
    total_tickets = kpi_contagem_coluna(df, col="situacao")
    duracao_media_minutos = df["duracao_media_minutos"].iloc[0] if "duracao_media_minutos" in df.columns and not df.empty else 0
    with col_principal:
        # --- TOPO: KPIs ---
        c1, c2 = st.columns(2)

        with c1:
            with st.expander("Tickets Fechados", expanded=True):
                render_kpi_total(total_tickets)

        with c2:
            with st.expander("Duração Média (minutos)", expanded=True):
                render_kpi_total(f"{duracao_media_minutos:.1f}")

        st.markdown("---")

        # --- PRIMEIRA FILEIRA: AVALIAÇÃO E EVOLUÇÃO ANUAL ---
        g1, g2 = st.columns(2)

        with g1:
            with st.expander("Avaliação de Tickets", expanded=True):
                if "avaliacao" in df.columns and not df.empty:
                    df_aval = ranking_ti(df, by="avaliacao", how="size", out_col="contagem")
                    render_grafico_barras_ranking(df_aval, "avaliacao", "contagem")
                else:
                    st.info("Coluna de avaliação não disponível.")

        with g2:
            with st.expander("Tickets por Mesa", expanded=True):
                if "mesa" in df.columns and "cliente" in df.columns and not df.empty:
                    df_mesa = ranking_ti(df, by="mesa", value_col="cliente", how="nunique", out_col="total_clientes")
                    render_grafico_barras_ranking(df_mesa, "mesa", "total_clientes")
                else:
                    st.info("Coluna de data de fechamento não disponível.")

        st.markdown("---")

        # --- SEGUNDA FILEIRA: SLA E MESA ---
        m1, m2 = st.columns(2)

        with m1:
            with st.expander("Atendeu SLA", expanded=True):
                if "sla" in df.columns and not df.empty:
                    # Filtrar apenas Sim e Não para o gráfico de rosca
                    df_sla = df[df["sla"].isin(["Sim", "Não"])].copy()
                    if not df_sla.empty:
                        render_grafico_donut_sla(df_sla, "sla")
                    else:
                        st.info("Nenhum dado de SLA (Sim/Não) disponível.")
                else:
                    st.info("Coluna de SLA não disponível.")

        with m2:
            with st.expander("Tickets por Ano", expanded=True):
                if "fechado_em" in df.columns and not df.empty:
                    df_ano = serie_anual_ti(df, date_col="fechado_em", out_col="contagem")
                    if not df_ano.empty:
                        render_grafico_linha(df_ano, "ano", "contagem", show_legend=False)
                    else:
                        st.info("Sem dados de ano disponíveis.")
                else:
                    st.info("Colunas de mesa ou cliente não disponíveis.")

        st.markdown("---")

        with st.expander("Top Problemas", expanded=True):
            if "Item" in df.columns and "cliente" in df.columns and not df.empty:
                df_item_cliente = ranking_ti(df, by="Item", value_col="cliente", how="nunique", out_col="total_clientes")
                df_item_cliente = df_item_cliente.sort_values("total_clientes", ascending=False).reset_index(drop=True)
                mapeamento_cols = {"Item": "Item", "total_clientes": "Total de Clientes"}
                render_tabela_generica(df_item_cliente, mapeamento_nomes=mapeamento_cols, altura=400)
            else:
                st.info("Colunas de item ou cliente não disponíveis.")