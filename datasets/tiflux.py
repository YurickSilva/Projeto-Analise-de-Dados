import streamlit as st
from datasets.loader import load_csv
import pandas as pd
from utils.logger import setup_logger

logger = setup_logger("datasets")

@st.cache_data(show_spinner="Carregando Tickets...")
def tickets():  
    logger.info("Solicitado dataset tiflux.tickets")
    df = load_csv(sistema="Tiflux", tabela="Tiflux_tb_Tickets")
    df["Criado_em"] = pd.to_datetime(df["Criado_em"], format="mixed", errors='coerce')
    df["Fechado_em"] = pd.to_datetime(df["Fechado_em"], format="mixed", errors='coerce')
    return df

@st.cache_data(show_spinner="Carregando Clientes...")
def clientes():  
    logger.info("Solicitado dataset tiflux.clientes")
    df = load_csv(sistema="Tiflux", tabela="Tiflux_tb_Clientes")
    return df

@st.cache_data(show_spinner="Carregando Apontamentos...")
def apontamentos():  
    logger.info("Solicitado dataset tiflux.apontamentos")
    df = load_csv(sistema="Tiflux", tabela="Tiflux_tb_Apontamentos")
    if "Data_apontamento" in df.columns:
        df["Data_apontamento"] = pd.to_datetime(df["Data_apontamento"], format="mixed", errors='coerce')
    return df

@st.cache_data(show_spinner="Carregando Valores Extras...")
def valores_extras():  
    logger.info("Solicitado dataset tiflux.valores_extras")
    try:
        df = load_csv(sistema="Tiflux", tabela="Tiflux_tb_Valores_extras")
    except FileNotFoundError:
        # Caso o mocker ainda não gere essa tabela, retorna um DF vazio para não quebrar o Streamlit
        logger.warning("Tabela Valores_extras não encontrada. Retornando DataFrame vazio.")
        return pd.DataFrame()
    return df