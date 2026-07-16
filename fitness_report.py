import subprocess

from load_data import lade_daten
from load_gymrun import lade_gymrun
from calculations import berechne_werte
from excel_export import exportiere_excel
from charts import erstelle_diagramme
from gymrun_calculations import (build_gym_max_rm,build_gym_volume)
from gymrun_config import GYM_EXERCISES
from gymrun_charts import (
    create_rm_chart_data,
    create_volume_chart_data,
    create_all_rm_chart_data,
    create_all_volume_chart_data,
    create_rm_excel_chart,
    create_volume_excel_chart
)

from config import (
    DASHBOARD_NAME,
    VERSION,
    GYMRUN_RM_CSV_FILE,
    FITNESS_CSV_FILE,
    BIRTHDAY,
    HEIGHT_CM,
    ACTIVITY_FACTOR,
    DIET_START_DATE,
    NUTRITION_PHASES
)

import time

from nutrition import (
    build_nutrition_dataframe,
    build_weekly_nutrition_summary
)

from excel_formatting import (
    color_percentage_column,
    color_change_column,
    format_table
)
from training import (
    filter_training_block,
    get_training_block_summary,
    get_training_block_summary_df,
    get_new_prs
)

start = time.perf_counter()

print()
print("=" * 60)
print(f"{DASHBOARD_NAME}    Version {VERSION}")
print("=" * 60)
print()

print("Programm gestartet")


# =====================================
# GymRun laden
# =====================================

dfGymRun = lade_gymrun()

print(
    f"GymRun geladen: "
    f"{len(dfGymRun):,} Datensätze"
)


# =====================================
# MaxRM
# =====================================

dfGymMaxRM = build_gym_max_rm(dfGymRun)

dfGymMaxRM.to_csv(
    GYMRUN_RM_CSV_FILE,
    index=False
)

import os

print(
    "Arbeitsverzeichnis:"
)

print(
    os.getcwd()
)

print(
    "CSV Pfad:"
)

print(
    os.path.abspath(
        GYMRUN_RM_CSV_FILE
    )
)


print(
    "GymRun RM CSV exportiert."
)

all_rm_charts = create_all_rm_chart_data(
    dfGymMaxRM
)


print(
    f"MaxRM Auswertung erstellt: "
    f"{dfGymMaxRM.shape[0]} Trainingstage, "
    f"{dfGymMaxRM.shape[1]-1} Übungen"
)

# =====================================
# Volumen
# =====================================

dfGymVolume = build_gym_volume(dfGymRun)

volume_info = create_volume_chart_data(
    dfGymVolume,
    "Flachbankdrücken Langhantel"
)

print()
print("Zeitraum:")

print(
    f"Zeitraum: "
    f"{dfGymRun['Date'].min().date()} "
    f"bis "
    f"{dfGymRun['Date'].max().date()}"
)

print(
    f"Volumen Auswertung erstellt: "
    f"{dfGymVolume.shape[0]} Trainingstage, "
    f"{dfGymVolume.shape[1]-1} Übungen"
)

dfGesamt = lade_daten()
dfGesamt = berechne_werte(dfGesamt)

# =====================================
# Trainingsblock filtern
# =====================================

dfGymMaxRMBlock = filter_training_block(
    dfGymMaxRM
)

dfGymVolumeBlock = filter_training_block(
    dfGymVolume
)

# =====================================
# Training Block Summary
# =====================================

training_summary = (
    get_training_block_summary(
        dfGymMaxRM
    )
)

print()

print(
    "Training Block Summary:"
)

print(
    training_summary
)

# =====================================
# Training Block Summary DataFrame
# =====================================

dfTrainingSummary = (
    get_training_block_summary_df(
        dfGymMaxRM
    )
)

print()

print(
    "Training Block Summary DataFrame:"
)

print(
    dfTrainingSummary
)

new_prs = get_new_prs(
    dfGymMaxRM
)

average_delta_rm = round(
    new_prs["Δ RM"].mean(),
    1
)

print()

print(
    "New PRs:"
)

print(
    new_prs
)

# =====================================
# Ernährungsanalyse
# =====================================

dfNutrition = build_nutrition_dataframe(
    dfGesamt
)


# =====================================
# Wochenauswertung Ernährung
# =====================================

dfNutritionWeekly = (
    build_weekly_nutrition_summary(
        dfNutrition
    )
)

# =====================================
# CSV-Datei exportieren
# =====================================

dfGesamt.to_csv(
    FITNESS_CSV_FILE,
    index=False
)

# =====================================
# Excel-Datei öffnen
# =====================================

workbook = exportiere_excel(
    dfGesamt
)

# =====================================
# Excel-Blatt Data Nutrition
# =====================================

try:

    workbook.sheets[
        "Data Nutrition"
    ].delete()

    print(
        "Data Nutrition gelöscht"
    )

except:
    pass

sheetNutrition = workbook.sheets.add(
    "Data Nutrition"
)

sheetNutrition.range("A1").options(
    index=False
).value = dfNutrition

# =====================================
# Tabellenkopf formatieren
# =====================================

header = sheetNutrition.range(
    "A1:R1"
)

header.api.Font.Bold = True

header.api.Font.Color = 16777215

header.color = (
    31,
    78,
    121
)

# =====================================
# Spaltenbreite automatisch anpassen
# =====================================

sheetNutrition.autofit()

color_percentage_column(
    sheetNutrition,
    "I"
)

color_percentage_column(
    sheetNutrition,
    "L"
)

color_percentage_column(
    sheetNutrition,
    "O"
)

color_percentage_column(
    sheetNutrition,
    "R"
)

format_table(
    sheetNutrition,
    "A1:R1000"
)

print("Data Nutrition erstellt.")

# =====================================
# Excel-Blatt Nutrition Report
# =====================================

try:

    workbook.sheets[
        "Nutrition Report"
    ].delete()

    print(
        "Nutrition Report gelöscht"
    )

except:
    pass

sheetReport = workbook.sheets.add(
    "Nutrition Report"
)

# =====================================
# Überschrift
# =====================================

sheetReport.range("A1:N1").merge()

sheetReport.range("A1").value = (
    "Nutrition Report"
)

sheetReport.range("A1").api.Font.Bold = True
sheetReport.range("A1").api.Font.Size = 18
sheetReport.range("A1").api.HorizontalAlignment = -4108

sheetReport.range("A1").color = (
    31,
    78,
    121
)

sheetReport.range("A1").api.Font.Color = 16777215

# =====================================
# Ernährungsphase
# =====================================

sheetReport.range("A3:N3").merge()

sheetReport.range("A3").value = (
    NUTRITION_PHASES[0]["name"]
)

sheetReport.range("A3").api.Font.Bold = True
sheetReport.range("A3").api.Font.Size = 12
sheetReport.range("A3").api.HorizontalAlignment = -4108

# =====================================
# Kennzahlen
# =====================================

nutrition_days = (
    dfNutrition["Calories Actual"]
    .count()
)

weight_days = (
    dfNutrition["Weight"]
    .count()
)

total_days = len(dfNutrition)

sheetReport.range("A5").value = "Nutrition Days:"
sheetReport.range("B5").value = (
    f"{nutrition_days} of {total_days}"
)

sheetReport.range("A6").value = "Weight Days:"
sheetReport.range("B6").value = (
    f"{weight_days} of {total_days}"
)

sheetReport.range("D5").value = "Calories (%):"

sheetReport.range("E5").value = round(
    dfNutrition["Calories %"].mean(),
    1
)

sheetReport.range("D6").value = "Protein (%):"

sheetReport.range("E6").value = round(
    dfNutrition["Protein %"].mean(),
    1
)

sheetReport.range("G5").value = "Fat (%):"

sheetReport.range("H5").value = round(
    dfNutrition["Fat %"].mean(),
    1
)

sheetReport.range("G6").value = "Carbs (%):"

sheetReport.range("H6").value = round(
    dfNutrition["Carbs %"].mean(),
    1
)


# Kennzahlen fett

sheetReport.range("A5:A6").api.Font.Bold = True
sheetReport.range("D5:D6").api.Font.Bold = True
sheetReport.range("G5:G6").api.Font.Bold = True

# =====================================
# Excel-Blatt Training Block Report
# =====================================

try:

    workbook.sheets[
        "Training Block Report"
    ].delete()

except:
    pass

sheetTraining = workbook.sheets.add(
    "Training Block Report"
)

# =====================================
# Überschrift
# =====================================

sheetTraining.range("A1:E1").merge()

sheetTraining.range("A1").value = (
    "Training Block Report"
)

sheetTraining.range("A1").api.Font.Bold = True
sheetTraining.range("A1").api.Font.Size = 18
sheetTraining.range("A1").api.HorizontalAlignment = -4108

sheetTraining.range("A1").color = (
    31,
    78,
    121
)

sheetTraining.range("A1").api.Font.Color = 16777215

# =====================================
# Trainingsblock
# =====================================

sheetTraining.range("A3:F3").merge()

sheetTraining.range("A3").value = (
    training_summary["name"]
)

sheetTraining.range("A3").api.Font.Bold = True
sheetTraining.range("A3").api.Font.Size = 12
sheetTraining.range("A3").api.HorizontalAlignment = -4108

sheetTraining.range("A5").value = "Period:"

sheetTraining.range("B5").value = (
    training_summary["start"].strftime("%d.%m.%Y")
    + " - "
    + training_summary["end"].strftime("%d.%m.%Y")
)

sheetTraining.range("A6").value = "Training Days:"
sheetTraining.range("B6").value = training_summary["training_days"]

sheetTraining.range("A7").value = (
    "Exercises Improved:"
)
sheetTraining.range("B7").value = (
    f"{len(new_prs)} of {len(GYM_EXERCISES)}"
)

sheetTraining.range("D5").value = "Duration:"
sheetTraining.range("E5").value = (
    f'{training_summary["duration_days"]} days'
)

sheetTraining.range("D6").value = "Frequency:"
sheetTraining.range("E6").value = (
    f'{training_summary["frequency"]} / week'
)

sheetTraining.range("A5:A7").api.Font.Bold = True
sheetTraining.range("D5:D7").api.Font.Bold = True

sheetTraining.range("D7").value = (
    "Average Δ RM:"
)
sheetTraining.range("E7").value = (
    f"{average_delta_rm} kg"
)
sheetTraining.range("D5:D6").api.Font.Bold = True


sheetTraining.autofit()

# =====================================
# Neue Personal Records
# =====================================

sheetTraining.range("A9").value = (
    "Exercise Progress"
)

sheetTraining.range("A9").api.Font.Bold = True
sheetTraining.range("A9").api.Font.Size = 12

sheetTraining.range("A11").options(
    index=False
).value = new_prs


# =====================================
# Wochenübersicht
# =====================================

sheetReport.range("A9").options(
    index=False
).value = dfNutritionWeekly

header = sheetTraining.range("A11:E11")

header.api.Font.Bold = True

header.color = (
    221,
    235,
    247
)

table = sheetTraining.range(
    f"A11:E{len(new_prs)+11}"
)

table.api.Borders.Weight = 2

sheetTraining.autofit()

# =====================================
# Überschrift überschreiben
# =====================================

sheetReport.range("J9").value = "Δ Wt"

sheetReport.range("L9").value = "Δ Fat"

sheetReport.range("N9").value = "Δ Mus"

sheetReport.range("J:J").column_width = 8

sheetReport.range("L:L").column_width = 8

sheetReport.range("N:N").column_width = 8



header = sheetReport.range("A9:N9")

header.api.Font.Bold = True

header.color = (
    221,
    235,
    247
)

# =====================================
# Spalten automatisch anpassen
# =====================================

sheetReport.autofit()

# =====================================
# Bedingte Formatierung Veränderungen
# =====================================

color_change_column(
    sheetReport,
    "L",
    positive_good=False,
    first_row=10
)

color_change_column(
    sheetReport,
    "N",
    positive_good=True,
    first_row=10
)


# =====================================
# Rahmen
# =====================================

format_table(
    sheetReport,
    "A9:N100"
)

print(
    "Nutrition Report erstellt."
)

# ===============================
# Alte GymRun-Blätter löschen
# ===============================

for sheet_name in [
    "Data GymRun One RM",
    "Data GymRun Volume",
    "Charts GymRun"
]:

    try:
        workbook.sheets[
            sheet_name
        ].delete()

        print(
            f"{sheet_name} gelöscht"
        )

    except:
        pass



erstelle_diagramme(workbook, dfGesamt)

#Hilfe
# print(
#     len(GYM_EXERCISES)
# )

#Hilfe
print("Start Schleife")

# Schleife durch die Übungen
for index, exercise_name in enumerate(
    GYM_EXERCISES
):
    # =====================================
    # Historie
    # =====================================

    create_rm_excel_chart(
        workbook,
        dfGymMaxRM,
        exercise_name,
        index
    )

    create_volume_excel_chart(
        workbook,
        dfGymVolume,
        exercise_name,
        index
    )

    # =====================================
    # Trainingsblock
    # =====================================

    create_rm_excel_chart(
        workbook,
        dfGymMaxRMBlock,
        exercise_name,
        index,
        "Data Training Block RM",
        "Charts Training Block"
    )

    create_volume_excel_chart(
        workbook,
        dfGymVolumeBlock,
        exercise_name,
        index,
        "Data Training Block Volume",
        "Charts Training Block"
    )

# ===============================
# Tabellenblätter sortieren
# ===============================

sheet_order = [

    # =====================================
    # Rohdaten
    # =====================================

    "Data Food and Body",

    "Data Nutrition",

    "Data GymRun One RM",

    "Data GymRun Volume",

    "Data Training Block RM",

    "Data Training Block Volume",

    # =====================================
    # Reports
    # =====================================

    "Nutrition Report",

    # =====================================
    # Diagramme
    # =====================================

    "Charts Body",

    "Charts GymRun",

    "Charts Training Block",

    # =====================================
    # Dashboard
    # =====================================

    "Körper"

]

for i, sheet_name in enumerate(sheet_order):

    try:

        if i == 0:
            workbook.sheets[
                sheet_name
            ].api.Move(
                Before=workbook.sheets[1].api
            )

        else:
            workbook.sheets[
                sheet_name
            ].api.Move(
                After=workbook.sheets[
                    sheet_order[i - 1]
                ].api
            )

    except Exception as e:

        print(
            f"Fehler bei {sheet_name}: {e}"
        )

# ===============================
# GitHub automatisch aktualisieren
# ===============================

print("GymRun RM CSV exportiert.")

subprocess.run(
    ["git", "add", "."]
)

subprocess.run(
    ["git", "status"]
)

commit_result = subprocess.run(
    [
        "git",
        "commit",
        "-m",
        "Automatisches Dashboard Update"
    ],
    capture_output=True,
    text=True
)

if commit_result.returncode == 0:
    print("Git Commit erstellt.")
else:
    print("Keine Änderungen für Commit vorhanden.")

subprocess.run(
    ["git", "push"]
)



print("GitHub wurde aktualisiert.")

ende = time.perf_counter()

print()
print(f"Fertig in {ende-start:.1f} Sekunden.")