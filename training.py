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

# ==========================================================
# Training Block DataFrame
# ==========================================================

import pandas as pd


def build_training_block_dataframe(
    dfGymMaxRM
):

    df = dfGymMaxRM.copy()

    rows = []

    for _, row in df.iterrows():

        block = get_training_block(
            row["Date"]
        )

        if block is None:
            continue

        row_dict = row.to_dict()

        row_dict["Training Block"] = (
            block["name"]
        )

        row_dict["Block"] = (
            block["block"]
        )

        rows.append(row_dict)

    return pd.DataFrame(rows)