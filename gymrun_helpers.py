import pandas as pd

from gymrun_config import GYM_EXERCISES


def get_exercise_rm(
    dfGymMaxRM,
    exercise_name
):

    start_date = pd.Timestamp(
        GYM_EXERCISES[exercise_name]["start_date"]
    )

    dfExercise = (
        dfGymMaxRM[
            ["Date", exercise_name]
        ]
        .dropna()
        .copy()
    )

    dfExercise = dfExercise[
        dfExercise["Date"] >= start_date
    ]

    return dfExercise

def get_exercise_volume(
    dfGymVolume,
    exercise_name
):

    start_date = pd.Timestamp(
        GYM_EXERCISES[exercise_name]["start_date"]
    )

    dfExercise = (
        dfGymVolume[
            ["Date", exercise_name]
        ]
        .dropna()
        .copy()
    )

    dfExercise = dfExercise[
        dfExercise["Date"] >= start_date
    ]

    return dfExercise