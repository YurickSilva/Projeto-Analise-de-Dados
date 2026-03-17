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

    col_main, col_filters = st.columns([4, 1])

    with col_filters:
        st.subheader("🔎 Filtros")
        filtros = filtro_periodo("Emitido_em")

    with col_main:

        df = operacoes_financeiras()
        valor = receita_mercadoria(df, filtros)

        c1, c2, c3 = st.columns(3)

        with c1:
            card_kpi_rs("Receita de Mercadoria", valor)

        with c2:
            card_kpi_rs("Receita (sem filtro)", receita_mercadoria(df))