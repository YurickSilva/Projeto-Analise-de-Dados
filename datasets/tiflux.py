import streamlit as st
from datasets.loader import load_csv
import pandas as pd
from utils.logger import setup_logger

logger = setup_logger("datasets")

# --- DOCUMENTAÇÃO ---
# Adicionamos @st.cache_data em TODAS as funções.
# Adicionamos a conversão de datas dentro do cache para evitar processamento repetitivo no render().

@st.cache_data(show_spinner="Carregando Tickets...")
def tickets():  
    logger.info("Solicitado dataset tiflux.tickets")
    df = load_csv(sistema="Tiflux", tabela="Tiflux_tb_Tickets")
    # Conversão centralizada (format="mixed" lida com diferentes padrões de data no CSV)
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
    # Converter data de apontamento aqui também é vital para evitar crashes em gráficos temporais
    if "Data_apontamento" in df.columns:
        df["Data_apontamento"] = pd.to_datetime(df["Data_apontamento"], format="mixed", errors='coerce')
    return df

@st.cache_data(show_spinner="Carregando Valores Extras...")
def valores_extras():  
    logger.info("Solicitado dataset tiflux.valores_extras")
    df = load_csv(sistema="Tiflux", tabela="Tiflux_tb_Valores_extras")
    return df