import streamlit as st
from streamlit_tree_select import tree_select
import pandas as pd
from datetime import date

def filtro_periodo(coluna_data: str):
    st.sidebar.subheader("Filtro de Data")

    data_inicio = st.sidebar.date_input(
        "Data início",
        value=None
    )

    data_fim = st.sidebar.date_input(
        "Data fim",
        value=None
    )

    if not data_inicio and not data_fim:
        return None

    return {
        "coluna_data": coluna_data,
        "data_inicio": data_inicio,
        "data_fim": data_fim
    }

def render_filtro_periodo(df, col_data, chave_unica):
    """
    Renderiza um slider de data com visual de cartões brancos.
    - df: DataFrame de origem.
    - col_data: Nome da coluna de data (ex: 'Criado_em').
    - chave_unica: ID exclusivo para o widget.
    """
    datas_validas = pd.to_datetime(df[col_data]).dt.date.dropna()
    
    if not datas_validas.empty:
        min_base = datas_validas.min()
        max_base = datas_validas.max()
    else:
        min_base = max_base = date.today()

    if min_base == max_base:
        st.info("Apenas uma data disponível.")
        return min_base, max_base

    selecao = st.slider(
        "Arraste para ajustar o período", 
        min_value=min_base, 
        max_value=max_base, 
        value=(min_base, max_base), 
        format="DD/MM/YYYY",
        key=chave_unica
    )
    
    # Renderização visual das caixas brancas (estilo cartão)
    c1, c2 = st.columns(2)
    estilo_card = """
        <div style="background-color: white; padding: 8px; border-radius: 5px; 
             border: 1px solid #ddd; text-align: center; color: #fe5000; 
             font-weight: bold; font-size: 0.9rem; box-shadow: 1px 1px 3px rgba(0,0,0,0.1);">
            {data}
        </div>
    """
    
    with c1:
        st.caption("Início")
        st.markdown(estilo_card.format(data=selecao[0].strftime('%d/%m/%Y')), unsafe_allow_html=True)
    with c2:
        st.caption("Fim")
        st.markdown(estilo_card.format(data=selecao[1].strftime('%d/%m/%Y')), unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True) 
    return selecao[0], selecao[1]


def filtro_multiselect(df, col, label, default_list=None, chave="filtro_multi"):
    """
    Componente para seleção de múltiplos itens de uma coluna.
    - Se default_list for None: Seleciona TODOS por padrão.
    - Se o usuário remover todos os itens: Retorna lista vazia.
    """
    # Extrai valores únicos e ordena
    opcoes = sorted([str(x) for x in df[col].dropna().unique()])
    
    # Lógica de seleção padrão: 
    # Se não houver lista específica, o padrão é a lista completa de opções
    if default_list is None:
        valores_selecionados_padrao = opcoes 
    else:
        # Se houver lista, filtra apenas o que existe nas opções do DF
        valores_selecionados_padrao = [m for m in default_list if m in opcoes]
    
    return st.multiselect(label, options=opcoes, default=valores_selecionados_padrao, key=chave)

def filtro_selectbox(df, col, label, incluir_todos=True, chave="filtro_select"):
    """
    Filtro de seleção única em lista suspensa.
    - incluir_todos: Adiciona a opção "Todos" no topo da lista.
    """
    opcoes = sorted([str(x) for x in df[col].dropna().unique()])
    if incluir_todos:
        opcoes = ["Todos"] + opcoes
    return st.selectbox(label, options=opcoes, key=chave)

def filtro_radio(label, opcoes, chave="filtro_radio"):
    """
    Filtro de seleção única por botões circulares.
    Retorna apenas o valor selecionado.
    """
    return st.radio(label, options=opcoes, key=chave)

def filtro_hierarquico_clientes(df, col_status, col_cliente, chave):
    """
    Cria uma árvore hierárquica (Slicer) Estilo Power BI.
    - Status (Sim, Não, Rescindido) são os nós pais.
    - Clientes são os nós filhos.
    """
    st.markdown("### Contrato e Clientes")
    
    # 1. Montar a estrutura de nodes para a árvore
    nodes = []
    # Ordenamos os status para ficarem organizados
    status_opcoes = sorted([str(x) for x in df[col_status].dropna().unique()])
    
    for status in status_opcoes:
        # Clientes pertencentes a este status específico
        clientes_do_status = sorted([str(x) for x in df[df[col_status] == status][col_cliente].dropna().unique()])
        
        # Estrutura: label , value
        node = {
            "label": status,
            "value": status,
            "children": [{"label": c, "value": c} for c in clientes_do_status]
        }
        nodes.append(node)
    
    # 2. Renderizar a árvore
    # check_model='leaf' foca em retornar os valores finais 
    return_select = tree_select(
        nodes, 
        check_model="leaf", 
        direction="ltr",
        key=chave
    )
    
    # 3. Retornar a lista de selecionados
    # Se não houver nada, retorna lista vazia
    clientes_selecionados = return_select.get("checked", [])
    
    return clientes_selecionados