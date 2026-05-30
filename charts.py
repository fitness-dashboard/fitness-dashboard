import pandas as pd
import numpy as np

def erstelle_diagramme(workbook, dfGesamt):
    # ===============================
    # Neues Sheet für Diagramme
    # ===============================

    try:
        workbook.sheets["Diagramm"].delete()
    except:
        pass

    wsChart = workbook.sheets.add("Diagramm")

    # ==================================================
    # Nullwerte für Diagramme entfernen
    # Diagramm 1
    # ===================================================
    dfGesamt["Muscle Mass (kg) 7 Tage"] = (
        dfGesamt["Muscle Mass (kg) 7 Tage"]
        .replace(0, np.nan)
    )

    # Diagramm 2
    dfGesamt["Körperfettanteil kg 7 Tage"] = (
        dfGesamt["Körperfettanteil kg 7 Tage"]
        .replace(0, np.nan)
    )

    # Diagramm 3
    dfGesamt["Weight (kg)"] = (
        dfGesamt["Weight (kg)"]
        .replace(0, np.nan)
    )

    # Diagramm 4
    dfGesamt["BMR (kcal)"] = (
        dfGesamt["BMR (kcal)"]
        .replace(0, np.nan)
    )

    # ===============================
    # Daten für Diagramm 1 Muskel KG vs Fett KG schreiben
    # ===============================

    wsChart.range("A1").value = "Datum"
    wsChart.range("B1").value = "Muscle Mass (kg) 7 Tage"
    wsChart.range("C1").value = "Körperfettanteil kg 7 Tage"

    # Daten für Diagramme filtern da wir nur Eintraege nach dem 20.11.2025 haben wollen
    start_datum_chart = pd.Timestamp("2025-06-14")
    dfChart = dfGesamt[dfGesamt["Only Date"] >= start_datum_chart].copy()

    chart_data = pd.DataFrame({
        "Datum": dfChart["Only Date"],
        "Muscle Mass (kg) 7 Tage": dfChart["Muscle Mass (kg) 7 Tage"],
        "Körperfettanteil kg 7 Tage": dfChart["Körperfettanteil kg 7 Tage"]
    })

    wsChart.range("A2").options(index=False).value = chart_data

    # ===============================
    # Diagramm 1 Muskel KG vs Fett KG erstellen
    # ===============================

    chart = wsChart.charts.add()

    chart.chart_type = "line"

    chart.set_source_data(
        wsChart.range(
            f"A1:C{len(chart_data) + 1}"
        )
    )

    chart.top = 50
    chart.left = 50
    chart.width = 800
    chart.height = 400

    excel_chart = chart.api[1]

    excel_chart.HasTitle = True
    excel_chart.ChartTitle.Text = "Muskelmasse und Körperfettanteil"

    # X-Achse
    excel_chart.Axes(1).HasTitle = True
    excel_chart.Axes(1).AxisTitle.Text = "Datum"

    # Y-Achse
    excel_chart.Axes(2).HasTitle = True
    excel_chart.Axes(2).AxisTitle.Text = "kg"

    # ===============================
    # Daten für Diagramm 2 Soll Fett vs Ist Fett schreiben
    # ===============================

    wsChart.range("F1").value = "Datum"
    wsChart.range("G1").value = "Body Fat (%) 7 Tage"
    wsChart.range("H1").value = "Fett % Soll"

    # Daten für Diagramme filtern da wir nur Eintraege nach dem 20.11.2025 haben wollen
    start_datum_chart = pd.Timestamp("2025-06-14")
    dfChart = dfGesamt[dfGesamt["Only Date"] >= start_datum_chart].copy()

    chart_data2 = pd.DataFrame({
        "Datum": dfChart["Only Date"],
        "Body Fat (%) 7 Tage": dfChart["Body Fat (%) 7 Tage"],
        "Fett % Soll": dfChart["Fett % Soll"]
    })

    wsChart.range("F2").options(
        index=False,
        header=False
    ).value = chart_data2

    # ===============================
    # Diagramm 2 Soll Fett vs Ist Fett erstellen
    # ===============================

    chart2 = wsChart.charts.add()

    chart2.chart_type = "line"

    chart2.set_source_data(
        wsChart.range(
            f"F1:H{len(chart_data2) + 1}"
        )
    )

    # Position unter Diagramm 1
    chart2.top = 500
    chart2.left = 50

    chart2.width = 800
    chart2.height = 400

    # Excel COM Objekt
    excel_chart2 = chart2.api[1]

    # Titel
    excel_chart2.HasTitle = True
    excel_chart2.ChartTitle.Text = "Körperfett % vs Ziel"

    # X-Achse
    excel_chart2.Axes(1).HasTitle = True
    excel_chart2.Axes(1).AxisTitle.Text = "Datum"

    # Y-Achse
    excel_chart2.Axes(2).HasTitle = True
    excel_chart2.Axes(2).AxisTitle.Text = "%"

    # Legende unten
    excel_chart2.Legend.Position = -4107

    # ===============================
    # Daten für Diagramm 3 Gewicht vs 500kcal vs 300kcal schreiben
    # ===============================

    wsChart.range("K1").value = "Datum"
    wsChart.range("L1").value = "Weight (kg) 7 Tage"
    wsChart.range("M1").value = "Weight (kg) 500kcal"
    wsChart.range("N1").value = "Weight (kg) 300kcal"

    # Daten für Diagramme filtern da wir nur Eintraege nach dem 20.11.2025 haben wollen
    start_datum_chart = pd.Timestamp("2025-06-14")
    dfChart = dfGesamt[dfGesamt["Only Date"] >= start_datum_chart].copy()

    chart_data3 = pd.DataFrame({
        "Datum": dfChart["Only Date"],
        "Weight (kg)": dfChart["Weight (kg)"],
        "Weight (kg) 500kcal": dfChart["Weight (kg) 500kcal"],
        "Weight (kg) 300kcal": dfChart["Weight (kg) 300kcal"]
    })

    wsChart.range("K2").options(
        index=False,
        header=False
    ).value = chart_data3

    # ===============================
    # Diagramm 3 Gewicht vs 500kcal vs 300kcal
    # ===============================

    chart3 = wsChart.charts.add()

    chart3.chart_type = "line"

    chart3.set_source_data(
        wsChart.range(
            f"K1:N{len(chart_data3) + 1}"
        )
    )

    # Position unter Diagramm 2
    chart3.top = 950
    chart3.left = 50

    chart3.width = 800
    chart3.height = 400

    # Excel COM Objekt
    excel_chart3 = chart3.api[1]

    # Titel
    excel_chart3.HasTitle = True
    excel_chart3.ChartTitle.Text = "Gewicht vs Defizit kcal"

    # X-Achse
    excel_chart3.Axes(1).HasTitle = True
    excel_chart3.Axes(1).AxisTitle.Text = "Datum"

    # Y-Achse
    excel_chart3.Axes(2).HasTitle = True
    excel_chart3.Axes(2).AxisTitle.Text = "KG"

    # Legende unten
    excel_chart3.Legend.Position = -4107

    # ===============================
    # Daten für Diagramm 4 Grundumsätze schreiben
    # ===============================

    wsChart.range("Q1").value = "Datum"
    wsChart.range("R1").value = "BMR (kcal) Tanita"
    wsChart.range("S1").value = "Grundumsatz pro Tag errechnet"
    wsChart.range("T1").value = "Grundumsatz Mifflin-St.-Jeor mit Faktor 1,12"

    # Daten für Diagramme filtern da wir nur Eintraege nach dem 20.11.2025 haben wollen
    start_datum_chart = pd.Timestamp("2025-06-14")
    dfChart = dfGesamt[dfGesamt["Only Date"] >= start_datum_chart].copy()

    chart_data4 = pd.DataFrame({
        "Datum": dfChart["Only Date"],
        "BMR (kcal) Tanita": dfChart["BMR (kcal)"],
        "Grundumsatz pro Tag errechnet": dfChart["Grundumsatz pro Tag errechnet"],
        "Grundumsatz Mifflin-St.-Jeor mit Faktor 1,12": dfChart["Grundumsatz Mifflin-St.-Jeor mit Faktor 1,12"]
    })

    wsChart.range("Q2").options(
        index=False,
        header=False
    ).value = chart_data4

    # ===============================
    # Diagramm 4 Grundumsätze
    # ===============================

    chart4 = wsChart.charts.add()

    chart4.chart_type = "line"

    chart4.set_source_data(
        wsChart.range(
            f"Q1:T{len(chart_data4) + 1}"
        )
    )

    # Position unter Diagramm 2
    chart4.top = 1400
    chart4.left = 50

    chart4.width = 800
    chart4.height = 400

    # Excel COM Objekt
    excel_chart4 = chart4.api[1]

    # Titel
    excel_chart4.HasTitle = True
    excel_chart4.ChartTitle.Text = "Grundumsätze"

    # X-Achse
    excel_chart4.Axes(1).HasTitle = True
    excel_chart4.Axes(1).AxisTitle.Text = "Datum"

    # Y-Achse
    excel_chart4.Axes(2).HasTitle = True
    excel_chart4.Axes(2).AxisTitle.Text = "kcal"

    # Legende unten
    excel_chart4.Legend.Position = -4107
