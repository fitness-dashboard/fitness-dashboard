import pandas as pd
import streamlit as st

from config import (
    NUTRITION_PHASE_SUMMARY_CSV_FILE
)

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

dfSummary["Start"] = pd.to_datetime(
    dfSummary["Start"]
)

dfSummary["End"] = pd.to_datetime(
    dfSummary["End"]
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