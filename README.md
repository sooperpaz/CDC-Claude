# CDC Provisional Natality Dashboard — 2025

A Streamlit dashboard for exploring 2025 U.S. provisional birth counts by
state, month, and infant sex. Built for undergraduate business analytics
students.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

Point the app at `app.py` as the main file. The data path in
`src/data_loader.py` is resolved relative to the repository root, so no
path changes are needed for deployment.

## Project structure

```
natality_dashboard/
├── app.py                # Entry point: layout + orchestration
├── data/                 # Source CSV
├── src/
│   ├── data_loader.py    # Cached loading + validation
│   ├── filters.py        # Sidebar filters
│   ├── kpis.py            # KPI calculations
│   ├── charts.py          # Plotly chart builders
│   └── constants.py       # Month order, state abbreviations, palette
├── .streamlit/config.toml # Theme
└── requirements.txt
```

## Data notes

Source: CDC National Center for Health Statistics, Provisional Natality
data, 2025. Figures are birth **counts**, not birth **rates**, and are
**provisional** — subject to revision as later data become available.
