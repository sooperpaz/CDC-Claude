"""
KPI calculations. Each function takes the already-filtered DataFrame and
returns a plain value, handling the empty-selection case explicitly so
app.py never has to special-case it.
"""

import pandas as pd


def total_births(df: pd.DataFrame) -> int:
    return int(df["births"].sum())


def geography_count(df: pd.DataFrame) -> int:
    return df["state_of_residence"].nunique()


def avg_births_per_month(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    by_month = df.groupby("month", observed=True)["births"].sum()
    return float(by_month.mean()) if not by_month.empty else 0.0


def top_geography(df: pd.DataFrame) -> tuple[str, int] | None:
    if df.empty:
        return None
    by_state = df.groupby("state_of_residence")["births"].sum()
    top = by_state.idxmax()
    return top, int(by_state.loc[top])


def top_month(df: pd.DataFrame) -> tuple[str, int] | None:
    if df.empty:
        return None
    by_month = df.groupby("month", observed=True)["births"].sum()
    top = by_month.idxmax()
    return str(top), int(by_month.loc[top])
