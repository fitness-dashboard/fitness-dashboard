import pandas as pd


def build_dashboard_dataframe(
    dfFitness,
    dfBody,
):
    """
    Erstellt die Wochenübersicht für das Dashboard.

    Aktuell wird nur eine Zeile pro Kalenderwoche erzeugt.
    Weitere Kennzahlen werden anschließend Schritt für Schritt ergänzt.
    """

    df = dfFitness.copy()

    df["Week"] = (
        pd.to_datetime(df["Only Date"])
        .dt.isocalendar()
        .week
    )

    df["Year"] = (
        pd.to_datetime(df["Only Date"])
        .dt.year
    )

    dashboard = (
        df.groupby(
            ["Year", "Week"],
            as_index=False
        )
        .agg(
            Start=("Only Date", "min"),
            End=("Only Date", "max"),

            Calories=("Calories (kcal)", "mean"),
            Protein=("Protein (g)", "mean"),
            Fat=("Fat (g)", "mean"),
            Carbs=("Carbohydrates (g)", "mean"),
        )
    )

    dashboard["Calories"] = (
        dashboard["Calories"]
        .round(0)
    )

    dashboard["Protein"] = (
        dashboard["Protein"]
        .round(0)
    )

    dashboard["Fat"] = (
        dashboard["Fat"]
        .round(0)
    )

    dashboard["Carbs"] = (
        dashboard["Carbs"]
        .round(0)
    )

    dashboard["Period"] = (
        dashboard["Start"].dt.strftime("%d.%m.")
        + " - "
        + dashboard["End"].dt.strftime("%d.%m.")
    )

    return dashboard