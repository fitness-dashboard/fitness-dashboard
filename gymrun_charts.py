import pandas as pd

from gymrun_helpers import (
    get_exercise_rm,
    get_exercise_volume
)
from gymrun_config import GYM_EXERCISES

def create_rm_chart_data(
    dfGymMaxRM,
    exercise_name
):

    dfChart = get_exercise_rm(
        dfGymMaxRM,
        exercise_name
    )

    dfChart = dfChart.rename(
        columns={
            exercise_name: "RM"
        }
    )

    config = GYM_EXERCISES[
        exercise_name
    ]

    return {
        "data": dfChart,
        "rm_min": config["rm_min"],
        "rm_max": config["rm_max"],
        "exercise_name": exercise_name
    }

def create_volume_chart_data(
    dfGymVolume,
    exercise_name
):

    dfChart = get_exercise_volume(
        dfGymVolume,
        exercise_name
    )

    dfChart = dfChart.rename(
        columns={
            exercise_name: "Volume"
        }
    )

    config = GYM_EXERCISES[
        exercise_name
    ]

    return {
        "data": dfChart,
        "vol_min": config["vol_min"],
        "vol_max": config["vol_max"],
        "exercise_name": exercise_name
    }

    return chart_info

def create_all_rm_chart_data(
    dfGymMaxRM
):

    all_charts = {}

    for exercise_name in GYM_EXERCISES:

        all_charts[exercise_name] = (
            create_rm_chart_data(
                dfGymMaxRM,
                exercise_name
            )
        )

    return all_charts

def create_all_volume_chart_data(
    dfGymVolume
):

    all_charts = {}

    for exercise_name in GYM_EXERCISES:

        all_charts[exercise_name] = (
            create_volume_chart_data(
                dfGymVolume,
                exercise_name
            )
        )

    return all_charts

def create_rm_excel_chart(
    workbook,
    dfGymMaxRM,
    exercise_name
):

    chart_info = create_rm_chart_data(
        dfGymMaxRM,
        exercise_name
    )

    dfChart = chart_info["data"]

    print(dfChart.head())

    print(dfChart.columns)

    # Blatt holen oder anlegen
    try:
        wsGymRun = workbook.sheets[
            "GymRun Data"
        ]
    except:
        wsGymRun = workbook.sheets.add(
            "GymRun Data"
        )

    try:
        wsGymRunCharts = workbook.sheets[
            "GymRun Charts"
        ]
    except:
        wsGymRunCharts = workbook.sheets.add(
            "GymRun Charts"
        )

    # Titel

    wsGymRun.range("A1").value = (
        exercise_name
    )

    wsGymRun.range("A1").font.bold = True
    wsGymRun.range("A1").font.size = 14

    # Daten

    wsGymRun.range("A3").value = dfChart

    #Hilfe
    print(dfChart.shape)

    last_row = len(dfChart) + 3

    # ===============================
    # Erstes GymRun Diagramm
    # ===============================

    chart = wsGymRunCharts.charts.add()

    chart.chart_type = "xy_scatter"

    # chart.set_source_data(
    #     wsGymRun.range(
    #         f"A3:B{last_row}"
    #     )
    # )

    chart.top = 50
    chart.left = 50

    chart.width = 800
    chart.height = 400

    excel_chart = chart.api[1]

    excel_chart.SeriesCollection().NewSeries()

    excel_chart.SeriesCollection(1).Values = (
        f"='GymRun Data'!$B$4:$B${last_row}"
    )

    excel_chart.SeriesCollection(1).XValues = (
        f"='GymRun Data'!$A$4:$A${last_row}"
    )

    excel_chart.SeriesCollection(1).Name = (
        exercise_name
    )

    # Titel

    excel_chart.HasTitle = True

    excel_chart.ChartTitle.Text = (
            exercise_name + " 1RM"
    )

    # X-Achse

    excel_chart.Axes(1).HasTitle = True
    excel_chart.Axes(1).AxisTitle.Text = (
        "Datum"
    )

    # Y-Achse

    excel_chart.Axes(2).HasTitle = True
    excel_chart.Axes(2).AxisTitle.Text = (
        "kg"
    )

    print(last_row)

    return chart_info