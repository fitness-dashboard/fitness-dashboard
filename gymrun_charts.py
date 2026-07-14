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
    exercise_name,
    index,
    data_sheet_name="Data GymRun One RM",
    chart_sheet_name="Charts GymRun"
):

    chart_info = create_rm_chart_data(
        dfGymMaxRM,
        exercise_name
    )



    rm_min = chart_info["rm_min"]
    rm_max = chart_info["rm_max"]

    dfChart = chart_info["data"]



    # Blatt holen oder anlegen
    try:
        wsGymRun = workbook.sheets[
            data_sheet_name
        ]
    except:
        wsGymRun = workbook.sheets.add(
            data_sheet_name
        )

    #wsGymRun.clear()

    try:
        wsGymRunCharts = workbook.sheets[
            chart_sheet_name
        ]
    except:
        wsGymRunCharts = workbook.sheets.add(
            chart_sheet_name
        )

    # Vorhandene Diagramme löschen

    # for chart in wsGymRunCharts.charts:
    #     chart.delete()

    start_col = 2 + index * 4

    column_pairs = [
        ("B", "C"),
        ("F", "G"),
        ("J", "K"),
        ("N", "O"),
        ("R", "S"),
        ("V", "W"),
        ("Z", "AA"),
        ("AD", "AE"),
        ("AH", "AI"),
        ("AL", "AM")
    ]

    date_col, value_col = (
        column_pairs[index]
    )

    # Titel

    wsGymRun.cells(
        1,
        start_col
    ).value = exercise_name


    wsGymRun.cells(
        1,
        start_col
    ).font.bold = True

    wsGymRun.cells(
        1,
        start_col
    ).font.size = 14

    # Daten

    wsGymRun.cells(
        3,
        start_col
    ).options(
        index=False
    ).value = dfChart



    last_row = len(dfChart) + 3

    # ===============================
    # Erstes GymRun Diagramm
    # ===============================

    chart = wsGymRunCharts.charts.add()

    chart.chart_type = "line"

    # chart.set_source_data(
    #     wsGymRun.range(
    #         f"A3:B{last_row}"
    #     )
    # )

    chart.top = 50 + index * 450
    chart.left = 50

    chart.width = 800
    chart.height = 400

    excel_chart = chart.api[1]

    excel_chart.SeriesCollection().NewSeries()

    excel_chart.SeriesCollection(1).Values = (
        f"='{data_sheet_name}'!"
        f"${value_col}$4:"
        f"${value_col}${last_row}"
    )

    excel_chart.SeriesCollection(1).XValues = (
        f"='{data_sheet_name}'!"
        f"${date_col}$4:"
        f"${date_col}${last_row}"
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
    exercise_name,
    index
):

    volume_info = create_volume_chart_data(
        dfGymVolume,
        exercise_name
    )

    dfChart = volume_info["data"]

    # ===============================
    # Datenposition berechnen
    # ===============================

    start_col = 2 + index * 4

    column_pairs = [
        ("B", "C"),
        ("F", "G"),
        ("J", "K"),
        ("N", "O"),
        ("R", "S"),
        ("V", "W"),
        ("Z", "AA"),
        ("AD", "AE"),
        ("AH", "AI"),
        ("AL", "AM")
    ]

    date_col, value_col = (
        column_pairs[index]
    )

    # ===============================
    # Blatt holen oder anlegen
    # ===============================

    try:
        wsGymRunVolume = workbook.sheets[
            "Data GymRun Volume"
        ]
    except:
        wsGymRunVolume = workbook.sheets.add(
            "Data GymRun Volume"
        )

    # Nicht mehr löschen
    # wsGymRunVolume.clear()

    # ===============================
    # Titel
    # ===============================

    wsGymRunVolume.cells(
        1,
        start_col
    ).value = exercise_name

    wsGymRunVolume.cells(
        1,
        start_col
    ).font.bold = True

    wsGymRunVolume.cells(
        1,
        start_col
    ).font.size = 14

    # ===============================
    # Daten schreiben
    # ===============================

    wsGymRunVolume.cells(
        3,
        start_col
    ).options(
        index=False
    ).value = dfChart

    last_row = len(dfChart) + 3

    # ===============================
    # Volumen Diagramm
    # ===============================

    try:
        wsGymRunCharts = workbook.sheets[
            "Charts GymRun"
        ]
    except:
        wsGymRunCharts = workbook.sheets.add(
            "Charts GymRun"
        )

    chart = wsGymRunCharts.charts.add()

    chart.chart_type = "line"

    chart.top = 50 + index * 450
    chart.left = 900

    chart.width = 800
    chart.height = 400

    excel_chart = chart.api[1]

    excel_chart.SeriesCollection().NewSeries()

    excel_chart.SeriesCollection(1).Values = (
        f"='Data GymRun Volume'!"
        f"${value_col}$4:"
        f"${value_col}${last_row}"
    )

    excel_chart.SeriesCollection(1).XValues = (
        f"='Data GymRun Volume'!"
        f"${date_col}$4:"
        f"${date_col}${last_row}"
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

    excel_chart.Axes(2).MinimumScale = (
        volume_info["vol_min"]
    )

    excel_chart.Axes(2).MaximumScale = (
        volume_info["vol_max"]
    )

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