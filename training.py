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