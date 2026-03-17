import streamlit as st
from datasets.loader import load_csv
import pandas as pd
from utils.logger import setup_logger

logger = setup_logger("datasets")

@st.cache_data(show_spinner="Carregando dados...")
def operacoes_financeiras():  
    logger.info("Solicitado dataset company.operacoes_financeiras")
    
    df = load_csv(sistema="Company", tabela="Company_tb_Operacoes_Financeiras")
    df["Emitido_em"] = pd.to_datetime(df["Emitido_em"])
    df["Valor_total"] = df["Valor_total"].astype(float)
    return df