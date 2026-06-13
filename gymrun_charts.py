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

    return chart_info