from datetime import datetime
from config import TRAINING_BLOCKS
from gymrun_config import (
    GYM_EXERCISES
)


# ==========================================================
# Trainingsblock bestimmen
# ==========================================================

def get_training_block(date):

    if isinstance(
            date,
            str
    ):

        date = datetime.strptime(
            date,
            "%Y-%m-%d"
        )

    for block in TRAINING_BLOCKS:

        start = datetime.strptime(
            block["start"],
            "%Y-%m-%d"
        )

        end = datetime.strptime(
            block["end"],
            "%Y-%m-%d"
        )

        if start <= date <= end:

            return block

    return None

import pandas as pd


# ==========================================================
# Daten eines Trainingsblocks filtern
# ==========================================================

def filter_training_block(
        df,
        block_number=1
):

    block = next(

        (
            b for b in TRAINING_BLOCKS

            if b["block"] == block_number
        ),

        None

    )

    if block is None:

        return df.copy()

    start = pd.Timestamp(
        block["start"]
    )

    end = pd.Timestamp(
        block["end"]
    )

    return df[

        (df["Date"] >= start)

        &

        (df["Date"] <= end)

    ].copy()

# ==========================================================
# Training Block Kennzahlen
# ==========================================================

def get_training_block_summary(
        dfGymMaxRM,
        block_number=1
):

    df = filter_training_block(
        dfGymMaxRM,
        block_number
    )

    block = next(

        (
            b for b in TRAINING_BLOCKS

            if b["block"] == block_number
        ),

        None

    )

    if block is None:

        return None

    start = pd.Timestamp(
        block["start"]
    )

    if len(df) > 0:

        end = df["Date"].max()

    else:

        end = start

    training_days = len(df)

    duration_days = (
        end - start
    ).days + 1

    weeks = duration_days / 7

    frequency = round(
        training_days / weeks,
        1
    )

    return {

        "name": block["name"],

        "start": start,

        "end": end,

        "training_days": training_days,

        "duration_days": duration_days,

        "frequency": frequency

    }



# ==========================================================
# Neue Personal Records innerhalb eines Trainingsblocks
# ==========================================================

def get_new_prs(
        dfGymMaxRM,
        block_number=1
):

    # =====================================
    # Trainingsblock suchen
    # =====================================

    block = next(

        (
            b for b in TRAINING_BLOCKS

            if b["block"] == block_number
        ),

        None

    )

    if block is None:

        return None

    # =====================================
    # Startdatum des Trainingsblocks
    # =====================================

    start = pd.Timestamp(
        block["start"]
    )


    # =====================================
    # Alle Trainings innerhalb
    # des Trainingsblocks
    # =====================================

    dfBlock = filter_training_block(

        dfGymMaxRM,

        block_number

    )

    # =====================================
    # Ergebnisse sammeln
    # =====================================

    results = []

    # =====================================
    # Jede Übung einzeln prüfen
    # =====================================

    for exercise in GYM_EXERCISES:

        # -----------------------------
        # PR zu Beginn des Blocks
        # -----------------------------

        erste_werte = dfBlock[
            exercise
        ].dropna()

        if len(erste_werte) == 0:
            continue

        start_pr = erste_werte.iloc[0]

        # -----------------------------
        # Aktueller PR im Trainingsblock
        # -----------------------------

        current_pr = dfBlock[
            exercise
        ].max()

        # -----------------------------
        # Datum des aktuellen PR
        # -----------------------------

        current_pr_date = None

        if not pd.isna(current_pr):
            current_pr_date = dfBlock.loc[

                dfBlock[exercise] == current_pr,

                "Date"

            ].max()

        # -----------------------------
        # Falls vor dem Trainingsblock
        # noch kein Wert vorhanden war
        # -----------------------------

        if pd.isna(start_pr):

            erste_werte = dfBlock[
                exercise
            ].dropna()

            if len(erste_werte) == 0:
                continue

            start_pr = erste_werte.iloc[0]

        # -----------------------------
        # Keine Übung im Block
        # -----------------------------

        if pd.isna(current_pr):

            continue

        # -----------------------------
        # Nur Verbesserungen aufnehmen
        # -----------------------------

        if current_pr > start_pr:

            results.append({

                "Exercise":
                    exercise,

                "PR at Start":
                    round(
                        start_pr,
                        1
                    ),

                "Current PR":
                    round(
                        current_pr,
                        1
                    ),

                "Δ PR":
                    round(
                        current_pr - start_pr,
                        1
                    ),

                "Date":
                    current_pr_date.strftime(
                        "%d.%m.%Y"
                    )
            })

    # =====================================
    # Ergebnis zurückgeben
    # =====================================

    results = pd.DataFrame(results)

    results = results.sort_values(
        "Δ PR",
        ascending=False
    )

    results = results.reset_index(
        drop=True
    )

    return results