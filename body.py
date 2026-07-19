import pandas as pd


# ==========================================================
# Body DataFrame erzeugen
# ==========================================================

def build_body_dataframe(dfGesamt):

    rows = []

    day = 1

    for _, row in dfGesamt.iterrows():

        rows.append({

            "Day":
                day,

            "Date":
                row["Only Date"],

            "Weight":
                round(row["Weight (kg)"], 1)
                if not pd.isna(row["Weight (kg)"])
                else None,

            "Body Fat %":
                row["Body Fat (%)"],

            "Fat Mass":
                row["Körperfettanteil kg"],

            "Muscle Mass":
                row["Muscle Mass (kg)"],

            "BMI":
                row["BMI"],

            "BMR":
                row["BMR (kcal)"],

            "Visceral Fat":
                row["Visc Fat"],

            "Body Water %":
                row["Body Water (%)"],

            "Bone Mass":
                row["Bone Mass (kg)"],

            "Metabolic Age":
                row["Metab Age"],

            # --------------------------------------------------
            # Segment Muscle Mass (kg)
            # --------------------------------------------------

            "Muscle Right Arm":
                row["Muscle mass - right arm"],

            "Muscle Left Arm":
                row["Muscle mass - left arm"],

            "Muscle Trunk":
                row["Muscle mass - trunk"],

            "Muscle Right Leg":
                row["Muscle mass - right leg"],

            "Muscle Left Leg":
                row["Muscle mass - left leg"],

            # --------------------------------------------------
            # Segment Body Fat (%)
            # --------------------------------------------------

            "Body Fat Right Arm":
                row["Body fat (%) - right arm"],

            "Body Fat Left Arm":
                row["Body fat (%) - left arm"],

            "Body Fat Trunk":
                row["Body fat (%) - trunk"],

            "Body Fat Right Leg":
                row["Body fat (%) - right leg"],

            "Body Fat Left Leg":
                row["Body fat (%) - left leg"],

        })

        day += 1

    # --------------------------------------------------
    # DataFrame erzeugen
    # --------------------------------------------------

    dfBody = pd.DataFrame(rows)

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