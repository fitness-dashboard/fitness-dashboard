from datetime import datetime

from config import TRAINING_BLOCKS


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
# Neue Personal Records
# ==========================================================

def get_new_prs(
        dfGymMaxRM,
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

        return None

    start = pd.Timestamp(
        block["start"]
    )

    dfBefore = dfGymMaxRM[
        dfGymMaxRM["Date"] <= start
    ]

    dfBlock = filter_training_block(
        dfGymMaxRM,
        block_number
    )

    print(dfBefore.head())

    print(dfBlock.head())

    return None