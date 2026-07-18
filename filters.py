import pandas as pd
import streamlit as st

from config import (
    TRAINING_BLOCK_SUMMARY_CSV_FILE,
    NUTRITION_PHASE_SUMMARY_CSV_FILE,
)


def select_period():
    """
    Gemeinsamer Zeitraum-Filter für alle Seiten.

    Returns
    -------
    dict
        {
            "type": "Training Block" | "Nutrition Phase",
            "name": str,
            "key": str,
            "start": Timestamp,
            "end": Timestamp,
        }
    """

    # --------------------------------------------------
    # Daten laden
    # --------------------------------------------------

    training = pd.read_csv(
        TRAINING_BLOCK_SUMMARY_CSV_FILE,
        parse_dates=["Start", "End"],
    )

    nutrition = pd.read_csv(
        NUTRITION_PHASE_SUMMARY_CSV_FILE,
        parse_dates=["Start", "End"],
    )

    # --------------------------------------------------
    # Zeitraum basiert auf ...
    # --------------------------------------------------

    period_type = st.radio(
        "Period Based On",
        [
            "Training Block",
            "Nutrition Phase",
        ],
        horizontal=True,
    )

    # --------------------------------------------------
    # Training Block
    # --------------------------------------------------

    if period_type == "Training Block":

        period_name = st.selectbox(
            "Training Block",
            training["Name"],
        )

        row = training[
            training["Name"] == period_name
        ].iloc[0]

        return {
            "type": period_type,
            "name": period_name,
            "key": row["Block"],
            "start": row["Start"],
            "end": row["End"],
        }

    # --------------------------------------------------
    # Nutrition Phase
    # --------------------------------------------------

    period_name = st.selectbox(
        "Nutrition Phase",
        nutrition["Phase"],
    )

    row = nutrition[
        nutrition["Phase"] == period_name
    ].iloc[0]

    return {
        "type": period_type,
        "name": period_name,
        "key": row["Phase"],
        "start": row["Start"],
        "end": row["End"],
    }