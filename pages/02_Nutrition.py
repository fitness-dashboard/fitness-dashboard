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

dfChart["Average"] = (
    dfChart[value_column]
    .rolling(window=7, min_periods=1)
    .mean()
)

show_target = st.checkbox(
    "Show Target",
    value=True,
)

show_average = st.checkbox(
    "Show 7-Day Average",
    value=True,
)

fig = px.line(
    dfChart,
    x="Date",
    y=value_column,
    markers=True,
    title=None,
    labels={
        value_column: "Actual",
    },
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

if show_average:

    fig.add_trace(

        go.Scatter(

            x=dfChart["Date"],
            y=dfChart["Average"],

            mode="lines",

            name="Average",

            line=dict(
                width=3,
            ),
        )
    )

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================================
# Daily Nutrition
# ==========================================================

st.subheader("Daily Nutrition")

dfTable = (
    dfChart
    .sort_values(
        "Date",
        ascending=False,
    )
    .copy()
)

dfTable = dfTable[
    [
        "Date",
        "Calories Actual",
        "Protein Actual",
        "Carbs Actual",
        "Fat Actual",
    ]
]

dfTable = dfTable.rename(
    columns={
        "Calories Actual": "Calories (kcal)",
        "Protein Actual": "Protein (g)",
        "Carbs Actual": "Carbs (g)",
        "Fat Actual": "Fat (g)",
    }
)

dfTable["Date"] = (
    dfTable["Date"]
    .dt.strftime("%d.%m.%Y")
)

dfTable["Calories (kcal)"] = (
    dfTable["Calories (kcal)"]
    .round(0)
    .astype(int)
)

for col in [
    "Protein (g)",
    "Carbs (g)",
    "Fat (g)",
]:
    dfTable[col] = dfTable[col].round(0)

st.dataframe(
    dfTable,
    use_container_width=True,
    hide_index=True,
)