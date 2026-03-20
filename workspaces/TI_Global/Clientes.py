import streamlit as st
import pandas as pd
from auth.authorization import usuario_tem_acesso
from datasets.tiflux import clientes 
from utils.styles import render_page_title, apply_metric_style
from components.graphs import render_kpi_total, render_grafico_donut, render_grafico_area_acumulada
from components.tables import render_tabela_generica
from metrics.interatividade import registrar_interatividade, filtrar_dados_do_mural, render_barra_limpeza_mural
from metrics.ti import get_clientes_metricas, get_clientes_ativos

def render():
    # 1. Setup
    
    WORKSPACE = "ti"

    if not usuario_tem_acesso(WORKSPACE):
        st.error("🚫 Você não tem acesso a este módulo")
        st.stop()
        
    render_page_title("Dashboard de Clientes")
    apply_metric_style()
    ID_PAGINA = "clientes_page"

    # 2. Carga via Métrica
    df_raw = get_clientes_metricas()
    df_base_pagina = df_raw.copy()

    # --- NOVO BOTÃO DE LIMPEZA ---
    # Ele aparece e desaparece automaticamente
    render_barra_limpeza_mural()

    # 3. DIVISÃO DO LAYOUT EM COLUNAS MESTRAS (Esquerda: Gráficos | Direita: Tabela)
    col_visuais, col_tabela = st.columns([2, 1])

    # 4. COLUNA DA ESQUERDA: VISUAIS
    with col_visuais:
        # Cruzamento com Mural (Filtros que vêm da tabela)
        df_visual_final = filtrar_dados_do_mural(df_base_pagina, sera_afetado=True)

        # --- KPI ---
        with st.container():
            st.markdown(
                """
                <p style='text-align: center; color: gray; font-size: 1.1rem; font-weight: bold; margin-bottom: -15px;'>
                    TOTAL DE CLIENTES
                </p>
                """, 
                unsafe_allow_html=True
            )
            render_kpi_total(len(df_visual_final))

        # --- GRÁFICOS DONUT ---
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("Contagem de Clientes por UF", expanded=True):
                if not df_visual_final.empty:
                    render_grafico_donut(
                        df_visual_final, 'estado', 'UF', 
                        show_legend=True, text_info='percent', text_position='inside',
                        margin=dict(t=30, b=10, l=10, r=100)
                    )
                else:
                    st.info("Sem dados.")
        with c2:
            with st.expander("Contagem de Cliente por Contrato", expanded=True):
                if not df_visual_final.empty:
                    render_grafico_donut(
                        df_visual_final, 'contrato', 'Status',
                        margin=dict(t=30, b=20, l=60, r=60)
                    )
                else:
                    st.info("Sem dados.")

        # --- ÁREA ACUMULADA ---
        with st.expander("Total Acumulado de Cliente com Contrato", expanded=True):
            df_ativos = get_clientes_ativos(df_visual_final)
            if not df_ativos.empty:
                render_grafico_area_acumulada(df_ativos, 'ano', 'contagem')
            else:
                st.info("Sem dados para os filtros selecionados.")

    # 5. COLUNA DA DIREITA: TABELA (LISTA COMPLETA)
    with col_tabela:
        st.markdown("<p style='font-weight: bold; color: gray;'>📋 LISTA DE CLIENTES</p>", unsafe_allow_html=True)
        
        # Filtramos o DF que vai para a tabela
        df_tab = filtrar_dados_do_mural(df_base_pagina, sera_afetado=True, id_proprio="tabela_clientes")
        
        # Mapeamento estrito: só estas colunas aparecerão, mas o AgGrid mantém os dados ocultos para filtro
        mapeamento = {
            "nome": "Cliente", 
        }
        
        # Chamada otimizada do teu componente
        response = render_tabela_generica(
            df=df_tab, 
            mapeamento_nomes=mapeamento, 
            altura=900 # Ajuste fino para alinhar com os gráficos da esquerda
        )
        
        sel_tab = response.get('selected_rows', [])
        
        # REGISTRO: O clique aqui filtra os KPIs e Gráficos da esquerda
        registrar_interatividade("tabela_clientes", sel_tab, vai_afetar=True, coluna_alvo="nome")