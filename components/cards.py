import streamlit as st

def card_kpi(titulo: str, valor: float):
    st.metric(
        label=titulo,
        value=f"{valor:,.2f}"
    )

def card_kpi_rs(titulo: str, valor: float, prefixo="R$"):
    st.metric(
        label=titulo,
        value=f"{prefixo} {valor:,.2f}"
    )