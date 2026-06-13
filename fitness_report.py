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

# CSV-Datei exportieren für Export nach Github
dfGesamt.to_csv(
    "fitness_dashboard_data.csv",
    index=False
)

workbook = exportiere_excel(dfGesamt)
erstelle_diagramme(workbook, dfGesamt)

#Hilfe
# print(
#     len(GYM_EXERCISES)
# )

#Hilfe
print("Start Schleife")

#Schleife durch die Übungen
for exercise_name in GYM_EXERCISES:

    print(exercise_name)

    create_rm_excel_chart(
        workbook,
        dfGymMaxRM,
        exercise_name
    )

    create_volume_excel_chart(
        workbook,
        dfGymVolume,
        exercise_name
    )

# ===============================
# GitHub automatisch aktualisieren
# ===============================

subprocess.run(
    ["git", "add", "."]
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