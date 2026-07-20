import pandas as pd


def get_weekly_pr_counts(
        dfGymRM,
        start=None,
        end=None
):

    df = dfGymRM.copy()

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Date"]
    )

    exercise_columns = [
        column
        for column in df.columns
        if column != "Date"
    ]

    df = df.melt(
        id_vars="Date",
        value_vars=exercise_columns,
        var_name="Exercise",
        value_name="RM"
    )

    df["RM"] = pd.to_numeric(
        df["RM"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["RM"]
    )

    historical_max = pd.Series(
        dtype="float64"
    )

    if start is not None:

        start = pd.Timestamp(start)

        historical_max = (
            df[
                df["Date"] < start
            ]
            .groupby("Exercise")["RM"]
            .max()
        )

        df = df[
            df["Date"] >= start
        ]

    if end is not None:

        end = pd.Timestamp(end)

        df = df[
            df["Date"] <= end
        ]

    if df.empty:

        return pd.DataFrame(
            columns=[
                "Year",
                "Week",
                "PRs"
            ]
        )

    df = df.sort_values(
        [
            "Exercise",
            "Date"
        ]
    )

    df["Previous Max"] = df.groupby(
        "Exercise"
    )["RM"].transform(
        lambda values: values.cummax().shift()
    )

    df["Historical Max"] = df[
        "Exercise"
    ].map(
        historical_max
    )

    df["Previous Max"] = df[
        [
            "Previous Max",
            "Historical Max"
        ]
    ].max(
        axis=1
    )

    df = df[
        df["RM"] > df["Previous Max"]
    ].copy()

    df["Year"] = df["Date"].dt.isocalendar().year

    df["Week"] = df["Date"].dt.isocalendar().week

    return (
        df.groupby(
            [
                "Year",
                "Week"
            ],
            as_index=False
        )["Exercise"]
        .nunique()
        .rename(
            columns={
                "Exercise": "PRs"
            }
        )
    )


def build_dashboard_dataframe(
    dfFitness,
    dfBody,
    dfTraining,
    dfGymRM,
    period,
):
    """
    Erstellt eine Wochenübersicht für das Dashboard.
    Eine Zeile entspricht genau einer Kalenderwoche.
    """

    dfFitness = dfFitness.copy()
    dfBody = dfBody.copy()

    dfTraining = dfTraining.copy()

    period_prs = get_weekly_pr_counts(
        dfGymRM,
        start=period["start"],
        end=period["end"]
    )

    all_time_prs = get_weekly_pr_counts(
        dfGymRM
    )

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

    dashboard = dashboard.merge(
        period_prs,
        on=[
            "Year",
            "Week"
        ],
        how="left"
    )

    dashboard = dashboard.merge(
        all_time_prs.rename(
            columns={
                "PRs": "All time PRs"
            }
        ),
        on=[
            "Year",
            "Week"
        ],
        how="left"
    )

    dashboard["PRs"] = (
        dashboard["PRs"]
        .fillna(0)
        .astype(int)
    )

    dashboard["All time PRs"] = (
        dashboard["All time PRs"]
        .fillna(0)
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
