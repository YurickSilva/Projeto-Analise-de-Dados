from auth.authorization import usuario_tem_acesso
import streamlit as st
import pandas as pd
from datasets import tiflux
from components.filters import render_filtro_multiselect, render_filtro_periodo, render_filtro_hierarquico_clientes
from components.tables import render_tabela_generica
from components.maps import render_mapa_atendimentos
from metrics.interatividade import get_selecao, render_barra_selecao, registrar_interatividade, filtrar_dados_do_mural
from utils.styles import render_page_title, apply_metric_style, apply_right_panel_style
from metrics.ti import aplicar_filtros_obrigatorios_ti

def render():
    
    WORKSPACE = "ti"

    if not usuario_tem_acesso(WORKSPACE):
        st.error("🚫 Você não tem acesso a este módulo")
        st.stop()

    # 1. Configurações Iniciais
    st.set_page_config(layout="wide", page_title="Sistema de Atendimentos")
    render_page_title("Atendimentos")
    apply_metric_style()
    apply_right_panel_style()

    ID_PAGINA = "atendimentos_page"

    df_tickets = tiflux.tickets()
    df_clientes = tiflux.clientes()
    df_apontamentos = tiflux.apontamentos()

    # Cruzamento 1: Apontamentos + Tickets
    # IMPORTANTE: Removi 'Mesa' de df_tickets para não dar conflito com a 'Mesa' de df_apontamentos
    df_merge = pd.merge(
        df_apontamentos, 
        df_tickets[['Id_ticket', 'Situacao', 'Desc_ticket', 'Responsavel', 'Prioridade']], 
        on='Id_ticket', 
        how='left'
    )

    # Cruzamento 2: + Clientes
    df_raw_bruto = pd.merge(
        df_merge, 
        df_clientes[['Cliente', 'Contrato', 'Estado']], 
        on='Cliente', 
        how='left'
    )

    # --- 3. CHAMADA DA MÉTRICA DE FILTRO FIXO ---
    df_raw = aplicar_filtros_obrigatorios_ti(df_raw_bruto)
    
    # Tratamento de data após o filtro
    df_raw['Data_apontamento'] = pd.to_datetime(df_raw['Data_apontamento']).dt.date

    col_principal, col_filtros = st.columns([4, 1])

    # --- 4. COLUNA DE FILTROS (DIREITA) ---
    with col_filtros:
        st.markdown("### ⚙️ Filtros")
        st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

        data_ini, data_fim = render_filtro_periodo(
            df_raw, 'Data_apontamento', 'chave_atend_periodo', 
            titulo_expander="📅 Período de Atendimento"
        )
        
        estados_sel = render_filtro_multiselect(
            df_raw, 'Estado', 'Filtrar por UF', 
            titulo_expander="🌎 Localização", 
            chave='atend_uf'
        )

        tecnicos_sel = render_filtro_multiselect(
            df_raw, 'Tecnico', 'Selecione os Técnicos', 
            titulo_expander="👤 Equipe Técnica", 
            chave='atend_tec'
        )

        with st.expander("Clientes por Contrato", expanded=False):
            clientes_sel = render_filtro_hierarquico_clientes(
                df_raw, 'Contrato', 'Cliente', 'tree_atend', 
                titulo_header="🏢 Estrutura de Clientes"
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 5. LÓGICA DE FILTRAGEM ---
    df_filtrado_base = df_raw[
        (df_raw['Data_apontamento'] >= data_ini) & 
        (df_raw['Data_apontamento'] <= data_fim)
    ].copy()

    # Aplicação do filtro de Estado
    if estados_sel:
        df_filtrado_base = df_filtrado_base[df_filtrado_base['Estado'].isin(estados_sel)]

    if tecnicos_sel:
        df_filtrado_base = df_filtrado_base[df_filtrado_base['Tecnico'].isin(tecnicos_sel)]

    if clientes_sel:
        df_filtrado_base = df_filtrado_base[df_filtrado_base['Cliente'].isin(clientes_sel)]

    # --- 6. COLUNA PRINCIPAL (ESQUERDA) ---
    with col_principal:
        sel_mapa_bruta = get_selecao(ID_PAGINA)
        registrar_interatividade("mapa", sel_mapa_bruta, vai_afetar=True, coluna_alvo="Id_ticket")

        render_barra_selecao(ID_PAGINA)

        with st.expander("📋 Detalhamento de Apontamentos", expanded=True):
            df_tabela = filtrar_dados_do_mural(df_filtrado_base, sera_afetado=True, id_proprio="tabela")

            response = render_tabela_generica(
                df_tabela[['Id_ticket', 'Desc_apontamento', 'Tecnico', 'Cliente', 'Latitude', 'Longitude', 'Contrato', 'Estado']], 
                mapeamento_nomes={
                    'Id_ticket': 'Ticket', 
                    'Desc_apontamento': 'Atividade',
                    'Tecnico': 'Técnico'
                },
                colunas_ocultas=['Latitude', 'Longitude', 'Contrato', 'Estado'],
                colunas_wrap=["Desc_apontamento"],
                altura=600
            )
            
            sel_tabela_bruta = response.get('selected_rows', [])
            registrar_interatividade("tabela", sel_tabela_bruta, vai_afetar=True, coluna_alvo="Id_ticket")

    # --- BLOCO DO MAPA COMENTADO ---
    """ 
    with col_principal: 
        with st.expander("🗺️ Localização dos Técnicos", expanded=True):
            df_mapa = filtrar_dados_do_mural(df_filtrado_base, sera_afetado=True, id_proprio="mapa")
            
            if not df_mapa.empty:
                render_mapa_atendimentos(
                    df_mapa, 
                    id_pagina=ID_PAGINA, 
                    response_atendimentos=response,
                    permite_clique=True 
                )
            else:
                st.info("Selecione um período ou técnico com coordenadas válidas.") 
    """