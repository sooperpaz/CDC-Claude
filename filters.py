"""
Sidebar filters: state/geography, month, and infant sex.

Widget state lives in st.session_state under fixed keys so the "Select All"
and "Reset Filters" buttons can programmatically overwrite selections via
on_click callbacks (Streamlit requires this to happen before the widget
is instantiated on the next run, hence the callback pattern rather than
just reassigning after the fact).
"""

import pandas as pd
import streamlit as st

from src.constants import MONTH_ORDER

STATE_KEY = "filter_states"
MONTH_KEY = "filter_months"
SEX_KEY = "filter_sex"

SEX_OPTIONS = ["Female", "Male"]


def _init_defaults(all_states: list[str]) -> None:
    st.session_state.setdefault(STATE_KEY, all_states)
    st.session_state.setdefault(MONTH_KEY, MONTH_ORDER.copy())
    st.session_state.setdefault(SEX_KEY, SEX_OPTIONS.copy())


def _select_all(all_states: list[str]) -> None:
    st.session_state[STATE_KEY] = all_states
    st.session_state[MONTH_KEY] = MONTH_ORDER.copy()
    st.session_state[SEX_KEY] = SEX_OPTIONS.copy()


def _reset(all_states: list[str]) -> None:
    # Reset currently means "back to everything selected," matching the
    # dashboard's default (unfiltered) view.
    _select_all(all_states)


def render_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar widgets and return the filtered DataFrame."""
    all_states = sorted(df["state_of_residence"].unique())
    _init_defaults(all_states)

    st.sidebar.header("Filters")

    col_a, col_b = st.sidebar.columns(2)
    col_a.button("Select All", on_click=_select_all, args=(all_states,), use_container_width=True)
    col_b.button("Reset Filters", on_click=_reset, args=(all_states,), use_container_width=True)

    st.sidebar.multiselect("State / geography", options=all_states, key=STATE_KEY)
    st.sidebar.multiselect("Month", options=MONTH_ORDER, key=MONTH_KEY)
    st.sidebar.multiselect("Infant sex", options=SEX_OPTIONS, key=SEX_KEY)

    selected_states = st.session_state[STATE_KEY]
    selected_months = st.session_state[MONTH_KEY]
    selected_sexes = st.session_state[SEX_KEY]

    st.sidebar.markdown("---")
    st.sidebar.caption(
        f"**Active filters:** {len(selected_states)} of {len(all_states)} geographies · "
        f"{len(selected_months)} of 12 months · "
        f"sex: {', '.join(selected_sexes) if selected_sexes else 'none selected'}"
    )

    filtered = df[
        df["state_of_residence"].isin(selected_states)
        & df["month"].isin(selected_months)
        & df["sex_of_infant"].isin(selected_sexes)
    ]
    return filtered
