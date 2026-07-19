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

    return dfBody