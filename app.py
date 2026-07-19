import plotly.express as px
import numpy as np
import streamlit as st
import pandas as pd

from config import (
    DAILY_FITNESS_DATA_CSV_FILE,
    BODY_CSV_FILE,
)

from filters import select_period

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

dfFitness["Only Date"] = pd.to_datetime(
    dfFitness["Only Date"]
)

dfBody["Date"] = pd.to_datetime(
    dfBody["Date"]
)

# ==========================================================
# Zeitraum auswählen
# ==========================================================

period = select_period()

dfFitness = dfFitness[
    (dfFitness["Only Date"] >= period["start"]) &
    (dfFitness["Only Date"] <= period["end"])
].copy()

dfBody = dfBody[
    (dfBody["Date"] >= period["start"]) &
    (dfBody["Date"] <= period["end"])
].copy()

st.divider()
