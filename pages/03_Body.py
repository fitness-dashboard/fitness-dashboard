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
    .dropna(subset=["Weight 7 Days"])
    .iloc[-1]
)

# --------------------------------------------------
# Erste Messung im Zeitraum
# --------------------------------------------------

first = (
    dfBody
    .dropna(subset=["Weight 7 Days"])
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
    "All values shown are based on 7-day rolling averages where applicable."
)

st.caption(
    latest["Date"].strftime("%d.%m.%Y")
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Weight",
        f'{latest["Weight 7 Days"]:.1f} kg'
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
    latest["Date"] - pd.Timestamp(period["start"])
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
            first["Weight 7 Days"],
            latest["Weight 7 Days"],
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

st.divider()

# --------------------------------------------------
# Body Trend Chart
# --------------------------------------------------

#Chart Überschrift
st.subheader("Body Trend")

# Chart drop down Auswahl
chart_options = {
    "Weight": "Weight 7 Days",
    "Body Fat %": "Body Fat % 7 Days",
    "Fat Mass": "Fat Mass 7 Days",
    "Muscle Mass": "Muscle Mass 7 Days",
    "BMI": "BMI",
    "Visceral Fat": "Visceral Fat",
    "Body Water %": "Body Water %",
    "Bone Mass": "Bone Mass",
    "BMR": "BMR",
}

selected_chart = st.selectbox(
    "Chart",
    options=list(chart_options.keys()),
    index=0,
)

#Chat anzeigen
chart_column = chart_options[selected_chart]

fig = px.line(
    dfBody,
    x="Date",
    y=chart_column,
    markers=True,
    template="plotly_white",
)

fig.update_layout(
    height=450,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="",
    yaxis_title="",
    hovermode="x unified",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()

# --------------------------------------------------
# Segment Analysis - Muscle Mass
# --------------------------------------------------

st.subheader("Segment Analysis")

muscle_regions = [
    ("Right Arm", "Muscle Right Arm 7 Days"),
    ("Left Arm", "Muscle Left Arm 7 Days"),
    ("Trunk", "Muscle Trunk 7 Days"),
    ("Right Leg", "Muscle Right Leg 7 Days"),
    ("Left Leg", "Muscle Left Leg 7 Days"),
]

rows = []

for region, column in muscle_regions:

    rows.append({
        "Body Region": region,
        "Start": f"{first[column]:.2f} kg",
        "End": f"{latest[column]:.2f} kg",
        "Δ": f"{latest[column] - first[column]:+.2f} kg",
    })

dfMuscle = pd.DataFrame(rows)

st.markdown("#### Muscle Mass")

st.dataframe(
    dfMuscle,
    hide_index=True,
    use_container_width=True,
)

# --------------------------------------------------
# Segment Analysis - Body Fat
# --------------------------------------------------

fat_regions = [
    ("Right Arm", "Body Fat Right Arm 7 Days"),
    ("Left Arm", "Body Fat Left Arm 7 Days"),
    ("Trunk", "Body Fat Trunk 7 Days"),
    ("Right Leg", "Body Fat Right Leg 7 Days"),
    ("Left Leg", "Body Fat Left Leg 7 Days"),
]

rows = []

for region, column in fat_regions:
    rows.append({
        "Body Region": region,
        "Start": f"{first[column]:.1f} %",
        "End": f"{latest[column]:.1f} %",
        "Δ": f"{latest[column] - first[column]:+.1f} %",
    })

dfFat = pd.DataFrame(rows)

st.markdown("#### Body Fat")

st.dataframe(
    dfFat,
    hide_index=True,
    use_container_width=True,
)
