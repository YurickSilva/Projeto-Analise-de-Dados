from metrics.base import aplicar_filtros
import pandas as pd

def receita_mercadoria(df: pd.DataFrame, filtros: dict | None = None) -> float:
    filtros = filtros or {}

    df_f = aplicar_filtros(
        df,
        coluna_data=filtros.get("coluna_data"),
        data_inicio=filtros.get("data_inicio"),
        data_fim=filtros.get("data_fim"),
        filtros_valores=filtros.get("filtros_valores")
    )

    mask = (
        (
            df_f["Desc_operacao"].str.contains(
                "VENDA DE MERCADORIA -", case=False, na=False
            )
            |
            df_f["Desc_operacao"].str.contains(
                "VENDA PARA ENTREGA FUTURA -", case=False, na=False
            )
        )
        &
        (df_f["Tipo_dado"] == "Venda")
    )

    return df_f.loc[mask, "Valor_total"].sum()

