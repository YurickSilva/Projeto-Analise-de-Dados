import pandas as pd


def ranking(
    df: pd.DataFrame,
    *,
    by: str,
    value_col: str | None = None,
    how: str = "size",  # size | count | nunique
    out_col: str = "total",
    ascending: bool = False,
    top_n: int | None = None,
    dropna: bool = True,
) -> pd.DataFrame:
    """
    Agregação padrão para rankings:
    - size: conta linhas
    - count: conta não-nulos de value_col
    - nunique: conta distintos de value_col
    Retorna DataFrame com colunas [by, out_col], ordenado.
    """
    if df is None or df.empty or by not in df.columns:
        return pd.DataFrame(columns=[by, out_col])

    base = df.dropna(subset=[by]).copy() if dropna else df.copy()

    if how == "size":
        s = base.groupby(by).size()
    else:
        if value_col is None or value_col not in base.columns:
            return pd.DataFrame(columns=[by, out_col])
        g = base.groupby(by)[value_col]
        if how == "count":
            s = g.count()
        elif how == "nunique":
            s = g.nunique(dropna=dropna)
        else:
            raise ValueError(f"how inválido: {how}")

    out = s.reset_index(name=out_col).sort_values(out_col, ascending=ascending)
    if top_n is not None:
        out = out.head(top_n)
    return out.reset_index(drop=True)


def serie_anual_contagem(df: pd.DataFrame, *, date_col: str, out_col: str = "total") -> pd.DataFrame:
    """
    Conta registros por ano (a partir de date_col).
    Retorna colunas: ano(str), out_col(int)
    """
    if df is None or df.empty or date_col not in df.columns:
        return pd.DataFrame(columns=["ano", out_col])

    t = pd.to_datetime(df[date_col], errors="coerce")
    anos = t.dt.year.dropna().astype(int)
    if anos.empty:
        return pd.DataFrame(columns=["ano", out_col])

    out = anos.value_counts().sort_index().reset_index()
    out.columns = ["ano", out_col]
    out["ano"] = out["ano"].astype(str)
    return out


def serie_trimestral_contagem(
    df: pd.DataFrame,
    *,
    date_col: str,
    out_col: str = "total",
    fill_missing: bool = True,
) -> pd.DataFrame:
    """
    Conta registros por trimestre e ano, com preenchimento (ano x T1..T4).
    Retorna colunas: ano(str), trimestre(int), T(str), out_col(int)
    """
    if df is None or df.empty or date_col not in df.columns:
        return pd.DataFrame(columns=["ano", "trimestre", "T", out_col])

    t = pd.to_datetime(df[date_col], errors="coerce")
    tmp = pd.DataFrame({"ano": t.dt.year, "trimestre": t.dt.quarter}).dropna()
    if tmp.empty:
        return pd.DataFrame(columns=["ano", "trimestre", "T", out_col])

    tmp["ano"] = tmp["ano"].astype(int)
    tmp["trimestre"] = tmp["trimestre"].astype(int)
    cont = tmp.groupby(["ano", "trimestre"]).size().reset_index(name=out_col)

    if fill_missing:
        anos = sorted(tmp["ano"].unique().tolist())
        esq = pd.MultiIndex.from_product([anos, [1, 2, 3, 4]], names=["ano", "trimestre"]).to_frame(index=False)
        cont = pd.merge(esq, cont, on=["ano", "trimestre"], how="left").fillna({out_col: 0})
        cont[out_col] = cont[out_col].astype(int)

    cont["T"] = cont["trimestre"].map({1: "T1", 2: "T2", 3: "T3", 4: "T4"})
    cont["ano"] = cont["ano"].astype(str)
    return cont.sort_values(["ano", "trimestre"]).reset_index(drop=True)

