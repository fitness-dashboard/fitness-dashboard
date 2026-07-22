import pandas as pd

from config import NUTRITION_PHASES, TRAINING_BLOCKS
from dashboard import (
    build_dashboard_dataframe,
    get_dashboard_summary,
    get_weekly_pr_counts,
)
from excel_utils import delete_sheet_if_exists
from gymrun_config import GYM_EXERCISES
from training import get_new_prs, get_training_block_summary


HEADER_COLOR = (31, 78, 121)
SUBHEADER_COLOR = (221, 235, 247)
WHITE = 16777215


def _new_sheet(workbook, name):
    delete_sheet_if_exists(workbook, name)
    return workbook.sheets.add(name)


def _title(sheet, text, last_column):
    area = sheet.range((1, 1), (1, last_column))
    area.merge()
    area.color = HEADER_COLOR
    area.api.Font.Color = WHITE
    area.api.Font.Bold = True
    area.api.Font.Size = 18
    area.api.HorizontalAlignment = -4108
    sheet.range("A1").value = text


def _section_header(sheet, row, column, text, width):
    area = sheet.range((row, column), (row, column + width - 1))
    area.merge()
    area.color = SUBHEADER_COLOR
    area.api.Font.Bold = True
    area.api.HorizontalAlignment = -4108
    sheet.range((row, column)).value = text


def _write_pairs(sheet, row, column, pairs):
    for offset, (label, value) in enumerate(pairs):
        target_row = row + offset
        sheet.range((target_row, column)).value = label
        sheet.range((target_row, column)).api.Font.Bold = True
        sheet.range((target_row, column + 1)).value = value


def _period_end(period, dates):
    configured_end = pd.Timestamp(period["end"])
    valid_dates = pd.to_datetime(dates, errors="coerce").dropna()
    if valid_dates.empty:
        return pd.Timestamp(period["start"])
    return min(configured_end, valid_dates.max())


def _body_summary(df_body, period):
    start = pd.Timestamp(period["start"])
    end = pd.Timestamp(period["end"])
    data = df_body[
        (df_body["Date"] >= start) & (df_body["Date"] <= end)
    ].copy()
    data = data.dropna(subset=["Weight 7 Days"])

    if data.empty:
        return None

    def values(column):
        valid = data.dropna(subset=[column])
        if valid.empty:
            return None
        start_value = valid.iloc[0][column]
        end_value = valid.iloc[-1][column]
        change = end_value - start_value
        return start_value, end_value, change

    return {
        "measurements": int(data["Weight"].notna().sum()),
        "start_date": data.iloc[0]["Date"],
        "end_date": data.iloc[-1]["Date"],
        "weight": values("Weight 7 Days"),
        "body_fat": values("Body Fat % 7 Days"),
        "fat_mass": values("Fat Mass 7 Days"),
        "muscle_mass": values("Muscle Mass 7 Days"),
    }


def create_training_block_report(workbook, df_gym_rm):
    sheet = _new_sheet(workbook, "Training Block Report")
    card_width = 7
    gap = 1
    last_column = len(TRAINING_BLOCKS) * (card_width + gap) - gap
    _title(sheet, "Training Block Report", last_column)

    for index, block in enumerate(TRAINING_BLOCKS):
        column = 1 + index * (card_width + gap)
        summary = get_training_block_summary(df_gym_rm, block["block"])
        progress = get_new_prs(df_gym_rm, block["block"])
        end = _period_end(block, df_gym_rm["Date"])
        period_prs = get_weekly_pr_counts(
            df_gym_rm,
            start=block["start"],
            end=block["end"],
            comparison_scope="period",
            exercises=GYM_EXERCISES,
        )["PRs"].sum()
        all_time_prs = get_weekly_pr_counts(
            df_gym_rm,
            start=block["start"],
            end=block["end"],
            comparison_scope="all_time",
            exercises=GYM_EXERCISES,
        )["PRs"].sum()

        _section_header(sheet, 3, column, block["name"], card_width)
        _write_pairs(sheet, 5, column, [
            ("Period:", f"{pd.Timestamp(block['start']):%d.%m.%Y} - {end:%d.%m.%Y}"),
            ("Training Days:", summary["training_days"]),
            ("Frequency:", f"{summary['frequency']} / week"),
            ("Exercises Improved:", f"{len(progress)} of {len(GYM_EXERCISES)}"),
            ("Average Δ RM:", round(progress["Δ RM"].mean(), 1) if not progress.empty else 0),
            ("Period PRs:", int(period_prs)),
            ("All-Time PRs:", int(all_time_prs)),
        ])

        sheet.range((13, column)).value = "Exercise Progress"
        sheet.range((13, column)).api.Font.Bold = True
        if not progress.empty:
            sheet.range((15, column)).options(index=False).value = progress
            sheet.range((15, column), (15, column + len(progress.columns) - 1)).color = SUBHEADER_COLOR
            sheet.range((15, column), (15, column + len(progress.columns) - 1)).api.Font.Bold = True

    sheet.autofit()
    return sheet


def create_nutrition_report(workbook, df_nutrition, df_weekly):
    sheet = _new_sheet(workbook, "Nutrition Report")
    card_width = 5
    gap = 1
    last_column = len(NUTRITION_PHASES) * (card_width + gap) - gap
    _title(sheet, "Nutrition Report", last_column)

    for index, phase in enumerate(NUTRITION_PHASES):
        column = 1 + index * (card_width + gap)
        start = pd.Timestamp(phase["start"])
        end = pd.Timestamp(phase["end"])
        data = df_nutrition[
            (df_nutrition["Date"] >= start) & (df_nutrition["Date"] <= end)
        ].copy()
        actual_end = _period_end(phase, df_nutrition["Date"])

        _section_header(sheet, 3, column, phase["name"], card_width)
        _write_pairs(sheet, 5, column, [
            ("Period:", f"{start:%d.%m.%Y} - {actual_end:%d.%m.%Y}"),
            ("Target Calories:", phase["calories"]),
            ("Nutrition Days:", f"{data['Calories Actual'].count()} of {len(data)}"),
            ("Weight Days:", f"{data['Weight'].count()} of {len(data)}"),
            ("Average Calories:", round(data["Calories Actual"].mean()) if not data.empty else None),
            ("Calories Target:", round(data["Calories %"].mean(), 1) if not data.empty else None),
            ("Average Protein:", round(data["Protein Actual"].mean(), 1) if not data.empty else None),
            ("Protein Target:", round(data["Protein %"].mean(), 1) if not data.empty else None),
            ("Average Fat:", round(data["Fat Actual"].mean(), 1) if not data.empty else None),
            ("Average Carbs:", round(data["Carbs Actual"].mean(), 1) if not data.empty else None),
        ])

    table_row = 17
    sheet.range((table_row, 1)).value = "Weekly Nutrition and Body Development"
    sheet.range((table_row, 1)).api.Font.Bold = True
    sheet.range((table_row + 2, 1)).options(index=False).value = df_weekly
    sheet.range((table_row + 2, 1), (table_row + 2, len(df_weekly.columns))).color = SUBHEADER_COLOR
    sheet.range((table_row + 2, 1), (table_row + 2, len(df_weekly.columns))).api.Font.Bold = True
    sheet.autofit()
    return sheet


def create_body_report(workbook, df_body):
    sheet = _new_sheet(workbook, "Body Report")
    periods = [("Training Block", item) for item in TRAINING_BLOCKS]
    periods += [("Nutrition Phase", item) for item in NUTRITION_PHASES]
    card_width = 5
    gap = 1
    last_column = max(len(TRAINING_BLOCKS), len(NUTRITION_PHASES)) * (card_width + gap) - gap
    _title(sheet, "Body Report (7-Day Averages)", last_column)

    section_rows = {"Training Block": 3, "Nutrition Phase": 18}
    section_indices = {"Training Block": 0, "Nutrition Phase": 0}

    for period_type, period in periods:
        index = section_indices[period_type]
        section_indices[period_type] += 1
        row = section_rows[period_type]
        column = 1 + index * (card_width + gap)
        summary = _body_summary(df_body, period)
        name = period["name"]

        _section_header(sheet, row, column, f"{period_type}: {name}", card_width)
        if summary is None:
            _write_pairs(sheet, row + 2, column, [("Status:", "No body data")])
            continue

        def metric(label, values, unit):
            if values is None:
                return (label, "No data")
            first, latest, change = values
            return (label, f"{first:.1f} → {latest:.1f} ({change:+.1f} {unit})")

        _write_pairs(sheet, row + 2, column, [
            ("Measured period:", f"{summary['start_date']:%d.%m.%Y} - {summary['end_date']:%d.%m.%Y}"),
            ("Measurement Days:", summary["measurements"]),
            metric("Weight:", summary["weight"], "kg"),
            metric("Body Fat:", summary["body_fat"], "%"),
            metric("Fat Mass:", summary["fat_mass"], "kg"),
            metric("Muscle Mass:", summary["muscle_mass"], "kg"),
        ])

    sheet.autofit()
    return sheet


def create_fitness_dashboard(
        workbook,
        df_fitness,
        df_body,
        df_training,
        df_gym_rm):
    sheet = _new_sheet(workbook, "Fitness Dashboard")
    last_column = 18
    _title(sheet, "Fitness Dashboard", last_column)

    periods = [("Training Block", item) for item in TRAINING_BLOCKS]
    periods += [("Nutrition Phase", item) for item in NUTRITION_PHASES]
    card_width = 5
    gap = 1
    rows = {"Training Block": 3, "Nutrition Phase": 17}
    indices = {"Training Block": 0, "Nutrition Phase": 0}

    for period_type, period in periods:
        index = indices[period_type]
        indices[period_type] += 1
        row = rows[period_type]
        column = 1 + index * (card_width + gap)
        summary = get_dashboard_summary(df_fitness, df_body, df_gym_rm, period)
        period_prs = get_weekly_pr_counts(
            df_gym_rm,
            start=period["start"],
            end=period["end"],
            comparison_scope="period",
            exercises=GYM_EXERCISES,
        )["PRs"].sum()

        _section_header(sheet, row, column, f"{period_type}: {period['name']}", card_width)
        _write_pairs(sheet, row + 2, column, [
            ("Calories:", round(summary["Calories"]) if pd.notna(summary["Calories"]) else None),
            ("Protein:", round(summary["Protein"], 1) if pd.notna(summary["Protein"]) else None),
            ("Weight:", round(summary["Weight"], 1) if summary["Weight"] is not None else None),
            ("Weight Change:", round(summary["Weight Change"], 1) if summary["Weight Change"] is not None else None),
            ("Muscle Mass:", round(summary["Muscle Mass"], 1) if summary["Muscle Mass"] is not None else None),
            ("Exercises Improved:", summary["Exercises Improved"]),
            ("Period PRs:", int(period_prs)),
            ("All-Time PRs:", int(summary["All time PRs"])),
            ("Training Days:", summary["Training Days"]),
        ])

    current_block = next(
        (
            block for block in TRAINING_BLOCKS
            if pd.Timestamp(block["start"]) <= pd.Timestamp.today().normalize()
            <= pd.Timestamp(block["end"])
        ),
        TRAINING_BLOCKS[-1],
    )
    weekly = build_dashboard_dataframe(
        df_fitness,
        df_body,
        df_training,
        df_gym_rm,
        current_block,
    )
    start = pd.Timestamp(current_block["start"])
    end = pd.Timestamp(current_block["end"])
    weekly = weekly[(weekly["Start"] >= start) & (weekly["Start"] <= end)].copy()
    table_columns = [
        "Week", "Period", "Calories", "Protein", "Fat", "Carbs",
        "Nutrition Days", "Weight", "Δ Weight", "Body Fat", "Δ Body Fat",
        "Muscle", "Δ Muscle", "Weight Days", "Workout Days", "PRs",
        "All time PRs",
    ]
    table_row = 32
    sheet.range((table_row, 1)).value = f"Weekly Dashboard – {current_block['name']}"
    sheet.range((table_row, 1)).api.Font.Bold = True
    sheet.range((table_row + 2, 1)).options(index=False).value = weekly[table_columns]
    sheet.range((table_row + 2, 1), (table_row + 2, len(table_columns))).color = SUBHEADER_COLOR
    sheet.range((table_row + 2, 1), (table_row + 2, len(table_columns))).api.Font.Bold = True
    sheet.autofit()
    return sheet


def create_all_excel_reports(
        workbook,
        df_fitness,
        df_nutrition,
        df_nutrition_weekly,
        df_body,
        df_training,
        df_gym_rm):
    create_training_block_report(workbook, df_gym_rm)
    create_nutrition_report(workbook, df_nutrition, df_nutrition_weekly)
    create_body_report(workbook, df_body)
    create_fitness_dashboard(
        workbook,
        df_fitness,
        df_body,
        df_training,
        df_gym_rm,
    )
