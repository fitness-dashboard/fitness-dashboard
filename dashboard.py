import pandas as pd


import pandas as pd


def build_dashboard_dataframe(
    dfFitness,
    dfBody,
    dfTraining,
):
    """
    Erstellt eine Wochenübersicht für das Dashboard.
    Eine Zeile entspricht genau einer Kalenderwoche.
    """

    dfFitness = dfFitness.copy()
    dfBody = dfBody.copy()

    dfTraining = dfTraining.copy()

    dfTraining["Week"] = (
        dfTraining["Date"]
        .dt.isocalendar()
        .week
    )

    dfTraining["Year"] = (
        dfTraining["Date"]
        .dt.isocalendar()
        .year
    )

    dfFitness["Week"] = (
        pd.to_datetime(dfFitness["Only Date"])
        .dt.isocalendar()
        .week
    )

    dfFitness["Year"] = (
        pd.to_datetime(dfFitness["Only Date"])
        .dt.isocalendar()
        .year
    )

    rows = []

    weeks = (
        dfFitness[
            ["Year", "Week"]
        ]
        .drop_duplicates()
        .sort_values(
            ["Year", "Week"]
        )
    )

    for _, week in weeks.iterrows():

        year = week["Year"]
        week_no = week["Week"]

        weekFitness = dfFitness[
            (dfFitness["Year"] == year)
            &
            (dfFitness["Week"] == week_no)
        ].copy()

        start = weekFitness["Only Date"].min()
        end = weekFitness["Only Date"].max()

        weekBody = dfBody[
            (dfBody["Date"] >= start)
            &
            (dfBody["Date"] <= end)
        ].copy()

        weekTraining = dfTraining[
            (dfTraining["Year"] == year)
            &
            (dfTraining["Week"] == week_no)
            ].copy()

        # ======================================================
        # Zeitraum
        # ======================================================

        period_data = {
            "Year": year,
            "Week": week_no,
            "Start": start,
            "End": end,
            "Period": f"{start:%d.%m.} - {end:%d.%m.}",
        }

        # ======================================================
        # Ernährung
        # ======================================================

        nutrition_data = {
            "Calories": weekFitness["Kalorien"].mean(),
            "Protein": weekFitness["Eiweiß (g)"].mean(),
            "Fat": weekFitness["Fett (g)"].mean(),
            "Carbs": weekFitness["Kohlenhydrate (g)"].mean(),
            "Nutrition Days": weekFitness["Kalorien"].notna().sum(),
        }

        # ======================================================
        # Körper
        # ======================================================

        body_data = {
            "Weight": weekBody["Weight 7 Days"].mean(),
            "Body Fat": weekBody["Body Fat % 7 Days"].mean(),
            "Muscle": weekBody["Muscle Mass 7 Days"].mean(),
            "Weight Days": len(weekBody),
        }

        # ======================================================
        # Training
        # ======================================================

        training_data = {
            "Workout Days": weekTraining["Workout Days"].sum(),
            "PRs": weekTraining["PRs"].sum(),
            "Training Minutes": weekFitness["Minuten für dieses Training"].sum(),
            "Training Calories": weekFitness["Kalorien aus Training"].sum(),
        }

        # ======================================================
        # Gesamte Zeile
        # ======================================================

        row = (
            period_data
            | nutrition_data
            | body_data
            | training_data
        )

        rows.append(row)

    dashboard = pd.DataFrame(rows)

    dashboard["Calories"] = dashboard["Calories"].round(0)
    dashboard["Protein"] = dashboard["Protein"].round(0)
    dashboard["Fat"] = dashboard["Fat"].round(0)
    dashboard["Carbs"] = dashboard["Carbs"].round(0)

    dashboard["Weight"] = dashboard["Weight"].round(2)
    dashboard["Body Fat"] = dashboard["Body Fat"].round(1)
    dashboard["Muscle"] = dashboard["Muscle"].round(2)

    dashboard["Training Minutes"] = (
        dashboard["Training Minutes"]
        .fillna(0)
        .astype(int)
    )

    dashboard["Training Calories"] = (
        dashboard["Training Calories"]
        .fillna(0)
        .round(0)
        .astype(int)
    )

    # ======================================================
    # Veränderungen zur Vorwoche
    # ======================================================

    dashboard["Δ Weight"] = (
        dashboard["Weight"]
        .diff()
        .round(2)
    )

    dashboard["Δ Body Fat"] = (
        dashboard["Body Fat"]
        .diff()
        .round(1)
    )

    dashboard["Δ Muscle"] = (
        dashboard["Muscle"]
        .diff()
        .round(2)
    )

    return dashboard