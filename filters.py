import pandas as pd
import streamlit as st

from config import (
    TRAINING_BLOCK_SUMMARY_CSV_FILE,
    NUTRITION_PHASE_SUMMARY_CSV_FILE,
)


def _get_current_period_index(periods, today=None):
    """Index der aktuellen bzw. zuletzt begonnenen Phase ermitteln."""

    if periods.empty:
        return 0

    reference_date = (
        pd.Timestamp.today().normalize()
        if today is None
        else pd.Timestamp(today).normalize()
    )

    active_periods = periods[
        (periods["Start"] <= reference_date)
        & (periods["End"] >= reference_date)
    ]

    if not active_periods.empty:
        selected_label = active_periods["Start"].idxmax()
    else:
        started_periods = periods[
            periods["Start"] <= reference_date
        ]

        if not started_periods.empty:
            selected_label = started_periods["Start"].idxmax()
        else:
            selected_label = periods["Start"].idxmin()

    return periods.index.get_loc(selected_label)


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
            index=_get_current_period_index(training),
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
        index=_get_current_period_index(nutrition),
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
