import pandas as pd
from datetime import date, datetime

def filtrar_periodo(
    df: pd.DataFrame,
    coluna_data: str,
    data_inicio=None,
    data_fim=None
) -> pd.DataFrame:

    if coluna_data not in df.columns:
        raise ValueError(f"Coluna {coluna_data} não existe no DataFrame")

    df_filtrado = df.copy()

    # garantia na coluna datetime
    df_filtrado[coluna_data] = pd.to_datetime(
        df_filtrado[coluna_data],
        errors="coerce"
    )

    if data_inicio is not None:
        data_inicio = pd.to_datetime(data_inicio).normalize()

    if data_fim is not None:
        data_fim = (
            pd.to_datetime(data_fim)
            + pd.Timedelta(days=1)
            - pd.Timedelta(seconds=1)
        )

    if data_inicio is not None:
        df_filtrado = df_filtrado[df_filtrado[coluna_data] >= data_inicio]

    if data_fim is not None:
        df_filtrado = df_filtrado[df_filtrado[coluna_data] <= data_fim]

    return df_filtrado


def filtrar_valores(
    df: pd.DataFrame,
    filtros: dict | None
) -> pd.DataFrame:
    if not filtros:
        return df

    df_filtrado = df.copy()

    for coluna, valor in filtros.items():
        if coluna not in df.columns:
            continue

        if isinstance(valor, list):
            df_filtrado = df_filtrado[df_filtrado[coluna].isin(valor)]
        else:
            df_filtrado = df_filtrado[df_filtrado[coluna] == valor]

    return df_filtrado

def aplicar_filtros(
    df: pd.DataFrame,
    *,
    coluna_data: str | None = None,
    data_inicio=None,
    data_fim=None,
    filtros_valores: dict | None = None
) -> pd.DataFrame:

    df_filtrado = df

    if coluna_data:
        df_filtrado = filtrar_periodo(
            df_filtrado,
            coluna_data,
            data_inicio,
            data_fim
        )

    if filtros_valores:
        df_filtrado = filtrar_valores(
            df_filtrado,
            filtros_valores
        )

    return df_filtrado