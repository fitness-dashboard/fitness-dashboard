import plotly.express as px
import numpy as np
import streamlit as st
import pandas as pd

from config import (
    DAILY_FITNESS_DATA_CSV_FILE,
    NUTRITION_CSV_FILE,
    BODY_CSV_FILE,
    GYMRUN_RM_CSV_FILE,
    TRAINING_DATA_CSV_FILE,
)

from filters import select_period
from dashboard import (
    build_dashboard_dataframe,
    get_dashboard_summary
)


def format_value(value, unit, decimals=1):

    if pd.isna(value):

        return "—"

    return f"{value:.{decimals}f} {unit}"


def format_delta(value, unit, decimals=1):

    if pd.isna(value):

        return None

    return f"{value:+.{decimals}f} {unit}"

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

dfNutrition = pd.read_csv(
    NUTRITION_CSV_FILE
)

dfBody = pd.read_csv(
    BODY_CSV_FILE
)

dfTraining = pd.read_csv(
    TRAINING_DATA_CSV_FILE
)

dfGymRM = pd.read_csv(
    GYMRUN_RM_CSV_FILE
)

dfFitness["Only Date"] = pd.to_datetime(
    dfFitness["Only Date"]
)

dfNutrition["Date"] = pd.to_datetime(
    dfNutrition["Date"]
)

dfBody["Date"] = pd.to_datetime(
    dfBody["Date"]
)

dfTraining["Date"] = pd.to_datetime(
    dfTraining["Date"]
)

dfGymRM["Date"] = pd.to_datetime(
    dfGymRM["Date"]
)

# ==========================================================
# Zeitraum auswählen
# ==========================================================

period = select_period()

dfNutritionPeriod = dfNutrition[
    (dfNutrition["Date"] >= period["start"])
    &
    (dfNutrition["Date"] <= period["end"])
].copy()

dfDashboard = build_dashboard_dataframe(
    dfFitness,
    dfBody,
    dfTraining,
    dfGymRM,
    period,
)

dfDashboard = dfDashboard[
    (dfDashboard["Start"] >= period["start"])
    &
    (dfDashboard["End"] <= period["end"])
].copy()

st.divider()

# ==========================================================
# Period Summary
# ==========================================================

summary = get_dashboard_summary(
    dfFitness,
    dfBody,
    dfGymRM,
    period
)

st.subheader("Period Summary")

st.caption(
    f'{period["start"]:%d.%m.%Y} - '
    f'{period["end"]:%d.%m.%Y}'
)

st.markdown("#### Nutrition")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Ø Calories",
        format_value(
            summary["Calories"],
            "kcal",
            decimals=0
        )
    )

with col2:

    st.metric(
        "Ø Protein",
        format_value(
            summary["Protein"],
            "g",
            decimals=0
        )
    )

with col3:

    st.metric(
        "Ø Carbs",
        format_value(
            summary["Carbs"],
            "g",
            decimals=0
        )
    )

with col4:

    st.metric(
        "Ø Fat",
        format_value(
            summary["Fat"],
            "g",
            decimals=0
        )
    )

st.markdown("##### Nutrition Target Achievement")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Ø Calories Target",
        format_value(
            dfNutritionPeriod["Calories %"].mean(),
            "%"
        )
    )

with col2:

    st.metric(
        "Ø Protein Target",
        format_value(
            dfNutritionPeriod["Protein %"].mean(),
            "%"
        )
    )

with col3:

    st.metric(
        "Ø Carbs Target",
        format_value(
            dfNutritionPeriod["Carbs %"].mean(),
            "%"
        )
    )

with col4:

    st.metric(
        "Ø Fat Target",
        format_value(
            dfNutritionPeriod["Fat %"].mean(),
            "%"
        )
    )

st.markdown("#### Body Development")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Weight",
        format_value(
            summary["Weight"],
            "kg"
        ),
        delta=format_delta(
            summary["Weight Change"],
            "kg"
        ),
        delta_color="normal"
    )

with col2:

    st.metric(
        "Fat Mass",
        format_value(
            summary["Fat Mass"],
            "kg"
        ),
        delta=format_delta(
            summary["Fat Mass Change"],
            "kg"
        ),
        delta_color="normal"
    )

with col3:

    st.metric(
        "Muscle Mass",
        format_value(
            summary["Muscle Mass"],
            "kg"
        ),
        delta=format_delta(
            summary["Muscle Mass Change"],
            "kg"
        ),
        delta_color="normal"
    )

with col4:

    st.metric(
        "Body Fat",
        format_value(
            summary["Body Fat"],
            "%"
        ),
        delta=format_delta(
            summary["Body Fat Change"],
            "%"
        ),
        delta_color="normal"
    )

st.markdown("#### Training Progress")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Exercises Improved",
        summary["Exercises Improved"]
    )

with col2:

    st.metric(
        "Average Δ RM",
        format_value(
            summary["Average Δ RM"],
            "kg"
        )
    )

with col3:

    st.metric(
        "All time PRs",
        summary["All time PRs"]
    )

with col4:

    st.metric(
        "Training Days",
        summary["Training Days"]
    )

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
            "All time PRs",
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
        "All time PRs": st.column_config.NumberColumn(
            "All time PRs",
            format="%d",
        ),
    },
)
