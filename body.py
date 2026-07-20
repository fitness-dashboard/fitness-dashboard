import pandas as pd


# ==========================================================
# Body DataFrame erzeugen
# ==========================================================

def build_body_dataframe(dfGesamt):

    dfGesamt = dfGesamt.reset_index(
        drop=True
    )

    dfBody = pd.DataFrame({

        "Day": range(
            1,
            len(dfGesamt) + 1
        ),

        "Date": dfGesamt["Only Date"],

        "Weight": dfGesamt[
            "Weight (kg)"
        ].round(1),

        "Weight 7 Days": dfGesamt[
            "Weight (kg) 7 Tage"
        ],

        "Body Fat %": dfGesamt[
            "Body Fat (%)"
        ],

        "Fat Mass": dfGesamt[
            "Körperfettanteil kg"
        ],

        "Muscle Mass": dfGesamt[
            "Muscle Mass (kg)"
        ],

        "BMI": dfGesamt["BMI"],

        "BMR": dfGesamt["BMR (kcal)"],

        "Visceral Fat": dfGesamt["Visc Fat"],

        "Body Water %": dfGesamt[
            "Body Water (%)"
        ],

        "Bone Mass": dfGesamt[
            "Bone Mass (kg)"
        ],

        "Metabolic Age": dfGesamt["Metab Age"],

        # --------------------------------------------------
        # Segment Muscle Mass (kg)
        # --------------------------------------------------

        "Muscle Right Arm": dfGesamt[
            "Muscle mass - right arm"
        ],

        "Muscle Left Arm": dfGesamt[
            "Muscle mass - left arm"
        ],

        "Muscle Trunk": dfGesamt[
            "Muscle mass - trunk"
        ],

        "Muscle Right Leg": dfGesamt[
            "Muscle mass - right leg"
        ],

        "Muscle Left Leg": dfGesamt[
            "Muscle mass - left leg"
        ],

        # --------------------------------------------------
        # Segment Body Fat (%)
        # --------------------------------------------------

        "Body Fat Right Arm": dfGesamt[
            "Body fat (%) - right arm"
        ],

        "Body Fat Left Arm": dfGesamt[
            "Body fat (%) - left arm"
        ],

        "Body Fat Trunk": dfGesamt[
            "Body fat (%) - trunk"
        ],

        "Body Fat Right Leg": dfGesamt[
            "Body fat (%) - right leg"
        ],

        "Body Fat Left Leg": dfGesamt[
            "Body fat (%) - left leg"
        ]

    })

    # --------------------------------------------------
    # 7-Tage-Durchschnitte
    # --------------------------------------------------

    dfBody["Body Fat % 7 Days"] = (
        dfBody["Body Fat %"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    dfBody["Fat Mass 7 Days"] = (
        dfBody["Fat Mass"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    dfBody["Muscle Mass 7 Days"] = (
        dfBody["Muscle Mass"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    # --------------------------------------------------
    # Segment Muscle Mass (7 Tage)
    # --------------------------------------------------

    dfBody["Muscle Right Arm 7 Days"] = (
        dfBody["Muscle Right Arm"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    dfBody["Muscle Left Arm 7 Days"] = (
        dfBody["Muscle Left Arm"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    dfBody["Muscle Trunk 7 Days"] = (
        dfBody["Muscle Trunk"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    dfBody["Muscle Right Leg 7 Days"] = (
        dfBody["Muscle Right Leg"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    dfBody["Muscle Left Leg 7 Days"] = (
        dfBody["Muscle Left Leg"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    # --------------------------------------------------
    # Segment Body Fat (7 Tage)
    # --------------------------------------------------

    dfBody["Body Fat Right Arm 7 Days"] = (
        dfBody["Body Fat Right Arm"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    dfBody["Body Fat Left Arm 7 Days"] = (
        dfBody["Body Fat Left Arm"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    dfBody["Body Fat Trunk 7 Days"] = (
        dfBody["Body Fat Trunk"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    dfBody["Body Fat Right Leg 7 Days"] = (
        dfBody["Body Fat Right Leg"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    dfBody["Body Fat Left Leg 7 Days"] = (
        dfBody["Body Fat Left Leg"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    return dfBody
