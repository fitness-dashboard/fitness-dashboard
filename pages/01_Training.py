import streamlit as st
import pandas as pd

from training import TRAINING_BLOCKS

from config import (
    TRAINING_BLOCK_SUMMARY_CSV_FILE,
    TRAINING_BLOCK_PROGRESS_CSV_FILE
)

st.title("💪 Training")

# =====================================
# Trainingsblock auswählen
# =====================================

block_names = [

    block["name"]

    for block in TRAINING_BLOCKS

]

selected_name = st.selectbox(

    "Training Block",

    block_names

)

selected_block = next(

    block

    for block in TRAINING_BLOCKS

    if block["name"] == selected_name

)

# =====================================
# CSV-Dateien laden
# =====================================

dfSummary = pd.read_csv(
    TRAINING_BLOCK_SUMMARY_CSV_FILE
)

dfProgress = pd.read_csv(
    TRAINING_BLOCK_PROGRESS_CSV_FILE
)

# =====================================
# Trainingsblock filtern
# =====================================

training_summary = dfSummary[
    dfSummary["Block"] == selected_block["block"]
].iloc[0]

exercise_progress = dfProgress[
    dfProgress["Block"] == selected_block["block"]
]

# =====================================
# Training Block Report
# =====================================

st.subheader(
    training_summary["Name"]
)

# =====================================
# Kennzahlen
# =====================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Training Days",
        training_summary["Training Days"]
    )

    st.metric(
        "Period",
        (
            training_summary["Start"].strftime("%d.%m.%Y")
            + " - "
            + training_summary["End"].strftime("%d.%m.%Y")
        )
    )

with col2:

    st.metric(
        "Frequency",
        f"{training_summary['Frequency']} / week"
    )

    st.metric(
        "Duration",
        f"{training_summary['Duration']} days"
    )

# =====================================
# Exercise Progress
# =====================================

st.subheader(
    "Exercise Progress"
)

st.dataframe(

    exercise_progress,

    use_container_width=True,
    hide_index=True

)