import pandas as pd
import plotly.express as px
import streamlit as st

from config import (
    NUTRITION_CSV_FILE,
    NUTRITION_PHASE_SUMMARY_CSV_FILE,
)
import plotly.graph_objects as go

# ==========================================================
# Seite
# ==========================================================

st.title("🥗 Nutrition")

# ==========================================================
# Daten laden
# ==========================================================

dfSummary = pd.read_csv(
    NUTRITION_PHASE_SUMMARY_CSV_FILE
)

dfNutrition = pd.read_csv(
    NUTRITION_CSV_FILE
)

dfSummary["Start"] = pd.to_datetime(
    dfSummary["Start"]
)

dfSummary["End"] = pd.to_datetime(
    dfSummary["End"]
)

dfNutrition["Date"] = pd.to_datetime(
    dfNutrition["Date"]
)

# ==========================================================
# Ernährungsphase auswählen
# ==========================================================

phase = st.selectbox(
    "Nutrition Phase",
    dfSummary["Phase"]
)

summary = dfSummary[
    dfSummary["Phase"] == phase
].iloc[0]

# ==========================================================
# Nutrition Report
# ==========================================================

st.subheader("Nutrition Report")

col1, col2 = st.columns(2)

with col1:

    st.write(
        f"**Average Calories:** {summary['Average Calories']:.0f} kcal"
    )

    st.write(
        f"**Average Protein:** {summary['Average Protein']:.1f} g"
    )

    st.write(
        f"**Average Carbs:** {summary['Average Carbs']:.1f} g"
    )

with col2:

    st.write(
        f"**Average Fat:** {summary['Average Fat']:.1f} g"
    )

    st.write(
        f"**Days:** {int(summary['Days'])}"
    )

    st.write(
        f"**Period:** "
        f"{summary['Start'].strftime('%d.%m.%Y')} - "
        f"{summary['End'].strftime('%d.%m.%Y')}"
    )

# ==========================================================
# Nutrition Chart
# ==========================================================

st.subheader("Nutrition Chart")

METRICS = {
    "Calories (kcal)": "Calories",
    "Protein (g)": "Protein",
    "Carbs (g)": "Carbs",
    "Fat (g)": "Fat",
}

metric_label = st.selectbox(
    "Metric",
    list(METRICS.keys())
)

metric = METRICS[metric_label]

TARGET_COLUMNS = {
    "Calories": "Calories Target",
    "Protein": "Protein Target",
    "Carbs": "Carbs Target",
    "Fat": "Fat Target",
}

target_column = TARGET_COLUMNS[metric]

view = st.radio(
    "View",
    [
        "Current Phase",
        "All Phases",
    ],
    horizontal=True,
)

if view == "Current Phase":

    dfChart = dfNutrition[
        (dfNutrition["Date"] >= summary["Start"])
        &
        (dfNutrition["Date"] <= summary["End"])
        ].copy()

else:

    dfChart = dfNutrition.copy()

value_column = f"{metric} Actual"

show_target = st.checkbox(
    "Show Target",
    value=True,
)

fig = px.line(
    dfChart,
    x="Date",
    y=value_column,
    markers=True,
    title=f"{metric} Over Time",
)

if show_target:

    fig.add_trace(

        go.Scatter(

            x=dfChart["Date"],
            y=dfChart[target_column],

            mode="lines",

            name="Target",

            line=dict(
                dash="dash",
                width=2,
            ),
        )
    )

st.plotly_chart(
    fig,
    use_container_width=True,
)