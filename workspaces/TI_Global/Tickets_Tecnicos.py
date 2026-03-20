from auth.authorization import usuario_tem_acesso
import streamlit as st
import pandas as pd
from utils.styles import (
    render_page_title, 
    apply_metric_style, 
    apply_right_panel_style
)
from components.filters import (
    render_filtro_periodo, 
    render_filtro_selectbox, 
    render_filtro_hierarquico_clientes,
    render_filtro_multiselect
)
from components.graphs import (
    render_kpi_total, 
    render_grafico_barras_ranking, 
    render_grafico_ranking, 
    render_grafico_evolucao_mensal
)
from metrics.ti import (
    get_tickets_tecnicos_base_com_filtros,
    calcular_tempo_medio_atendimento,
    aplicar_filtros_padrao_ti,
    kpi_contagem_coluna,
    ranking_ti,
)

def render():
    st.set_page_config(layout="wide", page_title="Tickets Técnicos")
    apply_metric_style()
    WORKSPACE = "ti"
    if not usuario_tem_acesso(WORKSPACE):
        st.error("🚫 Você não tem acesso a este módulo")
        st.stop()
    apply_right_panel_style()
    render_page_title("Performance de Tickets Técnicos")

    df_raw = get_tickets_tecnicos_base_com_filtros()

    col_principal, col_filtros = st.columns([4, 1])

    with col_filtros:
        st.markdown("### ⚙️ Filtros")
        st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

        data_ini, data_fim = render_filtro_periodo(df_raw, 'criado_em', 'perf_periodo', titulo_expander="📅 Período")

        with st.expander("🌍 Estado"):
            estado = render_filtro_selectbox(df_raw, 'estado', "Estado", chave="perf_est")

        tecnicos_sel = render_filtro_multiselect(df_raw, 'responsavel', "Selecionar Técnicos", chave="perf_tec", titulo_expander="👤Técnicos")
        
        clientes_sel = render_filtro_hierarquico_clientes(
            df_raw,
            col_status="contrato",
            col_cliente="cliente",
            chave="perf_clientes",
            titulo_header="🤝 Clientes por Contrato",
        )

        

        st.markdown("</div>", unsafe_allow_html=True)

    # --- LÓGICA ---
    filtros_valores = {}
    if estado != "Todos":
        filtros_valores["estado"] = estado
    if tecnicos_sel:
        filtros_valores["responsavel"] = tecnicos_sel

    df = aplicar_filtros_padrao_ti(
        df_raw,
        data_col="criado_em",
        data_ini=data_ini,
        data_fim=data_fim,
        filtros_valores=filtros_valores or None,
        clientes_sel=clientes_sel,
        col_cliente="cliente",
    )

    # --- LAYOUT ---
    with col_principal:
        if not df.empty:
            # `df_raw` já vem com filtro obrigatório (FECHADO); garantir robustez
            df_fechados = df.copy()

            c1, c2 = st.columns(2)
            with c1:
                with st.expander("Tickets Fechados", expanded=True):
                    render_kpi_total(kpi_contagem_coluna(df_fechados, col="situacao"))
            with c2:
                with st.expander("Tempo Médio de Atendimento", expanded=True):
                    # Usar métrica centralizada para calcular a duração média por ticket
                    duracao_media = calcular_tempo_medio_atendimento(df_fechados)
                    render_kpi_total(f"{int(round(duracao_media))} min")

            st.markdown("---")

            with st.expander("Ranking de Tickets Fechados", expanded=True):
                df_rank = ranking_ti(df_fechados, by="responsavel", how="size", out_col="total")
                render_grafico_ranking(df_rank, "total", "responsavel")


            st.markdown("---")

            b1, b2 = st.columns(2)
            with b1:
                with st.expander("Avaliação de Tickets", expanded=True):
                    df_aval = ranking_ti(df_fechados, by="avaliacao", how="size", out_col="qtd")
                    render_grafico_barras_ranking(df_aval, "avaliacao", "qtd", categorias_fixas=[1, 2, 3, 4, 5])
            with b2:
                with st.expander("Tickets por Mesa", expanded=True):
                    df_mesa = ranking_ti(df, by="mesa", how="size", out_col="total")
                    render_grafico_barras_ranking(df_mesa, "mesa", "total")
            st.markdown("---")

            with st.expander("Contagem de Chamados por Mês", expanded=True):
                render_grafico_evolucao_mensal(df, 'criado_em')
        else:
            st.info("Nenhum ticket encontrado para os filtros selecionados.")