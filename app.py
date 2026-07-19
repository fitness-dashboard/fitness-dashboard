import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Fitness Dashboard",
    page_icon="💪",
    layout="wide"
)

st.title("🏠 Dashboard")

#st.title("Fitness Dashboard")


from config import DAILY_FITNESS_DATA_CSV_FILE

dfGesamt = pd.read_csv(
    DAILY_FITNESS_DATA_CSV_FILE
)

dfGymRM = pd.read_csv(
    "gymrun_rm_data.csv"
)

dfGymRM["Date"] = pd.to_datetime(
    dfGymRM["Date"]
)


dfGesamt["Only Date"] = pd.to_datetime(
    dfGesamt["Only Date"]
)


# Zeitraum filtern
start_datum_chart = pd.Timestamp("2025-06-14")


dfChart = dfGesamt[
    dfGesamt["Only Date"] >= start_datum_chart
].copy()

#==================================================================================
# Erstes Diagramm
fig = px.line(
    dfChart,
    x="Only Date",
    y=[
        "Weight (kg)",
        "Weight (kg) 500kcal",
        "Weight (kg) 300kcal"
    ],
    title="Gewichtsentwicklung"
)


fig.for_each_trace(
    lambda trace: trace.update(
        name={
            "Weight (kg) 500kcal":
                "Weight (kg) 500kcal Defizit",

            "Weight (kg) 300kcal":
                "Weight (kg) 300kcal Defizit"
        }.get(trace.name, trace.name)
    )
)


# Y-Achse begrenzen
fig.update_yaxes(range=[70, 105])

# Achsen umbenennen bzw. ausblenden
fig.update_yaxes(
    title_text="kg"
)

fig.update_xaxes(
    title_text=""
)

# Für Handyansicht optimieren

fig.update_layout(
    height=350,

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.45,
        xanchor="center",
        x=0.5
    ),

    margin=dict(
        b=5
    )
)
# Diagramm 1 anzeigen
st.plotly_chart(fig, use_container_width=True)

#Neuen Zeitraum für Diagramm 2 festlegen, weil das Diagramm anders ist als die anderen

start_datum_chart2 = pd.Timestamp("2025-11-21")

dfChart2 = dfGesamt[
    dfGesamt["Only Date"] >= start_datum_chart2
].copy()


#==================================================================================
# Zweites Diagramm
fig2 = px.line(
    dfChart2,
    x="Only Date",
    y=[
        "Muscle Mass (kg) 7 Tage",
        "Körperfettanteil kg 7 Tage"
    ],
    title="Muskelmasse und Körperfettanteil"
)


# Y-Achse begrenzen
fig2.update_yaxes(range=[10, 75])

# Achsen umbenennen bzw. ausblenden
fig2.update_yaxes(
    title_text="Prozent"
)

fig2.update_xaxes(
    title_text=""
)


# Für Handyansicht optimieren

fig2.update_layout(
    height=350,

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.45,
        xanchor="center",
        x=0.5
    ),

    margin=dict(
        b=5
    )
)

# Diagramm 2 anzeigen
st.plotly_chart(fig2, use_container_width=True)

#==================================================================================
# Drittes Diagramm
fig3 = px.line(
    dfChart,
    x="Only Date",
    y=[
        "Body Fat (%) 7 Tage",
        "Fett % Soll"
    ],
    title="Körperfett % vs Ziel"
)


# Y-Achse begrenzen
fig3.update_yaxes(range=[10, 35])

# Achsen umbenennen bzw. ausblenden
fig3.update_yaxes(
    title_text="Prozent"
)

fig3.update_xaxes(
    title_text=""
)


# Für Handyansicht optimieren

fig3.update_layout(
    height=350,

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.45,
        xanchor="center",
        x=0.5
    ),

    margin=dict(
        b=5
    )
)

# Diagramm 3 anzeigen
st.plotly_chart(fig3, use_container_width=True)

#==================================================================================
# Viertes Diagramm
# Null-Werte durch NaN ersetzen
dfChart["BMR (kcal)"] = (
    dfChart["BMR (kcal)"]
    .replace(0, np.nan)
)

fig4 = px.line(
    dfChart,
    x="Only Date",
    y=[
        "BMR (kcal)",
        "Grundumsatz pro Tag errechnet 30 Tage",
        "Grundumsatz pro Tag errechnet 60 Tage",
        "Grundumsatz Mifflin-St.-Jeor mit Faktor 1,12"
    ],
    title="Grundumsätze"
)

# Graphen umbenennen
fig4.for_each_trace(
    lambda trace: trace.update(
        name={
            "BMR (kcal)": "BMR (kcal) Tanita",
            "Grundumsatz pro Tag errechnet 30 Tage": "Grundumsatz errechnet 30 Tage",
            "Grundumsatz pro Tag errechnet 60 Tage": "Grundumsatz errechnet 60 Tage",
            "Grundumsatz Mifflin-St.-Jeor mit Faktor 1,12":
                "Mifflin-St.-Jeor x 1,12"
        }.get(trace.name, trace.name)
    )
)


# Y-Achse begrenzen
fig4.update_yaxes(range=[1300, 2500])

# Achsen umbenennen bzw. ausblenden
fig4.update_yaxes(
    title_text="kcal"
)

fig4.update_xaxes(
    title_text=""
)


# Für Handyansicht optimieren

fig4.update_layout(
    height=350,

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.45,
        xanchor="center",
        x=0.5
    ),

    margin=dict(
        b=5
    )
)

# Diagramm anzeigen
st.plotly_chart(fig4, use_container_width=True)

#==================================================================================
# Diagramm 5 Muskelmasse Segmente
# ===============================

dfChart5 = dfChart.copy()

# 30-Tage-Durchschnitt berechnen
dfChart5["MM Right Arm 30 Tage"] = (
    dfChart5["Muscle mass - right arm"]
    .rolling(window=30, min_periods=1)
    .mean()
)

dfChart5["MM Left Arm 30 Tage"] = (
    dfChart5["Muscle mass - left arm"]
    .rolling(window=30, min_periods=1)
    .mean()
)

dfChart5["MM Right Leg 30 Tage"] = (
    dfChart5["Muscle mass - right leg"]
    .rolling(window=30, min_periods=1)
    .mean()
)

dfChart5["MM Left Leg 30 Tage"] = (
    dfChart5["Muscle mass - left leg"]
    .rolling(window=30, min_periods=1)
    .mean()
)

dfChart5["MM Trunk 30 Tage"] = (
    dfChart5["Muscle mass - trunk"]
    .rolling(window=30, min_periods=1)
    .mean()
)

fig5 = px.line(
    dfChart5,
    x="Only Date",
    y=[
        "MM Right Arm 30 Tage",
        "MM Left Arm 30 Tage",
        "MM Right Leg 30 Tage",
        "MM Left Leg 30 Tage",
        "MM Trunk 30 Tage"
    ],
    title="Muskelmasse nach Körpersegment"
)

# Legende schöner benennen
fig5.for_each_trace(
    lambda trace: trace.update(
        name={
            "MM Right Arm 30 Tage": "MM Rechter Arm",
            "MM Left Arm 30 Tage": "MM Linker Arm",
            "MM Right Leg 30 Tage": "MM Rechtes Bein",
            "MM Left Leg 30 Tage": "MM Linkes Bein",
            "MM Trunk 30 Tage": "MM Rumpf"
        }.get(trace.name, trace.name)
    )
)

# Achsen
fig5.update_yaxes(
    title_text="kg"
)

fig5.update_xaxes(
    title_text=""
)

# Für Handyansicht optimieren
fig5.update_layout(
    height=350,

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.45,
        xanchor="center",
        x=0.5
    ),

    margin=dict(
        b=5
    )
)

# Diagramm anzeigen
st.plotly_chart(
    fig5,
    use_container_width=True
)

#==================================================================================
# Diagramm 6 Muskelmasse Segmente
# ===============================

dfChart6 = dfChart.copy()

# 30-Tage-Durchschnitt berechnen
dfChart6["FM Right Arm 30 Tage"] = (
    dfChart6["Body fat (%) - right arm"]
    .rolling(window=30, min_periods=1)
    .mean()
)

dfChart6["FM Left Arm 30 Tage"] = (
    dfChart6["Body fat (%) - left arm"]
    .rolling(window=30, min_periods=1)
    .mean()
)

dfChart6["FM Right Leg 30 Tage"] = (
    dfChart6["Body fat (%) - right leg"]
    .rolling(window=30, min_periods=1)
    .mean()
)

dfChart6["FM Left Leg 30 Tage"] = (
    dfChart6["Body fat (%) - left leg"]
    .rolling(window=30, min_periods=1)
    .mean()
)

dfChart6["FM Trunk 30 Tage"] = (
    dfChart6["Body fat (%) - trunk"]
    .rolling(window=30, min_periods=1)
    .mean()
)

fig6 = px.line(
    dfChart6,
    x="Only Date",
    y=[
        "FM Right Arm 30 Tage",
        "FM Left Arm 30 Tage",
        "FM Right Leg 30 Tage",
        "FM Left Leg 30 Tage",
        "FM Trunk 30 Tage"
    ],
    title="Fettmasse nach Körpersegment"
)

# Legende schöner benennen
fig6.for_each_trace(
    lambda trace: trace.update(
        name={
            "FM Right Arm 30 Tage": "FM Rechter Arm",
            "FM Left Arm 30 Tage": "FM Linker Arm",
            "FM Right Leg 30 Tage": "FM Rechtes Bein",
            "FM Left Leg 30 Tage": "FM Linkes Bein",
            "FM Trunk 30 Tage": "FM Rumpf"
        }.get(trace.name, trace.name)
    )
)

# Achsen
fig6.update_yaxes(
    title_text="%"
)

fig6.update_xaxes(
    title_text=""
)

# Für Handyansicht optimieren
fig6.update_layout(
    height=350,

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.45,
        xanchor="center",
        x=0.5
    ),

    margin=dict(
        b=5
    )
)

# Diagramm anzeigen
st.plotly_chart(
    fig6,
    use_container_width=True
)
