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

#Hilfe
    print(chart_info.keys())

    rm_min = chart_info["rm_min"]
    rm_max = chart_info["rm_max"]

#Hilfe
    print(rm_min)
    print(rm_max)


    dfChart = chart_info["data"]



    # Blatt holen oder anlegen
    try:
        wsGymRun = workbook.sheets[
            "GymRun Data"
        ]
    except:
        wsGymRun = workbook.sheets.add(
            "GymRun Data"
        )

    wsGymRun.clear()

    try:
        wsGymRunCharts = workbook.sheets[
            "GymRun Charts"
        ]
    except:
        wsGymRunCharts = workbook.sheets.add(
            "GymRun Charts"
        )

    # Vorhandene Diagramme löschen

    for chart in wsGymRunCharts.charts:
        chart.delete()

    # Titel

    wsGymRun.range("A1").value = (
        exercise_name
    )

    wsGymRun.range("A1").font.bold = True
    wsGymRun.range("A1").font.size = 14

    # Daten

    wsGymRun.range("B3").options(
        index=False
    ).value = dfChart



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
        f"='GymRun Data'!$C$4:$C${last_row}"
    )

    excel_chart.SeriesCollection(1).XValues = (
        f"='GymRun Data'!$B$4:$B${last_row}"
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
    excel_chart.Axes(2).MinimumScale = rm_min
    excel_chart.Axes(2).MaximumScale = rm_max
    # rm_min = chart_info["rm_min"]
    # rm_max = chart_info["rm_max"]

    return chart_info

def create_volume_excel_chart(
    workbook,
    dfGymVolume,
    exercise_name
):
    volume_info = create_volume_chart_data(
        dfGymVolume,
        exercise_name
    )

    dfChart = volume_info["data"]

    dfChart = volume_info["data"]
    print(dfChart.shape)

    # Blatt holen oder anlegen

    try:
        wsGymRunVolume = workbook.sheets[
            "GymRun Volume Data"
        ]
    except:
        wsGymRunVolume = workbook.sheets.add(
            "GymRun Volume Data"
        )

    wsGymRunVolume.clear()

    wsGymRunVolume.range("A1").value = exercise_name

    wsGymRunVolume.range("B3").options(
        index=False
    ).value = dfChart

    last_row = len(dfChart) + 3

    # ===============================
    # Volumen Diagramm
    # ===============================

    try:
        wsGymRunCharts = workbook.sheets[
            "GymRun Charts"
        ]
    except:
        wsGymRunCharts = workbook.sheets.add(
            "GymRun Charts"
        )

    chart = wsGymRunCharts.charts.add()

    chart.chart_type = "xy_scatter_lines"

    chart.top = 50
    chart.left = 900

    chart.width = 800
    chart.height = 400

    excel_chart = chart.api[1]

    excel_chart.SeriesCollection().NewSeries()

    excel_chart.SeriesCollection(1).Values = (
        f"='GymRun Volume Data'!$C$4:$C${last_row}"
    )

    excel_chart.SeriesCollection(1).XValues = (
        f"='GymRun Volume Data'!$B$4:$B${last_row}"
    )

    excel_chart.SeriesCollection(1).Name = (
        exercise_name
    )

    excel_chart.HasTitle = True

    excel_chart.ChartTitle.Text = (
            exercise_name + " Volumen"
    )

    excel_chart.Axes(1).HasTitle = True
    excel_chart.Axes(1).AxisTitle.Text = (
        "Datum"
    )

    excel_chart.Axes(2).HasTitle = True
    excel_chart.Axes(2).AxisTitle.Text = (
        "Volumen"
    )

    print(last_row)

    return volume_info
def create_volume_chart_data(
    dfGymVolume,
    exercise_name
):
    dfChart = dfGymVolume[
        ["Date", exercise_name]
    ].copy()

    dfChart = dfChart.dropna()

    return {
        "data": dfChart,
        "vol_min": GYM_EXERCISES[
            exercise_name
        ]["vol_min"],
        "vol_max": GYM_EXERCISES[
            exercise_name
        ]["vol_max"],
        "exercise_name": exercise_name
    }