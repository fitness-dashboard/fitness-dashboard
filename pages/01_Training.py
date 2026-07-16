import streamlit as st

from training import TRAINING_BLOCKS
from load_gymrun import lade_gymrun

from gymrun_calculations import (
    build_gym_max_rm
)

from training import (
    get_training_block_summary,
    get_new_prs
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
# GymRun laden
# =====================================

dfGymRun = lade_gymrun()

dfGymMaxRM = build_gym_max_rm(
    dfGymRun
)

training_summary = (
    get_training_block_summary(

        dfGymMaxRM,

        selected_block["block"]

    )
)

exercise_progress = get_new_prs(

    dfGymMaxRM,

    selected_block["block"]

)

# =====================================
# Training Block Report
# =====================================

st.subheader(
    training_summary["name"]
)

# =====================================
# Kennzahlen
# =====================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Training Days",
        training_summary["training_days"]
    )

    st.metric(
        "Period",
        (
            training_summary["start"].strftime("%d.%m.%Y")
            + " - "
            + training_summary["end"].strftime("%d.%m.%Y")
        )
    )

with col2:

    st.metric(
        "Frequency",
        f"{training_summary['frequency']} / week"
    )

    st.metric(
        "Duration",
        f"{training_summary['duration_days']} days"
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