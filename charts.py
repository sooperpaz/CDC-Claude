"""
Chart builders. Every function takes the filtered DataFrame and returns a
Plotly Figure, or None if there's nothing to plot (empty selection) so
app.py can show a consistent "no data" message instead of a blank chart.

Axes are never truncated to a non-zero baseline for bar/choropleth values,
per the no-misleading-axes requirement.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.constants import (
    CATEGORICAL_PALETTE,
    COLOR_FEMALE,
    COLOR_MALE,
    MONTH_ORDER,
    SEQUENTIAL_SCALE,
)


def monthly_trend(df: pd.DataFrame) -> go.Figure | None:
    """Total births by month, summed across current selection."""
    if df.empty:
        return None
    by_month = (
        df.groupby("month", observed=False)["births"].sum().reindex(MONTH_ORDER).reset_index()
    )
    fig = px.line(
        by_month, x="month", y="births", markers=True,
        title="Monthly Birth Trend",
        labels={"month": "Month", "births": "Total Births"},
        color_discrete_sequence=[CATEGORICAL_PALETTE[0]],
    )
    fig.update_traces(hovertemplate="%{x}: %{y:,} births<extra></extra>")
    fig.update_yaxes(rangemode="tozero", tickformat=",")
    return fig


def sex_comparison(df: pd.DataFrame) -> go.Figure | None:
    """Female vs. male births by month, grouped bars."""
    if df.empty:
        return None
    by_month_sex = (
        df.groupby(["month", "sex_of_infant"], observed=False)["births"]
        .sum()
        .reset_index()
    )
    fig = px.bar(
        by_month_sex, x="month", y="births", color="sex_of_infant",
        barmode="group",
        category_orders={"month": MONTH_ORDER},
        title="Female vs. Male Births by Month",
        labels={"month": "Month", "births": "Total Births", "sex_of_infant": "Sex"},
        color_discrete_map={"Female": COLOR_FEMALE, "Male": COLOR_MALE},
    )
    fig.update_traces(hovertemplate="%{x}, %{fullData.name}: %{y:,} births<extra></extra>")
    fig.update_yaxes(rangemode="tozero", tickformat=",")
    return fig


def state_ranking(df: pd.DataFrame, top_n: int | None = None) -> go.Figure | None:
    """Horizontal bar of total births by geography, descending."""
    if df.empty:
        return None
    by_state = df.groupby("state_of_residence")["births"].sum().sort_values(ascending=False)
    if top_n:
        by_state = by_state.head(top_n)
    fig = px.bar(
        by_state.sort_values().reset_index(),
        x="births", y="state_of_residence", orientation="h",
        title="Births by Geography" if not top_n else f"Top {top_n} Geographies by Births",
        labels={"births": "Total Births", "state_of_residence": "Geography"},
        color_discrete_sequence=[CATEGORICAL_PALETTE[0]],
    )
    fig.update_traces(hovertemplate="%{y}: %{x:,} births<extra></extra>")
    fig.update_xaxes(rangemode="tozero", tickformat=",")
    fig.update_layout(height=max(400, 18 * len(by_state)))
    return fig


def choropleth_map(df: pd.DataFrame) -> go.Figure | None:
    """US choropleth of total births by state."""
    if df.empty:
        return None
    by_state = df.groupby(["state_of_residence", "state_abbrev"])["births"].sum().reset_index()
    fig = px.choropleth(
        by_state, locations="state_abbrev", locationmode="USA-states",
        color="births", scope="usa", color_continuous_scale=SEQUENTIAL_SCALE,
        title="Total Births by State",
        hover_name="state_of_residence",
        labels={"births": "Total Births"},
    )
    fig.update_traces(hovertemplate="%{hovertext}: %{z:,} births<extra></extra>")
    return fig


def state_month_heatmap(df: pd.DataFrame) -> go.Figure | None:
    """State x month heatmap of total births."""
    if df.empty:
        return None
    pivot = (
        df.groupby(["state_of_residence", "month"], observed=False)["births"]
        .sum()
        .unstack("month")
        .reindex(columns=MONTH_ORDER)
    )
    # Order states by total descending so the heatmap reads top-to-bottom
    # from highest to lowest volume.
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]
    fig = px.imshow(
        pivot, aspect="auto", color_continuous_scale=SEQUENTIAL_SCALE,
        title="Births by State and Month",
        labels={"x": "Month", "y": "Geography", "color": "Births"},
    )
    fig.update_traces(hovertemplate="%{y}, %{x}: %{z:,} births<extra></extra>")
    fig.update_layout(height=max(500, 16 * len(pivot)))
    return fig


def top_bottom_comparison(df: pd.DataFrame, n: int = 5) -> go.Figure | None:
    """Side-by-side comparison of the top-N and bottom-N geographies."""
    if df.empty:
        return None
    by_state = df.groupby("state_of_residence")["births"].sum().sort_values(ascending=False)
    if len(by_state) < 2:
        return None
    n = min(n, len(by_state) // 2) or 1
    top = by_state.head(n).reset_index()
    top["group"] = f"Top {n}"
    bottom = by_state.tail(n).reset_index()
    bottom["group"] = f"Bottom {n}"
    combined = pd.concat([top, bottom]).sort_values("births")
    fig = px.bar(
        combined, x="births", y="state_of_residence", color="group", orientation="h",
        title=f"Top {n} vs. Bottom {n} Geographies",
        labels={"births": "Total Births", "state_of_residence": "Geography", "group": ""},
        color_discrete_map={f"Top {n}": CATEGORICAL_PALETTE[0], f"Bottom {n}": CATEGORICAL_PALETTE[1]},
    )
    fig.update_traces(hovertemplate="%{y}: %{x:,} births<extra></extra>")
    fig.update_xaxes(rangemode="tozero", tickformat=",")
    return fig
