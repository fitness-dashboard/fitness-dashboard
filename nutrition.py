import pandas as pd

from config import NUTRITION_PHASES

#Hilfe
print("Hilfe für Kai")
print(NUTRITION_PHASES)

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

    rows = []

    day = 1

    for _, row in dfGesamt.iterrows():

        phase = get_nutrition_phase(
            row["Only Date"]
        )

        # =====================================
        # Sollwerte berechnen
        # =====================================

        targets = None

        if (
                phase is not None
                and not pd.isna(
                    row["Weight (kg)"]
                )
        ):
            targets = calculate_macro_targets(
                row["Only Date"],
                row["Weight (kg)"],
                row["Kalorien aus Training"]
                if not pd.isna(
                    row["Kalorien aus Training"]
                )
                else 0
            )

        rows.append({

            "Day":
                day,

            "Date":
                row["Only Date"],

            "Nutrition Phase":
                f"Phase {phase['phase']}"
                if phase is not None
                else None,

            "Weight":
                round(row["Weight (kg)"], 1)
                if not pd.isna(row["Weight (kg)"])
                else None,

            "Fat Mass":
                row["Körperfettanteil kg"],

            "Muscle Mass":
                row["Muscle Mass (kg)"],

            "Calories Target":
                targets["calories"]
                if targets
                else None,

            "Calories Actual":
                row["Kalorien"],

            "Calories %":
                round(
                    row["Kalorien"]
                    / targets["calories"]
                    * 100,
                    1
                )
                if (
                    targets
                    and not pd.isna(
                        row["Kalorien"]
                    )
                )
                else None,

            "Protein Target":
                targets["protein"]
                if targets
                else None,

            "Protein Actual":
                row["Eiweiß (g)"],

            "Protein %":
                round(
                    row["Eiweiß (g)"]
                    / targets["protein"]
                    * 100,
                    1
                )
                if (
                    targets
                    and not pd.isna(
                        row["Eiweiß (g)"]
                    )
                )
                else None,

            "Fat Target":
                targets["fat"]
                if targets
                else None,

            "Fat Actual":
                row["Fett (g)"],

            "Fat %":
                round(
                    row["Fett (g)"]
                    / targets["fat"]
                    * 100,
                    1
                )
                if (
                    targets
                    and not pd.isna(
                        row["Fett (g)"]
                    )
                )
                else None,

            "Carbs Target":
                targets["carbs"]
                if targets
                else None,

            "Carbs Actual":
                row["Kohlenhydrate (g)"],

            "Carbs %":
                round(
                    row["Kohlenhydrate (g)"]
                    / targets["carbs"]
                    * 100,
                    1
                )
                if (
                    targets
                    and not pd.isna(
                        row["Kohlenhydrate (g)"]
                    )
                )
                else None

        })

        day += 1

    return pd.DataFrame(rows)
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