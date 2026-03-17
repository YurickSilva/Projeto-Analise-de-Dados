import json
import streamlit as st
import pandas as pd

# --- LÓGICA DO MAPA ---
def get_selecao(id_pagina):
    return st.session_state.get(f"sel_{id_pagina}")

def set_selecao(id_pagina, valor):
    chave = f"sel_{id_pagina}"
    if st.session_state.get(chave) != valor:
        st.session_state[chave] = valor
        st.rerun()

def limpar_selecao(id_pagina):
    st.session_state[f"sel_{id_pagina}"] = None
    st.rerun()

def render_barra_selecao(id_pagina):
    selecionado = get_selecao(id_pagina)
    if selecionado:
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.info(f"📍 **Filtro de Mapa Ativo:** Exibindo dados do Ticket **{selecionado}**")
        with col2:
            if st.button("Limpar ❌", key=f"btn_clean_{id_pagina}", use_container_width=True):
                limpar_selecao(id_pagina)

# --- LÓGICA DO MURAL ---
def registrar_interatividade(id_componente, selecao, vai_afetar, coluna_alvo=None):
    if not vai_afetar: return
    if "mural_interativo" not in st.session_state:
        st.session_state.mural_interativo = {}

    def selecoes_sao_iguais(antiga, nova):
        if antiga is None and nova is None: return True
        if antiga is None or nova is None: return False
        try:
            if isinstance(antiga, pd.DataFrame) and isinstance(nova, pd.DataFrame):
                return antiga.equals(nova)
            return json.dumps(antiga, sort_keys=True) == json.dumps(nova, sort_keys=True)
        except: return False

    chave_cache = f"last_sel_{id_componente}"
    if selecoes_sao_iguais(st.session_state.get(chave_cache), selecao):
        return

    st.session_state[chave_cache] = selecao
    
    # Verifica se há conteúdo real
    tem_conteudo = len(selecao) > 0 if isinstance(selecao, (list, pd.DataFrame)) else bool(selecao)

    if tem_conteudo:
        st.session_state.mural_interativo[id_componente] = {"valor": selecao, "coluna": coluna_alvo}
    else:
        st.session_state.mural_interativo.pop(id_componente, None)
    
    st.rerun()

def filtrar_dados_do_mural(df_base, sera_afetado, id_proprio=None):
    if not sera_afetado or "mural_interativo" not in st.session_state:
        return df_base

    df_filtrado = df_base.copy()
    mural = st.session_state.mural_interativo

    for id_origem, info in mural.items():
        if id_proprio and id_origem == id_proprio: continue
        
        valor = info["valor"]
        coluna = info["coluna"]
        if not coluna or coluna not in df_filtrado.columns: continue

        if isinstance(valor, (list, pd.DataFrame)):
            df_sel = pd.DataFrame(valor)
            if coluna in df_sel.columns:
                df_filtrado = df_filtrado[df_filtrado[coluna].isin(df_sel[coluna])]
        elif valor:
            df_filtrado = df_filtrado[df_filtrado[coluna] == valor]

    return df_filtrado

def limpar_mural_completo():
    """Limpa todas as seleções de interatividade e caches de componentes."""
    # 1. Limpa o mural (o que filtra os gráficos)
    if "mural_interativo" in st.session_state:
        st.session_state.mural_interativo = {}
    
    # 2. Limpa os caches específicos de cada componente (ex: last_sel_tabela_clientes)
    # Buscamos todas as chaves que começam com 'last_sel_' e as removemos
    chaves_para_remover = [key for key in st.session_state.keys() if key.startswith("last_sel_")]
    for chave in chaves_para_remover:
        st.session_state.pop(chave, None)
    
    st.rerun()

def render_barra_limpeza_mural():
    """Renderiza um botão de limpeza apenas se houver algo filtrado no mural."""
    mural = st.session_state.get("mural_interativo", {})
    
    if mural: # Só mostra se o dicionário não estiver vazio
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.warning("⚡ **Filtro de Seleção Ativo:** A tabela está filtrando os gráficos.")
        with col2:
            if st.button("Limpar Tudo ❌", use_container_width=True, key="btn_clean_mural"):
                limpar_mural_completo()