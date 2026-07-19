import streamlit as st
import pandas as pd
import plotly.express as px

from config import BODY_CSV_FILE
from filters import select_period


# ==========================================================
# Daten laden
# ==========================================================

dfBody = pd.read_csv(
    BODY_CSV_FILE
)

dfBody["Date"] = pd.to_datetime(
    dfBody["Date"]
)

#Hilfe
print("Hilfe Kai 1")
st.write(f"Anzahl Zeilen nach Filter: {len(dfBody)}")

st.dataframe(
    dfBody.head(),
    use_container_width=True
)
#Ende Hilfe


# ==========================================================
# Seitenüberschrift
# ==========================================================

st.title("🧍 Body")

st.divider()

# ==========================================================
# Zeitraum auswählen
# ==========================================================

dfBody = select_period(
    dfBody,
    date_column="Date"
)


# ==========================================================
# Seite
# ==========================================================


st.dataframe(
    dfBody,
    use_container_width=True
)