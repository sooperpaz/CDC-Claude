"""
CDC Provisional Natality 2025 Dashboard.

Entry point: this file is kept intentionally thin. It handles page config,
layout, and wires together the functions in src/ — data loading and
filtering, KPI math, and chart building all live in their own modules.
"""

import streamlit as st

from src.charts import (
    choropleth_map,
    monthly_trend,
    sex_comparison,
    state_month_heatmap,
    state_ranking,
    top_bottom_comparison,
)
from src.data_loader import DataValidationError, load_data
from src.filters import render_filters
from src.kpis import avg_births_per_month, geography_count, top_geography, top_month, total_births

st.set_page_config(
    page_title="CDC Provisional Natality Dashboard 2025",
    page_icon="👶",
    layout="wide",
)


def render_header() -> None:
    st.title("CDC Provisional Natality Dashboard — 2025")
    st.markdown(
        "Explore 2025 U.S. birth counts by state, month, and infant sex using "
        "provisional CDC data. Use the sidebar filters to narrow the selection."
    )
    st.warning(
        "**Provisional data:** These 2025 figures are preliminary and subject to "
        "revision as more complete records become available.",
        icon="⚠️",
    )
    st.info(
        "**Counts, not rates:** All figures shown are raw birth *counts*, not "
        "birth *rates*. They are not adjusted for population size, so larger "
        "states will naturally show higher counts.",
        icon="ℹ️",
    )
    st.caption("Source: CDC National Center for Health Statistics, Provisional Natality data, 2025.")


def render_kpis(df) -> None:
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Births", f"{total_births(df):,}")
    col2.metric("Geographies Selected", f"{geography_count(df):,}")
    col3.metric("Avg. Births / Month", f"{avg_births_per_month(df):,.0f}")

    top_geo = top_geography(df)
    col4.metric(
        "Top Geography",
        top_geo[0] if top_geo else "—",
        f"{top_geo[1]:,} births" if top_geo else None,
    )

    top_mo = top_month(df)
    col5.metric(
        "Top Month",
        top_mo[0] if top_mo else "—",
        f"{top_mo[1]:,} births" if top_mo else None,
    )


def _show_or_empty_message(fig) -> None:
    if fig is None:
        st.info("No data for the current filter selection. Try adjusting the filters in the sidebar.")
    else:
        st.plotly_chart(fig, use_container_width=True)


def render_overview_tab(df) -> None:
    _show_or_empty_message(monthly_trend(df))
    _show_or_empty_message(sex_comparison(df))


def render_geographic_tab(df) -> None:
    _show_or_empty_message(choropleth_map(df))
    _show_or_empty_message(state_ranking(df))


def render_monthly_sex_tab(df) -> None:
    _show_or_empty_message(state_month_heatmap(df))
    _show_or_empty_message(top_bottom_comparison(df))


def render_data_tab(df) -> None:
    st.subheader("Filtered Data")
    search = st.text_input("Search (matches any column)", "")
    display_df = df.drop(columns=["state_abbrev"])
    if search:
        mask = display_df.apply(
            lambda col: col.astype(str).str.contains(search, case=False, na=False)
        ).any(axis=1)
        display_df = display_df[mask]

    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.caption(f"{len(display_df):,} rows shown.")

    st.download_button(
        "Download filtered data as CSV",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_natality_data.csv",
        mime="text/csv",
    )


def render_about_tab() -> None:
    st.subheader("About the Data")
    st.markdown(
        """
- **Source:** CDC National Center for Health Statistics (NCHS), Provisional Natality data for 2025.
- **Provisional status:** These figures are preliminary. Provisional data are released ahead of
  final data to give a timely picture, but counts can change — sometimes materially for the most
  recent months — once late-reported and corrected birth certificates are incorporated.
- **Counts vs. rates:** This dashboard shows birth *counts* (raw numbers of births), not birth
  *rates* (births relative to population). A state with a high count may still have a low rate if
  its population is large; comparing counts across states of very different sizes should be done
  with that in mind.
- **Geography:** "State" here means state (or D.C.) of maternal residence, not the state where the
  birth occurred.
- **Granularity:** Data are reported by state, month, and infant sex for 2025.
        """
    )


def main() -> None:
    try:
        df = load_data()
    except DataValidationError as e:
        st.error(f"Data failed validation and could not be loaded: {e}")
        st.stop()

    render_header()
    filtered_df = render_filters(df)

    st.markdown("---")
    render_kpis(filtered_df)
    st.markdown("---")

    tab_overview, tab_geo, tab_monthly_sex, tab_data, tab_about = st.tabs(
        ["Overview", "Geographic Analysis", "Monthly and Sex Analysis", "Data Table and Download", "About the Data"]
    )
    with tab_overview:
        render_overview_tab(filtered_df)
    with tab_geo:
        render_geographic_tab(filtered_df)
    with tab_monthly_sex:
        render_monthly_sex_tab(filtered_df)
    with tab_data:
        render_data_tab(filtered_df)
    with tab_about:
        render_about_tab()


if __name__ == "__main__":
    main()
