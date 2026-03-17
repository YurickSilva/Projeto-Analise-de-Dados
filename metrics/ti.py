import pandas as pd
from metrics.base import aplicar_filtros
from datasets.tiflux import tickets, clientes, apontamentos
import streamlit as st

def contagem(df: pd.DataFrame, filtros: dict | None = None) -> int:
    filtros = filtros or {}

    df_f = aplicar_filtros(
        df,
        coluna_data=filtros.get("coluna_data"),
        data_inicio=filtros.get("data_inicio"),
        data_fim=filtros.get("data_fim"),
        filtros_valores=filtros.get("filtros_valores")
    )

    contagem = len(df_f)

    return contagem

def calcular_total_apontamentos(df):
    return len(df)

def calcular_media_duracao(df):
    if df.empty or 'Duracao' not in df.columns: return 0
    return df['Duracao'].mean()

def contar_tecnicos_ativos(df):
    if df.empty or 'tecnico' not in df.columns: return 0
    return df['tecnico'].nunique()


def filtrar_dados_atendimentos(df, data_ini, data_fim, tecnicos, estados, contrato, mesas, situacoes, clientes):
    df_f = df.copy()
    
    # 1. GARANTIR CONVERSÃO DA DATA
    df_f['Criado_em'] = pd.to_datetime(df_f['Criado_em'])
    
    # 2. FILTRO DE PERÍODO
    # Agora o .dt.date funcionará com segurança
    df_f = df_f[(df_f['Criado_em'].dt.date >= data_ini) & (df_f['Criado_em'].dt.date <= data_fim)]
    
    # 3. FILTROS MULTISELECT (Regra: Vazio = Nada exibe)
    df_f = df_f[df_f['Responsavel'].isin(tecnicos)]
    df_f = df_f[df_f['Estado'].isin(estados)]
    df_f = df_f[df_f['Mesa'].isin(mesas)]
    df_f = df_f[df_f['Situacao'].isin(situacoes)]
    
    # 4. FILTRO HIERÁRQUICO (Árvore de Clientes)
    # Aqui é aplicada a lista que veio da streamlit-tree-select
    df_f = df_f[df_f['Cliente'].isin(clientes)]
    
    return df_f

def aplicar_filtros_obrigatorios_ti(df):
    if df.empty:
        return df
    
    # Verifica se as colunas existem antes de filtrar para evitar o crash
    cols_necessarias = ['Situacao', 'Mesa']
    for col in cols_necessarias:
        if col not in df.columns:
            # Se não achar 'Mesa', tenta procurar por 'Mesa_x' ou 'Mesa_y'
            raise KeyError(f"A coluna '{col}' não foi encontrada no DataFrame. Colunas disponíveis: {list(df.columns)}")

    mesas_permitidas = ['Help-Desk', 'LABIN', 'On-Site SSP', 'On-Site Ti', 'Telefonia']
    
    return df[
        (df['Situacao'].str.upper() == 'FECHADO') & 
        (df['Mesa'].isin(mesas_permitidas))
    ].copy()


@st.cache_data(show_spinner="Carregando Tickets - Visão Geral...")
def get_tickets_geral_base() -> pd.DataFrame:
    """
    Prepara a base de tickets gerais enriquecida com dados de clientes
    e com nomes de colunas padronizados para os dashboards.
    """
    df_tickets = tickets()
    df_clientes = clientes()

    df = pd.merge(
        df_tickets,
        df_clientes[["Id_cliente", "Contrato", "Estado"]],
        on="Id_cliente",
        how="left",
    )

    df = df.rename(
        columns={
            "Criado_em": "criado_em",
            "Fechado_em": "fechado_em",
            "Cliente": "cliente",
            "Estado": "estado",
            "Contrato": "contrato",
            "Situacao": "situacao",
            "Mesa": "mesa",
            "Avaliacao": "avaliacao",
            "SLA_atendido": "sla",
        }
    )

    # Coluna de "problema" baseada no Item do catálogo
    if "Item" in df.columns and "problema" not in df.columns:
        df["problema"] = df["Item"]

    df["criado_em"] = pd.to_datetime(df["criado_em"], errors="coerce")
    df["fechado_em"] = pd.to_datetime(df["fechado_em"], errors="coerce")

    return df


@st.cache_data(show_spinner="Carregando base de Tickets Geral com Filtros...")
def get_tickets_geral_base_com_filtros() -> pd.DataFrame:
    """
    Retorna base de tickets com filtros obrigatórios de página:
    - Mesa: Ativação Agências, Help-Desk, LABIN, On-Site SSP, On-Site Ti, Telefonia
    - Situação: Fechado
    - Inclui cálculo de duração média
    """
    df = get_tickets_geral_base()
    df_apontamentos = apontamentos()
    
    # Aplicar filtros obrigatórios
    mesas_permitidas = ['Ativação Agências', 'Help-Desk', 'LABIN', 'On-Site SSP', 'On-Site Ti', 'Telefonia']
    
    df_filtrado = df[
        (df['mesa'].isin(mesas_permitidas)) & 
        (df['situacao'].astype(str).str.upper() == 'FECHADO')
    ].copy()
    
    # Calcular duração média via merge com apontamentos
    # Fórmula DAX: DIVIDE(SUM(Duração Minutos), COUNTA(Tickets[Situacao]))
    if not df_apontamentos.empty and 'Duracao' in df_apontamentos.columns:
        df_apont_dur = df_apontamentos[['Id_ticket', 'Duracao']].copy()
        df_apont_sumario = df_apont_dur.groupby('Id_ticket')['Duracao'].sum().reset_index(name='total_duracao')
        
        df_filtrado = df_filtrado.merge(df_apont_sumario, on='Id_ticket', how='left')
        total_duracao = df_filtrado['total_duracao'].sum()
        total_tickets = len(df_filtrado)
        
        duracao_media = total_duracao / total_tickets if total_tickets > 0 else 0
    else:
        duracao_media = 0
    
    # Adicionar coluna de duração média para todos os registros (será usada nos cartões)
    df_filtrado['duracao_media_minutos'] = duracao_media
    
    return df_filtrado


def filtrar_tickets_geral(
    df: pd.DataFrame,
    data_ini,
    data_fim,
    estados=None,
    contratos=None,
    clientes_sel=None,
) -> pd.DataFrame:
    df_f = df.copy()

    # --- AJUSTE AQUI: Garante que os limites sejam Timestamps do Pandas ---
    t_ini = pd.to_datetime(data_ini)
    t_fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)

    # Comparamos Datetime com Datetime (mais rápido e evita o erro)
    df_f = df_f[
        (df_f["criado_em"] >= t_ini) & (df_f["criado_em"] <= t_fim)
    ]

    if estados:
        df_f = df_f[df_f["estado"].isin([str(x) for x in estados])]
    if contratos:
        df_f = df_f[df_f["contrato"].isin([str(x) for x in contratos])]
    if clientes_sel:
        df_f = df_f[df_f["cliente"].isin(clientes_sel)]

    return df_f.copy()


@st.cache_data(show_spinner="Carregando base de Tickets Abertos...")
def get_tickets_abertos_base() -> pd.DataFrame:
    """
    Retorna a base de tickets enriquecida com Contrato/Estado do cadastro de clientes.
    """
    df_tickets = tickets()
    df_clientes = clientes()

    df = pd.merge(
        df_tickets,
        df_clientes[["Id_cliente", "Contrato", "Estado"]],
        on="Id_cliente",
        how="left",
    )

    df["Criado_em"] = pd.to_datetime(df["Criado_em"], errors="coerce")
    df["Criado_em_date"] = df["Criado_em"].dt.date

    for col in ["Estado", "Contrato", "Mesa", "Responsavel"]:
        if col in df.columns:
            df[col] = df[col].astype(str)

    return df


@st.cache_data(show_spinner="Carregando base de Tempo Decorrido...")
def get_tempo_decorrido_base() -> pd.DataFrame:
    """
    Base de tickets com informações de clientes preparada para o dashboard de Tempo Decorrido.
    """
    df_tickets = tickets()
    df_clientes = clientes()

    df_clientes_clean = df_clientes[
        ["Cliente", "Contrato", "Estado", "Situacao"]
    ].rename(columns={"Situacao": "Situacao_do_Cliente"})

    df = pd.merge(
        df_tickets,
        df_clientes_clean,
        on="Cliente",
        how="left",
    )

    df["Criado_em"] = pd.to_datetime(df["Criado_em"], errors="coerce")
    df["Fechado_em"] = pd.to_datetime(df.get("Fechado_em"), errors="coerce")

    return df


def filtrar_tempo_decorrido(
    df: pd.DataFrame,
    data_ini,
    data_fim,
    mesas,
    responsaveis,
    situacoes_ticket,
    estados,
    situacoes_cliente,
    clientes_sel=None,
) -> pd.DataFrame:
    df_f = df.copy()

    # --- AJUSTE AQUI ---
    t_ini = pd.to_datetime(data_ini)
    t_fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)

    mask = (df_f["Criado_em"] >= t_ini) & (df_f["Criado_em"] <= t_fim)
    # ------------------
    
    mask &= df_f["Mesa"].isin(mesas)
    mask &= df_f["Responsavel"].isin(responsaveis)
    mask &= df_f["Situacao"].isin(situacoes_ticket)
    mask &= df_f["Estado"].isin(estados)
    mask &= df_f["Situacao_do_Cliente"].isin(situacoes_cliente)

    if clientes_sel:
        mask &= df_f["Cliente"].isin(clientes_sel)

    return df_f[mask].copy()


def filtrar_tickets_abertos(
    df: pd.DataFrame,
    data_ini,
    data_fim,
    estados=None,
    mesas=None,
    responsaveis=None,
    clientes_sel=None,
) -> pd.DataFrame:
    df_f = df.copy()

    df_f = df_f[
        (df_f["Criado_em_date"] >= data_ini) & (df_f["Criado_em_date"] <= data_fim)
    ]

    if estados:
        df_f = df_f[df_f["Estado"].isin([str(x) for x in estados])]
    if mesas:
        df_f = df_f[df_f["Mesa"].isin([str(x) for x in mesas])]
    if responsaveis:
        df_f = df_f[df_f["Responsavel"].isin([str(x) for x in responsaveis])]
    if clientes_sel:
        df_f = df_f[df_f["Cliente"].isin(clientes_sel)]

    return df_f.copy()
    

@st.cache_data
def get_clientes_metricas():
    """
    Prepara a base de clientes com nomes padronizados e colunas de tempo.
    """
    df = clientes()
    
    # Padronização de nomes (CSV -> Código)
    df = df.rename(columns={
        'Estado': 'estado',
        'Contrato': 'contrato',
        'Cliente': 'nome',
        'Criado_em': 'data_criacao'
    })
    
    # Tratamento de Tempo
    df['data_criacao'] = pd.to_datetime(df['data_criacao'], errors='coerce')
    df['ano'] = df['data_criacao'].dt.year
    
    return df

@st.cache_data
def get_clientes_ativos(df):
    """
    Retorna apenas os clientes com contrato ativo.
    """
    # Filtramos ignorando maiúsculas/minúsculas e espaços
    return df[df['contrato'].astype(str).str.strip().str.lower() == 'sim'].copy()


def get_tickets_tecnicos_base() -> pd.DataFrame:
    """
    Prepara a base de tickets técnicos enriquecida com dados de clientes
    para o dashboard de performance de tickets técnicos.
    """
    df_tickets = tickets()
    df_clientes = clientes()

    df = pd.merge(
        df_tickets,
        df_clientes[["Id_cliente", "Contrato", "Estado"]],
        on="Id_cliente",
        how="left",
    )

    df = df.rename(
        columns={
            "Criado_em": "criado_em",
            "Estado": "estado",
            "Contrato": "contrato",
            "Situacao": "situacao",
            "Mesa": "mesa",
            "Avaliacao": "avaliacao",
            "Responsavel": "responsavel",
        }
    )

    return df
