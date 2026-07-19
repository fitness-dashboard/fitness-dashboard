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

# ==========================================================
# Seitenüberschrift
# ==========================================================

st.title("🧍 Body")

st.divider()

# ==========================================================
# Zeitraum auswählen
# ==========================================================

period = select_period()

dfBody = dfBody[
    (dfBody["Date"] >= period["start"]) &
    (dfBody["Date"] <= period["end"])
].copy()

st.divider()
# --------------------------------------------------
# Aktuelle Messung
# --------------------------------------------------

latest = (
    dfBody
    .dropna(subset=["Weight"])
    .iloc[-1]
)

# --------------------------------------------------
# Erste Messung im Zeitraum
# --------------------------------------------------

first = (
    dfBody
    .dropna(subset=["Weight"])
    .iloc[0]
)

# --------------------------------------------------
# Delta-Funktion
# --------------------------------------------------

def format_delta(start, end, unit):
    if pd.isna(start) or pd.isna(end):
        return "—"

    return f"{end - start:+.1f} {unit}"
# --------------------------------------------------
# Aktueller Status
# --------------------------------------------------

# --------------------------------------------------
# Aktuelle Messung
# --------------------------------------------------

st.subheader("Latest Measurement")

st.caption(
    latest["Date"].strftime("%d.%m.%Y")
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Weight",
        f'{latest["Weight"]:.1f} kg'
    )

    st.metric(
        "Muscle Mass",
        f'{latest["Muscle Mass 7 Days"]:.1f} kg'
    )

with col2:
    st.metric(
        "Body Fat",
        f'{latest["Body Fat % 7 Days"]:.1f} %'
    )

    st.metric(
        "BMI",
        f'{latest["BMI"]:.1f}'
    )

with col3:
    st.metric(
        "Fat Mass",
        f'{latest["Fat Mass 7 Days"]:.1f} kg'
    )

    st.metric(
        "Visceral Fat",
        f'{latest["Visceral Fat"]:.0f}'
    )

st.divider()

# --------------------------------------------------
# Period Summary
# --------------------------------------------------

st.subheader("Period Summary")

st.caption(
    f'{period["start"]:%d.%m.%Y} - {period["end"]:%d.%m.%Y}'
)

duration_days = (
    period["end"] - period["start"]
).days + 1

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Duration",
        f"{duration_days} days"
    )

    st.metric(
        "Δ Weight",
        format_delta(
            first["Weight"],
            latest["Weight"],
            "kg"
        )
    )
    st.metric(
        "Δ Body Fat",
        format_delta(
            first["Body Fat % 7 Days"],
            latest["Body Fat % 7 Days"],
            "%"
        )
    )



with col2:
    st.metric(
        "Δ Muscle Mass",
        format_delta(
            first["Muscle Mass 7 Days"],
            latest["Muscle Mass 7 Days"],
            "kg"
        )
    )
    st.metric(
        "Δ Fat Mass",
        format_delta(
            first["Fat Mass 7 Days"],
            latest["Fat Mass 7 Days"],
            "kg"
        )
    )



# ==========================================================
# Seite
# ==========================================================




st.dataframe(
    dfBody,
    use_container_width=True
)