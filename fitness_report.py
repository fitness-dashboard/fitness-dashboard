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
# Ernährungsanalyse
# =====================================

dfNutrition = build_nutrition_dataframe(
    dfGesamt
)

print()
print("Nutrition Data:")
print(dfNutrition)

# =====================================
# Wochenauswertung Ernährung
# =====================================

dfNutritionWeekly = (
    build_weekly_nutrition_summary(
        dfNutrition
    )
)

print()
print("Weekly Nutrition:")
print(dfNutritionWeekly)

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

# =====================================
# Bereichsfarben
# =====================================

# Body
sheetNutrition.range(
    "D:F"
).color = (
    221,
    235,
    247
)

# Calories
sheetNutrition.range(
    "G:I"
).color = (
    252,
    228,
    214
)

# Protein
sheetNutrition.range(
    "J:L"
).color = (
    226,
    239,
    218
)

# Fat
sheetNutrition.range(
    "M:O"
).color = (
    255,
    242,
    204
)

# Carbs
sheetNutrition.range(
    "P:R"
).color = (
    232,
    220,
    247
)

# Kopfzeile erneut dunkelblau
header.color = (
    31,
    78,
    121
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

sheetReport.range("A1:K1").merge()

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

sheetReport.range("A3:K3").merge()

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
# Wochenübersicht
# =====================================

sheetReport.range("A9").options(
    index=False
).value = dfNutritionWeekly

header = sheetReport.range("A9:K9")

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
# Rahmen
# =====================================

table = sheetReport.range(
    "A9:K100"
)

table.api.Borders.Weight = 2

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

#Schleife durch die Übungen
for index, exercise_name in enumerate(
    GYM_EXERCISES
):

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

# ===============================
# Tabellenblätter sortieren
# ===============================

sheet_order = [
    "Data Food and Body",
    "Data GymRun Volume",
    "Data GymRun One RM",
    "Charts Body",
    "Charts GymRun",
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