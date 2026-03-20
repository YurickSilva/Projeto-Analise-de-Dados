import pandas as pd
from metrics.base import aplicar_filtros
from metrics.agg import ranking, serie_anual_contagem, serie_trimestral_contagem
from datasets.tiflux import tickets, clientes, apontamentos
import streamlit as st


@st.cache_data
def filtro_pagina_mesas_permitidas() -> list[str]:
    # Mantido como métrica (reuso em páginas) conforme padrão do projeto
    return [
        "Ativacao",
        "Help-Desk",
        "Labin",
        "On Site SSP",
        "On Site TI",
        "Telefonia",
        "Infraestrutura"
    ]


@st.cache_data
def aplicar_filtro_pagina_mesa(df: pd.DataFrame, *, col_mesa: str = "mesa") -> pd.DataFrame:
    if df is None or df.empty or col_mesa not in df.columns:
        return df
    mesas = filtro_pagina_mesas_permitidas()
    return df[df[col_mesa].isin(mesas)].copy()


@st.cache_data
def aplicar_filtro_pagina_situacao_fechado(
    df: pd.DataFrame,
    *,
    col_situacao: str = "situacao",
    valor_fechado: str = "FECHADO",
) -> pd.DataFrame:
    if df is None or df.empty or col_situacao not in df.columns:
        return df
    return df[df[col_situacao].astype(str).str.upper() == valor_fechado].copy()


@st.cache_data
def kpi_contagem_coluna(df: pd.DataFrame, *, col: str | None = None) -> int:
    """
    KPI padrão: se col for informado, conta não-nulos dessa coluna; senão len(df).
    """
    if df is None or df.empty:
        return 0
    if col and col in df.columns:
        return int(df[col].count())
    return int(len(df))


@st.cache_data
def aplicar_filtros_padrao_ti(
    df: pd.DataFrame,
    *,
    data_col: str,
    data_ini,
    data_fim,
    filtros_valores: dict | None = None,
    clientes_sel: list[str] | None = None,
    col_cliente: str = "cliente",
) -> pd.DataFrame:
    """
    Wrapper TI em cima de metrics.base.aplicar_filtros.
    - Filtra período (datetime) de forma consistente
    - Aplica filtros_valores (equals/isin)
    - Aplica clientes_sel (isin) quando fornecido
    """
    if df is None or df.empty:
        return df

    df_f = aplicar_filtros(
        df,
        coluna_data=data_col,
        data_inicio=data_ini,
        data_fim=data_fim,
        filtros_valores=filtros_valores,
    ).copy()

    if clientes_sel and col_cliente in df_f.columns:
        df_f = df_f[df_f[col_cliente].isin(clientes_sel)].copy()

    return df_f


@st.cache_data
def ranking_ti(
    df: pd.DataFrame,
    *,
    by: str,
    value_col: str | None = None,
    how: str = "size",
    out_col: str = "total",
    top_n: int | None = None,
) -> pd.DataFrame:
    return ranking(df, by=by, value_col=value_col, how=how, out_col=out_col, top_n=top_n)


@st.cache_data
def serie_anual_ti(df: pd.DataFrame, *, date_col: str, out_col: str = "total") -> pd.DataFrame:
    return serie_anual_contagem(df, date_col=date_col, out_col=out_col)


@st.cache_data
def serie_trimestral_ti(
    df: pd.DataFrame,
    *,
    date_col: str,
    out_col: str = "total",
    fill_missing: bool = True,
) -> pd.DataFrame:
    return serie_trimestral_contagem(df, date_col=date_col, out_col=out_col, fill_missing=fill_missing)


@st.cache_data
def adicionar_tempo_decorrido_cols(
    df: pd.DataFrame,
    *,
    col_inicio: str = "Criado_em",
    col_fim: str = "Fechado_em",
    out_dias: str = "Diferenca_dias_corridos",
    out_flag: str = "Atencao",
    limite_dias: int = 30,
) -> pd.DataFrame:
    """
    Enriquecimento padrão do Tempo Decorrido:
    - diferença em dias corridos
    - flag de atenção (>limite_dias)
    """
    if df is None or df.empty:
        return df
    if col_inicio not in df.columns or col_fim not in df.columns:
        return df

    out = df.copy()
    out[out_dias] = (out[col_fim] - out[col_inicio]).dt.days
    out[out_flag] = out[out_dias].apply(lambda x: "VERIFICAR" if pd.notna(x) and x > limite_dias else "Ok")
    return out
@st.cache_data
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
@st.cache_data
def calcular_total_apontamentos(df):
    return len(df)
@st.cache_data
def calcular_media_duracao(df):
    if df.empty or 'Duracao' not in df.columns: return 0
    return df['Duracao'].mean()
@st.cache_data
def contar_tecnicos_ativos(df):
    if df.empty or 'tecnico' not in df.columns: return 0
    return df['tecnico'].nunique()

@st.cache_data
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
@st.cache_data
def aplicar_filtros_obrigatorios_ti(df):
    if df.empty:
        return df
    
    # Verifica se as colunas existem antes de filtrar para evitar o crash
    cols_necessarias = ['Situacao', 'Mesa']
    for col in cols_necessarias:
        if col not in df.columns:
            # Se não achar 'Mesa', tenta procurar por 'Mesa_x' ou 'Mesa_y'
            raise KeyError(f"A coluna '{col}' não foi encontrada no DataFrame. Colunas disponíveis: {list(df.columns)}")

    mesas_permitidas = filtro_pagina_mesas_permitidas()
    
    return df[
        (df["Situacao"].astype(str).str.upper() == "FECHADO")
        & (df["Mesa"].isin(mesas_permitidas))
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
    
    # Aplicar filtros obrigatórios (como métricas reutilizáveis)
    df_filtrado = aplicar_filtro_pagina_mesa(df, col_mesa="mesa")
    df_filtrado = aplicar_filtro_pagina_situacao_fechado(df_filtrado, col_situacao="situacao")
    
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

@st.cache_data
def calcular_tempo_medio_atendimento(df_fechados: pd.DataFrame) -> float:
    """
    Calcula a duração média (minutos) por ticket usando a tabela de apontamentos.
    Recebe o DataFrame de tickets fechados (deve conter 'Id_ticket').
    Retorna média em minutos (float).
    """
    if df_fechados is None or df_fechados.empty:
        return 0.0

    df_apont = apontamentos()
    if df_apont.empty or 'Duracao' not in df_apont.columns or 'Id_ticket' not in df_fechados.columns:
        return 0.0

    df_apont_sum = df_apont.groupby('Id_ticket')['Duracao'].sum().reset_index(name='total_duracao')
    df_merge = df_fechados.merge(df_apont_sum, on='Id_ticket', how='left')
    total_dur = df_merge['total_duracao'].sum(skipna=True)
    total_tickets = len(df_fechados)
    return (total_dur / total_tickets) if total_tickets > 0 else 0.0

@st.cache_data
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
        ["Id_cliente", "Contrato", "Estado", "Situacao"]
    ].rename(columns={"Situacao": "Situacao_do_Cliente"})

    df = pd.merge(
        df_tickets,
        df_clientes_clean,
        on="Id_cliente",
        how="left",
    )

    df["Criado_em"] = pd.to_datetime(df["Criado_em"], errors="coerce")
    df["Fechado_em"] = pd.to_datetime(df.get("Fechado_em"), errors="coerce")

    return df


@st.cache_data(show_spinner="Carregando base de Tickets para Análise Temporal...")
@st.cache_data(show_spinner="Carregando base de Tickets para Análise Temporal...")
def get_tickets_tempo_base() -> pd.DataFrame:
    """
    Prepara a base de tickets para análise temporal com dados de clientes.
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
        }
    )

    df["criado_em"] = pd.to_datetime(df["criado_em"], errors="coerce")
    df["fechado_em"] = pd.to_datetime(df["fechado_em"], errors="coerce")

    return df


@st.cache_data(show_spinner="Carregando base de Tickets Temporal com Filtros...")
def get_tickets_tempo_base_com_filtros() -> pd.DataFrame:
    """
    Retorna base de tickets temporal com filtros obrigatórios de página:
    - Mesa: Ativação Agências, Help-Desk, LABIN, On-Site SSP, On-Site Ti, Telefonia
    - Situação: Fechado
    """
    df = get_tickets_tempo_base()
    
    df_filtrado = aplicar_filtro_pagina_mesa(df, col_mesa="mesa")
    df_filtrado = aplicar_filtro_pagina_situacao_fechado(df_filtrado, col_situacao="situacao")
    
    return df_filtrado

    return df

@st.cache_data
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


@st.cache_data
def filtrar_tempo_base(
    df: pd.DataFrame,
    data_ini,
    data_fim,
    estados=None,
    contratos=None,
) -> pd.DataFrame:
    """
    Filtra a base de tempo por período, estado e contrato.
    Se nenhum estado/contrato for selecionado, exibe todos.
    """
    df_f = df.copy()

    t_ini = pd.to_datetime(data_ini)
    t_fim = pd.to_datetime(data_fim).replace(hour=23, minute=59, second=59)

    df_f = df_f[(df_f["criado_em"] >= t_ini) & (df_f["criado_em"] <= t_fim)]

    if estados:
        df_f = df_f[df_f["estado"].isin([str(x) for x in estados])]
    if contratos:
        df_f = df_f[df_f["contrato"].isin([str(x) for x in contratos])]

    return df_f.copy()

@st.cache_data
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

@st.cache_data(show_spinner="Carregando base de Tickets Técnicos...")
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
            "Cliente": "cliente",
        }
    )

    # Conversão de data para garantir compatibilidade com filtros
    df["criado_em"] = pd.to_datetime(df["criado_em"], errors="coerce")

    return df


@st.cache_data(show_spinner="Carregando base de Tickets Técnicos com Filtros...")
def get_tickets_tecnicos_base_com_filtros() -> pd.DataFrame:
    """
    Retorna base de tickets técnicos com filtros obrigatórios de página:
    - Mesa: Ativação Agências, Help-Desk, LABIN, On-Site SSP, On-Site Ti, Telefonia
    - Situação: Fechado
    """
    df = get_tickets_tecnicos_base()
    
    df_filtrado = aplicar_filtro_pagina_mesa(df, col_mesa="mesa")
    df_filtrado = aplicar_filtro_pagina_situacao_fechado(df_filtrado, col_situacao="situacao")
    
    return df_filtrado
