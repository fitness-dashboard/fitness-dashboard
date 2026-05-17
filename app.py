import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


st.title("Fitness Dashboard")


dfGesamt = pd.read_csv(
    "fitness_dashboard_data.csv"
)


dfGesamt["Only Date"] = pd.to_datetime(
    dfGesamt["Only Date"]
)


# Zeitraum filtern
start_datum_chart = pd.Timestamp("2025-11-20")

dfChart = dfGesamt[
    dfGesamt["Only Date"] >= start_datum_chart
]


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
fig.update_yaxes(range=[70, 90])

# Für Handyansicht optimieren

fig.update_layout(
    height=350,

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.35,
        xanchor="center",
        x=0.5
    ),

    margin=dict(
        b=15
    )
)
# Diagramm 1 anzeigen
st.plotly_chart(fig, use_container_width=True)


# Zweites Diagramm
fig2 = px.line(
    dfChart,
    x="Only Date",
    y=[
        "Muscle Mass (kg) 7 Tage",
        "Körperfettanteil kg 7 Tage"
    ],
    title="Muskelmasse und Körperfettanteil"
)


# Y-Achse begrenzen
fig2.update_yaxes(range=[15, 65])


# Diagramm 2 anzeigen
st.plotly_chart(fig2, use_container_width=True)


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


# Diagramm 3 anzeigen
st.plotly_chart(fig3, use_container_width=True)

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
        "Grundumsatz pro Tag errechnet",
        "Grundumsatz Mifflin-St.-Jeor mit Faktor 1,12"
    ],
    title="Grundumsätze"
)

# Graphen umbenennen
fig4.for_each_trace(
    lambda trace: trace.update(
        name={
            "BMR (kcal)": "BMR (kcal) Tanita",
            "Grundumsatz pro Tag errechnet": "Grundumsatz errechnet",
            "Grundumsatz Mifflin-St.-Jeor mit Faktor 1,12":
                "Mifflin-St.-Jeor x 1,12"
        }.get(trace.name, trace.name)
    )
)


# Y-Achse begrenzen
fig4.update_yaxes(range=[1500, 3000])


# Diagramm anzeigen
st.plotly_chart(fig4, use_container_width=True)