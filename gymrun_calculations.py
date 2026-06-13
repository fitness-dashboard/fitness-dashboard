import pandas as pd


def build_gym_max_rm(dfGymRun):

    dfMaxRM = (
        dfGymRun
        .groupby(
            ["Date", "Exercise"]
        )["RM Brzycki"]
        .max()
        .reset_index()
    )

    dfMaxRM = (
        dfMaxRM
        .pivot(
            index="Date",
            columns="Exercise",
            values="RM Brzycki"
        )
        .reset_index()
    )

    return dfMaxRM
def build_gym_volume(dfGymRun):

    dfVolume = (
        dfGymRun
        .groupby(
            ["Date", "Exercise"]
        )["Volume"]
        .sum()
        .reset_index()
    )

    dfVolume = (
        dfVolume
        .pivot(
            index="Date",
            columns="Exercise",
            values="Volume"
        )
        .reset_index()
    )

    return dfVolume