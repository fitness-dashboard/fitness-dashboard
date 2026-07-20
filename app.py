import plotly.express as px
import numpy as np
import streamlit as st
import pandas as pd

from config import (
    DAILY_FITNESS_DATA_CSV_FILE,
    BODY_CSV_FILE,
    TRAINING_DATA_CSV_FILE,
)

from filters import select_period
from dashboard import build_dashboard_dataframe

st.set_page_config(
    page_title="Fitness Dashboard",
    page_icon="💪",
    layout="wide"
)

st.title("🏠 Fitness Dashboard")

st.divider()


# ==========================================================
# Daten laden
# ==========================================================

dfFitness = pd.read_csv(
    DAILY_FITNESS_DATA_CSV_FILE
)

dfBody = pd.read_csv(
    BODY_CSV_FILE
)

dfTraining = pd.read_csv(
    TRAINING_DATA_CSV_FILE
)

dfFitness["Only Date"] = pd.to_datetime(
    dfFitness["Only Date"]
)

dfBody["Date"] = pd.to_datetime(
    dfBody["Date"]
)

dfTraining["Date"] = pd.to_datetime(
    dfTraining["Date"]
)

dfDashboard = build_dashboard_dataframe(
    dfFitness,
    dfBody,
    dfTraining,
)

# ==========================================================
# Zeitraum auswählen
# ==========================================================

period = select_period()

dfDashboard = dfDashboard[
    (dfDashboard["Start"] >= period["start"])
    &
    (dfDashboard["End"] <= period["end"])
].copy()

st.divider()

# ==========================================================
# Weekly Dashboard
# ==========================================================

st.subheader("Weekly Dashboard")

st.dataframe(
    dfDashboard[
        [
            "Week",
            "Period",
            "Calories",
            "Protein",
            "Fat",
            "Carbs",
            "Nutrition Days",
            "Weight",
            "Δ Weight",
            "Body Fat",
            "Δ Body Fat",
            "Muscle",
            "Δ Muscle",
            "Weight Days",
            "Workout Days",
            "PRs",
            "Training Minutes",
            "Training Calories",
        ]
    ],
    hide_index=True,
    use_container_width=True,
    column_config={
        "Calories": st.column_config.NumberColumn(
            "Calories",
            format="%.0f kcal",
        ),
        "Protein": st.column_config.NumberColumn(
            "Protein",
            format="%.0f g",
        ),
        "Fat": st.column_config.NumberColumn(
            "Fat",
            format="%.0f g",
        ),
        "Carbs": st.column_config.NumberColumn(
            "Carbs",
            format="%.0f g",
        ),
        "Weight": st.column_config.NumberColumn(
            "Weight",
            format="%.2f kg",
        ),
        "Δ Weight": st.column_config.NumberColumn(
            "Δ Weight",
            format="%+.2f kg",
        ),
        "Body Fat": st.column_config.NumberColumn(
            "Body Fat",
            format="%.1f %%",   # Doppeltes % ist korrekt
        ),
        "Δ Body Fat": st.column_config.NumberColumn(
            "Δ Body Fat",
            format="%+.1f %%",
        ),
        "Muscle": st.column_config.NumberColumn(
            "Muscle",
            format="%.2f kg",
        ),
        "Δ Muscle": st.column_config.NumberColumn(
            "Δ Muscle",
            format="%+.2f kg",
        ),
        "PRs": st.column_config.NumberColumn(
            "PRs",
            format="%d",
        ),
        "Training Minutes": st.column_config.NumberColumn(
            "Minutes",
            format="%d min",
        ),
        "Training Calories": st.column_config.NumberColumn(
            "Training kcal",
            format="%d kcal",
        ),
    },
)
