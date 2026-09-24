"""
Static reference data used across the dashboard.

Keeping these in one module means the month ordering, the state/abbreviation
mapping, and the color palette are each defined exactly once and imported
everywhere they're needed (data loading, filters, charts).
"""

# Chronological month order. Used to build a pandas Categorical dtype so
# charts and tables sort Jan -> Dec instead of alphabetically.
MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

# State (and DC) name -> USPS abbreviation. Hardcoded rather than looked up
# from a third-party package so the choropleth's `locations` field never
# depends on an external mapping matching the CDC's exact naming.
STATE_ABBREV = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT",
    "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL",
    "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
    "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY",
    "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
}

# Colorblind-safe categorical palette (Okabe-Ito), reused across every chart
# so Female/Male and other categorical encodings stay consistent dashboard-wide.
COLOR_FEMALE = "#E69F00"   # orange
COLOR_MALE = "#0072B2"     # blue
CATEGORICAL_PALETTE = [
    "#0072B2", "#E69F00", "#009E73", "#CC79A7",
    "#56B4E9", "#D55E00", "#F0E442", "#000000",
]
# Sequential palette for the choropleth and heatmap (perceptually uniform,
# colorblind-safe).
SEQUENTIAL_SCALE = "Viridis"

REQUIRED_COLUMNS = [
    "state_of_residence", "month", "month_code", "year_code",
    "sex_of_infant", "births",
]
VALID_SEXES = {"Female", "Male"}
