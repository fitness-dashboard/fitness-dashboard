import pandas as pd

from config import NUTRITION_PHASES


# ==========================================================
# Ernährungsphase für ein Datum finden
# ==========================================================

def get_nutrition_phase(date):

    datum = pd.Timestamp(date)

    for phase in NUTRITION_PHASES:

        start = pd.Timestamp(phase["start"])
        end = pd.Timestamp(phase["end"])

        if start <= datum <= end:
            return phase

    return None


# ==========================================================
# Sollwerte berechnen
# ==========================================================

def calculate_macro_targets(
    date,
    weight,
    training_calories=0
):

    phase = get_nutrition_phase(date)

    if phase is None:
        return None

    calories = (
            phase["calories"]
            + training_calories
    )

    protein = round(
        weight * phase["protein_per_kg"]
    )

    fat = round(
        weight * phase["fat_per_kg"]
    )

    carbs = round(
        (
            calories
            - protein * 4
            - fat * 9
        ) / 4
    )

    return {

        "calories": calories,
        "protein": protein,
        "fat": fat,
        "carbs": carbs

    }




# ==========================================================
# Nutrition DataFrame erzeugen
# ==========================================================

def build_nutrition_dataframe(dfGesamt):

    dfGesamt = dfGesamt.reset_index(
        drop=True
    )

    dfNutrition = pd.DataFrame({

        "Day": range(
            1,
            len(dfGesamt) + 1
        ),

        "Date": dfGesamt["Only Date"],

        "Nutrition Phase": None,

        "Nutrition Phase name": None,

        "Weight": dfGesamt[
            "Weight (kg)"
        ].round(1),

        "Fat Mass": dfGesamt[
            "Körperfettanteil kg"
        ],

        "Muscle Mass": dfGesamt[
            "Muscle Mass (kg)"
        ],

        "Calories Target": float("nan"),

        "Calories Actual": dfGesamt[
            "Kalorien"
        ],

        "Calories %": float("nan"),

        "Protein Target": float("nan"),

        "Protein Actual": dfGesamt[
            "Eiweiß (g)"
        ],

        "Protein %": float("nan"),

        "Fat Target": float("nan"),

        "Fat Actual": dfGesamt[
            "Fett (g)"
        ],

        "Fat %": float("nan"),

        "Carbs Target": float("nan"),

        "Carbs Actual": dfGesamt[
            "Kohlenhydrate (g)"
        ],

        "Carbs %": float("nan")

    })

    for phase in NUTRITION_PHASES:

        phase_mask = (
            (dfNutrition["Date"] >= pd.Timestamp(phase["start"]))
            &
            (dfNutrition["Date"] <= pd.Timestamp(phase["end"]))
        )

        target_mask = (
            phase_mask
            &
            dfGesamt["Weight (kg)"].notna()
        )

        dfNutrition.loc[
            phase_mask,
            "Nutrition Phase"
        ] = f"Phase {phase['phase']}"

        dfNutrition.loc[
            phase_mask,
            "Nutrition Phase name"
        ] = phase["name"]

        training_calories = dfGesamt.loc[
            target_mask,
            "Kalorien aus Training"
        ].fillna(0)

        calories_target = (
            phase["calories"]
            + training_calories
        )

        protein_target = (
            dfGesamt.loc[
                target_mask,
                "Weight (kg)"
            ]
            * phase["protein_per_kg"]
        ).round()

        fat_target = (
            dfGesamt.loc[
                target_mask,
                "Weight (kg)"
            ]
            * phase["fat_per_kg"]
        ).round()

        carbs_target = (
            (
                calories_target
                - protein_target * 4
                - fat_target * 9
            )
            / 4
        ).round()

        dfNutrition.loc[
            target_mask,
            "Calories Target"
        ] = calories_target

        dfNutrition.loc[
            target_mask,
            "Protein Target"
        ] = protein_target

        dfNutrition.loc[
            target_mask,
            "Fat Target"
        ] = fat_target

        dfNutrition.loc[
            target_mask,
            "Carbs Target"
        ] = carbs_target

    dfNutrition["Calories %"] = (
        dfNutrition["Calories Actual"]
        / dfNutrition["Calories Target"]
        * 100
    ).round(1)

    dfNutrition["Protein %"] = (
        dfNutrition["Protein Actual"]
        / dfNutrition["Protein Target"]
        * 100
    ).round(1)

    dfNutrition["Fat %"] = (
        dfNutrition["Fat Actual"]
        / dfNutrition["Fat Target"]
        * 100
    ).round(1)

    dfNutrition["Carbs %"] = (
        dfNutrition["Carbs Actual"]
        / dfNutrition["Carbs Target"]
        * 100
    ).round(1)

    return dfNutrition
# ==========================================================
# Wochenauswertung Ernährung
# ==========================================================

def build_weekly_nutrition_summary(dfNutrition):

    import pandas as pd

    df = dfNutrition.copy()

    # =====================================
    # Ernährungswochen berechnen
    # =====================================

    start_date = df["Date"].min()

    df["Week"] = (
        (
            df["Date"] - start_date
        ).dt.days // 7
    ) + 1

    # =====================================
    # Zeitraum je Woche
    # =====================================

    period = (

        df.groupby("Week")["Date"]

        .agg(["min", "max"])

        .reset_index()

    )

    period["Period"] = (

        period["min"].dt.strftime("%d.%m.")

        + " - "

        + period["max"].dt.strftime("%d.%m.")

    )

    # =====================================
    # Wochendurchschnitte
    # =====================================

    dfWeekly = (

        df.groupby("Week", as_index=False)

        .agg({

            "Calories %": "mean",

            "Protein %": "mean",

            "Fat %": "mean",

            "Carbs %": "mean",

            "Weight": "mean",

            "Fat Mass": "mean",

            "Muscle Mass": "mean"

        })

    )

    # =====================================
    # Tracking Ernährung
    # =====================================

    nutrition_days = (

        df.groupby("Week")["Calories Actual"]

        .count()

        .reset_index(name="Nutrition Days")

    )

    nutrition_days["Nutrition"] = (

        nutrition_days["Nutrition Days"]

        .astype(str)

        + " of 7"

    )

    # =====================================
    # Tracking Gewicht
    # =====================================

    weight_days = (

        df.groupby("Week")["Weight"]

        .count()

        .reset_index(name="Weight Days")

    )

    weight_days["Weight Days"] = (

        weight_days["Weight Days"]

        .astype(str)

        + " of 7"

    )

    # =====================================
    # Alles zusammenführen
    # =====================================

    dfWeekly = dfWeekly.merge(

        period[
            ["Week", "Period"]
        ],

        on="Week"

    )

    dfWeekly = dfWeekly.merge(

        nutrition_days[
            ["Week", "Nutrition"]
        ],

        on="Week"

    )

    dfWeekly = dfWeekly.merge(

        weight_days[
            ["Week", "Weight Days"]
        ],

        on="Week"

    )

    # =====================================
    # Entwicklung zur Vorwoche
    # =====================================

    dfWeekly["Weight Change"] = (
        dfWeekly["Weight"]
        .diff()
    )

    dfWeekly["Fat Mass Change"] = (
        dfWeekly["Fat Mass"]
        .diff()
    )

    dfWeekly["Muscle Mass Change"] = (
        dfWeekly["Muscle Mass"]
        .diff()
    )

    # =====================================
    # Spalten sortieren
    # =====================================

    dfWeekly = dfWeekly[

        [

            "Week",

            "Period",

            "Nutrition",

            "Weight Days",

            "Calories %",

            "Protein %",

            "Fat %",

            "Carbs %",

            "Weight",

            "Weight Change",

            "Fat Mass",

            "Fat Mass Change",

            "Muscle Mass",

            "Muscle Mass Change"

        ]

    ]

    # =====================================
    # Runden
    # =====================================

    for col in [

        "Calories %",

        "Protein %",

        "Fat %",

        "Carbs %",

        "Weight",

        "Weight Change",

        "Fat Mass",

        "Fat Mass Change",

        "Muscle Mass",

        "Muscle Mass Change"

    ]:

        dfWeekly[col] = (

            dfWeekly[col]

            .round(1)

        )

    return dfWeekly


# ==========================================================
# Nutrition Phase Summary
# ==========================================================

def get_nutrition_phase_summary_df(dfNutrition):

    rows = []

    for phase in NUTRITION_PHASES:

        start = pd.Timestamp(phase["start"])
        end = pd.Timestamp(phase["end"])

        dfPhase = dfNutrition[
            (dfNutrition["Date"] >= start)
            &
            (dfNutrition["Date"] <= end)
        ].copy()

        if dfPhase.empty:
            continue

        rows.append({

            "Phase":
                phase["name"],

            "Start":
                start,

            "End":
                end,

            "Days":
                len(dfPhase),

            "Average Calories":
                round(
                    dfPhase["Calories Actual"].mean(),
                    0
                ),

            "Average Protein":
                round(
                    dfPhase["Protein Actual"].mean(),
                    1
                ),

            "Average Carbs":
                round(
                    dfPhase["Carbs Actual"].mean(),
                    1
                ),

            "Average Fat":
                round(
                    dfPhase["Fat Actual"].mean(),
                    1
                )

        })

    return pd.DataFrame(rows)

# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print(
        calculate_macro_targets(
            "2026-07-20",
            80
        )
    )
