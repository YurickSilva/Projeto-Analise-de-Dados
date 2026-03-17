def render():
    import streamlit as st

    from datasets.company import operacoes_financeiras
    from metrics.controladoria import receita_mercadoria
    from components.cards import card_kpi_rs
    from components.filters import filtro_periodo
    from auth.authorization import usuario_tem_acesso

    WORKSPACE = "controladoria"

    if not usuario_tem_acesso(WORKSPACE):
        st.error("🚫 Você não tem acesso a este módulo")
        st.stop()

    st.title("📈 Controladoria")

    df = operacoes_financeiras()

    filtros = filtro_periodo("Emitido_em")
    valor = receita_mercadoria(df, filtros)

    col1, col2, col3 = st.columns(3)

    with col1:
        card_kpi_rs("Receita de Mercadoria", valor)

    with col2:
        card_kpi_rs(
            "Receita (sem filtro)",
            receita_mercadoria(df)
        )