import pandas as pd


import pandas as pd


def build_dashboard_dataframe(
    dfFitness,
    dfBody,
):
    """
    Erstellt eine Wochenübersicht für das Dashboard.
    Jede Zeile entspricht einer Kalenderwoche.
    """

    dfFitness = dfFitness.copy()

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

        row = {
            "Year": year,
            "Week": week_no,
            "Start": start,
            "End": end,
            "Period":
                f"{start:%d.%m.} - {end:%d.%m.}",

            "Calories":
                weekFitness["Kalorien"].mean(),

            "Protein":
                weekFitness["Eiweiß (g)"].mean(),

            "Fat":
                weekFitness["Fett (g)"].mean(),

            "Carbs":
                weekFitness["Kohlenhydrate (g)"].mean(),
        }

        rows.append(row)

    dashboard = pd.DataFrame(rows)

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

    return dashboard