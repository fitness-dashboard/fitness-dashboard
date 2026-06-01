import subprocess

from load_data import lade_daten
from calculations import berechne_werte
from excel_export import exportiere_excel
from charts import erstelle_diagramme

print("Programm gestartet")


dfGesamt = lade_daten()
dfGesamt = berechne_werte(dfGesamt)

# CSV-Datei exportieren für Export nach Github
dfGesamt.to_csv(
    "fitness_dashboard_data.csv",
    index=False
)

workbook = exportiere_excel(dfGesamt)
erstelle_diagramme(workbook, dfGesamt)

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

print(commit_result.stdout)

subprocess.run(
    ["git", "push"]
)

print("GitHub wurde aktualisiert.")