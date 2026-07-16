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
    TRAINING_BLOCK_SUMMARY_CSV_FILE,
    parse_dates=[
        "Start",
        "End"
    ]
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

left, right = st.columns(2)

with left:

    st.markdown("**Training Days**")
    st.markdown(f"### {training_summary['Training Days']}")

    st.markdown("**Frequency**")
    st.markdown(f"### {training_summary['Frequency']} / week")

    st.markdown("**Duration**")
    st.markdown(f"### {training_summary['Duration']} days")

with right:

    st.markdown("**Exercises Improved**")
    st.markdown(f"### {training_summary['Exercises Improved']}")

    st.markdown("**Average Δ RM**")
    st.markdown(f"### {training_summary['Average Δ RM']} kg")

    st.markdown("**Period**")
    st.markdown(
        f"### {training_summary['Start'].strftime('%d.%m.%Y')} - "
        f"{training_summary['End'].strftime('%d.%m.%Y')}"
    )

st.markdown("---")

# =====================================
# Exercise Progress
# =====================================

st.subheader(
    "Exercise Progress"
)

st.dataframe(

    exercise_progress.drop(
        columns=[
            "Block",
            "Name"
        ]
    ),

    use_container_width=True,
    hide_index=True

)

st.markdown("---")

# =====================================
# Exercise Chart
# =====================================

st.subheader(
    "Exercise Chart"
)

exercise = st.selectbox(

    "Exercise",

    sorted(
        exercise_progress["Exercise"].unique()
    )

)

view = st.radio(

    "View",

    [

        "Training Block",
        "All Time"

    ],

    horizontal=True

)

fig = create_exercise_chart(

    dfGymRM,

    exercise,

    selected_block,

    view

)

st.plotly_chart(

    fig,

    use_container_width=True

)