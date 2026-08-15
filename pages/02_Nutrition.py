import pandas as pd
import plotly.express as px
import streamlit as st

from config import (
    DAILY_FITNESS_DATA_CSV_FILE,
    NUTRITION_CSV_FILE,
    NUTRITION_PHASE_SUMMARY_CSV_FILE,
    NUTRITION_PHASES,
)
import plotly.graph_objects as go

from filters import select_period

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

dfFitness = pd.read_csv(
    DAILY_FITNESS_DATA_CSV_FILE
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

dfFitness["Only Date"] = pd.to_datetime(
    dfFitness["Only Date"]
)

# ==========================================================
# Sportbereinigte Kalorien
# ==========================================================

training_calories_by_date = (
    dfFitness
    .groupby("Only Date")["Kalorien aus Training"]
    .sum(min_count=1)
)

dfNutrition["Training Calories"] = (
    dfNutrition["Date"]
    .map(training_calories_by_date)
    .fillna(0)
)

dfNutrition["Net Calories"] = (
    dfNutrition["Calories Actual"]
    - dfNutrition["Training Calories"]
)

dfNutrition["Net Calories Target"] = pd.Series(
    pd.NA,
    index=dfNutrition.index,
    dtype="Float64"
)

for nutrition_phase in NUTRITION_PHASES:

    phase_mask = (
        (dfNutrition["Date"] >= pd.Timestamp(nutrition_phase["start"]))
        &
        (dfNutrition["Date"] <= pd.Timestamp(nutrition_phase["end"]))
    )

    dfNutrition.loc[
        phase_mask,
        "Net Calories Target"
    ] = nutrition_phase["calories"]

dfNutrition["Net Calories %"] = (
    dfNutrition["Net Calories"]
    / dfNutrition["Net Calories Target"]
    * 100
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

# ==========================================================
# Zeitraum filtern
# ==========================================================

if period["type"] == "Nutrition Phase":

    summary = dfSummary[
        dfSummary["Phase"] == period["name"]
    ].iloc[0]

else:

    matching_phases = dfSummary[
        (dfSummary["Start"] <= period["end"])
        &
        (dfSummary["End"] >= period["start"])
    ]

    summary = {
        "Phase": period["name"],
        "Average Calories": matching_phases["Average Calories"].mean(),
        "Average Protein": matching_phases["Average Protein"].mean(),
        "Average Carbs": matching_phases["Average Carbs"].mean(),
        "Average Fat": matching_phases["Average Fat"].mean(),
        "Days": (period["end"] - period["start"]).days + 1,
        "Start": period["start"],
        "End": period["end"],
    }

summary["Average Net Calories"] = (
    dfNutritionPeriod["Net Calories"].mean()
)

summary["Net Calories Target"] = (
    dfNutritionPeriod["Net Calories %"].mean()
)

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
        f"**Average Net Calories:** "
        f"{summary['Average Net Calories']:.0f} kcal"
    )

    st.write(
        f"**Average Protein:** {summary['Average Protein']:.1f} g"
    )

    st.write(
        f"**Average Carbs:** {summary['Average Carbs']:.1f} g"
    )

with col2:

    st.write(
        f"**Net Calories Target:** "
        f"{summary['Net Calories Target']:.1f} %"
    )

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
    "Net Calories (kcal)": "Net Calories",
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
    "Net Calories": "Net Calories Target",
}

target_column = TARGET_COLUMNS[metric]

view = st.radio(
    "View",
    [
        "Selected Period",
        "All Time",
    ],
    horizontal=True,
)

if view == "Selected Period":

    dfChart = dfNutrition[
        (dfNutrition["Date"] >= period["start"])
        &
        (dfNutrition["Date"] <= period["end"])
    ].copy()

else:

    dfChart = dfNutrition.copy()

if metric == "Net Calories":
    value_column = "Net Calories"
else:
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
        "Calories %",

        "Training Calories",
        "Net Calories",
        "Net Calories %",

        "Protein Actual",
        "Protein %",

        "Carbs Actual",
        "Carbs %",

        "Fat Actual",
        "Fat %",
    ]
]

dfTable = dfTable.rename(
    columns={
        "Calories Actual": "Calories",
        "Calories %": "Cal %",

        "Training Calories": "Sport Calories",
        "Net Calories %": "Net Cal %",

        "Protein Actual": "Protein",
        "Protein %": "Prot %",

        "Carbs Actual": "Carbs",
        "Carbs %": "Carb %",

        "Fat Actual": "Fat",
        "Fat %": "Fat %",
    }
)

dfTable["Date"] = (
    dfTable["Date"]
    .dt.strftime("%d.%m.%Y")
)

# =====================================
# Zahlen formatieren
# =====================================

numeric_columns = [
    "Calories",
    "Sport Calories",
    "Net Calories",
    "Protein",
    "Carbs",
    "Fat",
    "Cal %",
    "Net Cal %",
    "Prot %",
    "Carb %",
    "Fat %",
]

for col in numeric_columns:

    dfTable[col] = (
        dfTable[col]
        .round(0)
        .astype("Int64")
    )

def highlight_percent(val):

    if val < 80:
        color = "#f8d7da"      # hellrot

    elif val < 90:
        color = "#fff3cd"      # hellgelb

    elif val <= 110:
        color = "#d4edda"      # hellgrün

    elif val <= 120:
        color = "#fff3cd"      # hellgelb

    else:
        color = "#f8d7da"      # hellrot

    return f"background-color: {color}"


percent_columns = [
    "Cal %",
    "Net Cal %",
    "Prot %",
    "Carb %",
    "Fat %",
]

styler = (
    dfTable.style
    .map(
        highlight_percent,
        subset=percent_columns,
    )
)

st.dataframe(
    styler,
    use_container_width=True,
    hide_index=True,
)
