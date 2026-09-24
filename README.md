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
├── app.py                      # Entry point: page config, layout, tab orchestration
├── data/
│   └── Provisional_Natality_2025_CDC.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # load_data(), validation, state→abbrev mapping
│   ├── filters.py               # sidebar filter widgets, filter-application logic
│   ├── kpis.py                  # KPI computation functions
│   ├── charts.py                # all Plotly figure builders
│   └── constants.py             # STATE_ABBREV dict, MONTH_ORDER list, color palette
├── .streamlit/
│   └── config.toml              # theme (accessible palette)
├── requirements.txt
└── README.md
```

## Data notes

Source: CDC National Center for Health Statistics, Provisional Natality
data, 2025. Figures are birth **counts**, not birth **rates**, and are
**provisional** — subject to revision as later data become available.
