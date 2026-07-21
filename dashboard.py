import pandas as pd

from gymrun_config import GYM_EXERCISES


def get_weekly_pr_counts(
        dfGymRM,
        start=None,
        end=None,
        comparison_scope="all_time",
        exercises=None
):

    df = dfGymRM.copy()

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Date"]
    )

    if exercises is None:
        exercise_columns = [
            column for column in df.columns
            if column != "Date"
        ]
    else:
        exercise_columns = [
            exercise for exercise in exercises
            if exercise in df.columns
        ]

    if comparison_scope not in {"period", "all_time"}:

        raise ValueError(
            "comparison_scope must be 'period' or 'all_time'"
        )

    if not exercise_columns:

        return pd.DataFrame(
            columns=["Year", "Week", "PRs"]
        )

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

    start = pd.Timestamp(start) if start is not None else None
    end = pd.Timestamp(end) if end is not None else None

    # Perioden-PRs starten am Periodenanfang mit einer neuen Baseline.
    # All-Time-PRs werden zuerst gegen die komplette Historie geprueft
    # und erst danach auf den angezeigten Zeitraum eingeschraenkt.
    if comparison_scope == "period":

        if start is not None:
            df = df[df["Date"] >= start]

        if end is not None:
            df = df[df["Date"] <= end]

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

    df = df[
        df["RM"] > df["Previous Max"]
    ].copy()

    if comparison_scope == "all_time":

        if start is not None:
            df = df[df["Date"] >= start]

        if end is not None:
            df = df[df["Date"] <= end]

    df["Year"] = df["Date"].dt.isocalendar().year

    df["Week"] = df["Date"].dt.isocalendar().week

    return (
        df.groupby(
            [
                "Year",
                "Week"
            ],
            as_index=False
        )
        .size()
        .rename(
            columns={"size": "PRs"}
        )
    )


def get_dashboard_summary(
        dfFitness,
        dfBody,
        dfGymRM,
        period
):

    start = pd.Timestamp(
        period["start"]
    )

    end = pd.Timestamp(
        period["end"]
    )

    dfFitnessPeriod = dfFitness[
        (dfFitness["Only Date"] >= start)
        &
        (dfFitness["Only Date"] <= end)
    ].copy()

    dfBodyPeriod = dfBody[
        (dfBody["Date"] >= start)
        &
        (dfBody["Date"] <= end)
    ].copy()

    dfBodyMeasurements = dfBodyPeriod.dropna(
        subset=["Weight 7 Days"]
    )

    body_summary = {
        "Weight": None,
        "Weight Change": None,
        "Fat Mass": None,
        "Fat Mass Change": None,
        "Muscle Mass": None,
        "Muscle Mass Change": None,
        "Body Fat": None,
        "Body Fat Change": None
    }

    if not dfBodyMeasurements.empty:

        first = dfBodyMeasurements.iloc[0]
        latest = dfBodyMeasurements.iloc[-1]

        body_summary = {
            "Weight": latest["Weight 7 Days"],
            "Weight Change": (
                latest["Weight 7 Days"]
                - first["Weight 7 Days"]
            ),
            "Fat Mass": latest["Fat Mass 7 Days"],
            "Fat Mass Change": (
                latest["Fat Mass 7 Days"]
                - first["Fat Mass 7 Days"]
            ),
            "Muscle Mass": latest["Muscle Mass 7 Days"],
            "Muscle Mass Change": (
                latest["Muscle Mass 7 Days"]
                - first["Muscle Mass 7 Days"]
            ),
            "Body Fat": latest["Body Fat % 7 Days"],
            "Body Fat Change": (
                latest["Body Fat % 7 Days"]
                - first["Body Fat % 7 Days"]
            )
        }

    dfGymRM = dfGymRM.copy()

    dfGymRM["Date"] = pd.to_datetime(
        dfGymRM["Date"],
        errors="coerce"
    )

    dfGymRMPeriod = dfGymRM[
        (dfGymRM["Date"] >= start)
        &
        (dfGymRM["Date"] <= end)
    ].copy()

    exercise_columns = [
        exercise
        for exercise in GYM_EXERCISES
        if exercise in dfGymRMPeriod.columns
    ]

    improvements = []

    for exercise in exercise_columns:

        values = pd.to_numeric(
            dfGymRMPeriod[
                exercise
            ],
            errors="coerce"
        ).dropna()

        if values.empty:

            continue

        start_rm = values.iloc[0]
        best_rm = values.max()

        if best_rm > start_rm:

            improvements.append(
                best_rm - start_rm
            )

    all_time_prs = get_weekly_pr_counts(
        dfGymRM,
        start=start,
        end=end,
        comparison_scope="all_time",
        exercises=GYM_EXERCISES
    )["PRs"].sum()

    return {
        "Calories": dfFitnessPeriod["Kalorien"].mean(),
        "Protein": dfFitnessPeriod["Eiweiß (g)"].mean(),
        "Carbs": dfFitnessPeriod["Kohlenhydrate (g)"].mean(),
        "Fat": dfFitnessPeriod["Fett (g)"].mean(),
        **body_summary,
        "Exercises Improved": len(improvements),
        "Average Δ RM": (
            sum(improvements)
            / len(improvements)
            if improvements
            else None
        ),
        "All time PRs": all_time_prs,
        "Training Days": dfGymRMPeriod["Date"].nunique()
    }


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
        end=period["end"],
        comparison_scope="period",
        exercises=GYM_EXERCISES
    )

    all_time_prs = get_weekly_pr_counts(
        dfGymRM,
        comparison_scope="all_time",
        exercises=GYM_EXERCISES
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
