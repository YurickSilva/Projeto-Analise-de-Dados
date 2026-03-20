import streamlit as st
import pandas as pd
import numpy as np
from auth.authorization import usuario_tem_acesso
from utils.styles import render_page_title, apply_metric_style, apply_right_panel_style

# Importação dos seus componentes de filtro base
from components.filters import (
    render_filtro_periodo, 
    render_filtro_multiselect, 
    render_filtro_hierarquico_clientes
)
from components.tables import render_tabela_generica
from components.graphs import render_kpi_total # Componente para renderizar o card

from metrics.ti import get_tempo_decorrido_base, filtrar_tempo_decorrido, adicionar_tempo_decorrido_cols

def render():
    if not usuario_tem_acesso("ti"):
        st.error("🚫 Acesso negado")
        st.stop()

    apply_metric_style()
    apply_right_panel_style()
    render_page_title("Tempo Decorrido de Atendimento")

    df_base = get_tempo_decorrido_base()

    # --- ESTRUTURA DE LAYOUT ---
    col_principal, col_filtros = st.columns([4, 1.2])

    # 2. COLUNA DE FILTROS (DIREITA)
    with col_filtros:
        st.markdown("### ⚙️ Filtros")
        st.markdown("<div class='right-panel'>", unsafe_allow_html=True)
        
        data_ini, data_fim = render_filtro_periodo(df_base, 'Criado_em', 't_dec_per_v3')
        mesas_sel = render_filtro_multiselect(df_base, 'Mesa', "Selecione as Mesas", "🖥️ Mesas", chave="f_mesa")
        resp_sel = render_filtro_multiselect(df_base, 'Responsavel', "Selecione os Responsáveis", "👤 Responsáveis", chave="f_resp")
        sit_tkt_sel = render_filtro_multiselect(df_base, 'Situacao', "Situação do Ticket", "📝 Situação Ticket", chave="f_sit_tkt")
        est_sel = render_filtro_multiselect(df_base, 'Estado', "Estado (UF)", "📍 Estado", chave="f_est")
        sit_cli_sel = render_filtro_multiselect(df_base, 'Situacao_do_Cliente', "Situação do Cliente", "🏢 Status Cliente", chave="f_sit_cli")

        clientes_sel = render_filtro_hierarquico_clientes(
            df_base, 
            col_status='Contrato', 
            col_cliente='Cliente', 
            chave='f_hierarquia_cli',
            titulo_header="🤝 Clientes por Contrato"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. PROCESSAMENTO E APLICAÇÃO DOS FILTROS
    df_filtrado = filtrar_tempo_decorrido(
        df_base,
        data_ini,
        data_fim,
        mesas=mesas_sel,
        responsaveis=resp_sel,
        situacoes_ticket=sit_tkt_sel,
        estados=est_sel,
        situacoes_cliente=sit_cli_sel,
        clientes_sel=clientes_sel,
    )

    # --- CÁLCULO DE MEDIDAS ---
    df_filtrado = adicionar_tempo_decorrido_cols(df_filtrado)

    # --- 4. ÁREA PRINCIPAL ---
    with col_principal:
        if not df_filtrado.empty:
            
            # --- CARD DE CONTAGEM CENTRALIZADO ---
            # Criamos 3 colunas e usamos a do meio para centralizar o KPI
            espaco_esq, col_central, espaco_dir = st.columns([1, 1, 1])
            with col_central:
                st.markdown("<p style='text-align: center; color: gray; margin-bottom: -10px; font-weight: bold;'>TOTAL TICKETS</p>", unsafe_allow_html=True)
                render_kpi_total(df_filtrado['Situacao'].count())

            st.markdown("---")
            
            # Mapeamento e Tabela
            mapeamento = {
                'Id_ticket': 'ID Ticket',
                'Atencao': 'Atenção',
                'Cliente': 'Cliente',
                'Mesa': 'Mesa',
                'Criado_em': 'Criado em',
                'Fechado_em': 'Fechado em',
                'Diferenca_dias_corridos': 'Diferença Dias Corridos',
                'Desc_ticket': 'Desc_ticket',
                'Duracao_apontada': 'Duracao_apontada (min)',
                #'Tempo_total_atendimento': 'Tempo_total_atendimento (h)',
                'Tempo_total_fechamento': 'Tempo_total_fechamento (h)',
                #'Tempo_total_SLA': 'Tempo_total_SLA'
            }
            
            colunas_validas = [c for c in mapeamento.keys() if c in df_filtrado.columns]
            
            render_tabela_generica(
                df_filtrado[colunas_validas],
                mapeamento_nomes=mapeamento,
                colunas_wrap=['Desc_ticket'],
                altura=700
            )
        else:
            st.info("Nenhum ticket encontrado para os critérios selecionados.")