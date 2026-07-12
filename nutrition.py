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

def calculate_macro_targets(date, weight):

    phase = get_nutrition_phase(date)

    if phase is None:
        return None

    calories = phase["calories"]

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

        if phase is None:
            continue

        # =====================================
        # Sollwerte berechnen
        # =====================================

        targets = None

        if not pd.isna(
                row["Weight (kg)"]
        ):
            targets = calculate_macro_targets(
                row["Only Date"],
                row["Weight (kg)"]
            )

        rows.append({

            "Day":
                day,

            "Date":
                row["Only Date"],

            "Nutrition Phase":
                f"Phase {phase['phase']}",

            "Weight":
                round(row["Weight (kg)"], 1)
                if not pd.isna(row["Weight (kg)"])
                else None,

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
                        and not pd.isna(row["Kalorien"])
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
                        and not pd.isna(row["Eiweiß (g)"])
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
                        and not pd.isna(row["Fett (g)"])
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
                        and not pd.isna(row["Kohlenhydrate (g)"])
                )
                else None

        })

        day += 1

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