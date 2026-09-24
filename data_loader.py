"""
Loading and validating the CDC provisional natality data.

All loading goes through `load_data`, which is cached with st.cache_data so
the CSV is parsed once per session instead of on every filter interaction.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from src.constants import MONTH_ORDER, REQUIRED_COLUMNS, VALID_SEXES, STATE_ABBREV

# Resolved relative to this file, not the working directory, so the app finds
# the CSV whether it's run locally (`streamlit run app.py` from anywhere) or
# deployed on Streamlit Community Cloud.
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Provisional_Natality_2025_CDC.csv"


class DataValidationError(Exception):
    """Raised when the source CSV fails a sanity check."""


def _validate(df: pd.DataFrame) -> None:
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise DataValidationError(f"Missing expected column(s): {missing_cols}")

    if df[REQUIRED_COLUMNS].isnull().any().any():
        raise DataValidationError("Found null values in one or more required columns.")

    if not (df["births"] >= 0).all():
        raise DataValidationError("Found negative birth counts.")

    bad_sex = set(df["sex_of_infant"].unique()) - VALID_SEXES
    if bad_sex:
        raise DataValidationError(f"Unexpected sex_of_infant value(s): {bad_sex}")

    unknown_states = set(df["state_of_residence"].unique()) - set(STATE_ABBREV.keys())
    if unknown_states:
        raise DataValidationError(
            f"State name(s) not found in abbreviation mapping: {unknown_states}"
        )

    months_present = set(df["month"].unique())
    if not months_present.issubset(set(MONTH_ORDER)):
        raise DataValidationError(f"Unrecognized month value(s): {months_present - set(MONTH_ORDER)}")


@st.cache_data
def load_data(path: str | Path = DATA_PATH) -> pd.DataFrame:
    """Load, validate, and lightly enrich the natality CSV.

    Returns a DataFrame with `month` as an ordered Categorical (Jan -> Dec)
    and a `state_abbrev` column added for map plotting.
    """
    df = pd.read_csv(path)
    _validate(df)

    df["month"] = pd.Categorical(df["month"], categories=MONTH_ORDER, ordered=True)
    df["state_abbrev"] = df["state_of_residence"].map(STATE_ABBREV)

    return df
