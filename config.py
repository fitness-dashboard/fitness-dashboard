from pathlib import Path

# ==========================================================
# Projektinformationen
# ==========================================================

DASHBOARD_NAME = "Dashboard Kai"
VERSION = "2.3.0"

# ==========================================================
# Dashboard
# ==========================================================

DASHBOARD_NAME = "Dashboard Kai"
VERSION = "2.3"

# ==========================================================
# Ordner
# ==========================================================

DOWNLOADS_FOLDER = Path(
    r"D:\Downloads"
)

GYMRUN_FOLDER = Path(
    r"D:\Documents\Gesundheit Kai\Fitness\CSV-Datei GymRun Laptop"
)

TANITA_OLDDATA_FOLDER = Path(
    r"D:\Documents\Gesundheit Kai\Fitness"
)

# ==========================================================
# Dateien
# ==========================================================

TANITA_OLDDATA_FILE = (
    TANITA_OLDDATA_FOLDER
    / "Altdaten Tanita Neu fertig.csv"
)

EXCEL_FILE = (
    TANITA_OLDDATA_FOLDER
    / "Gewicht mit Python.xlsm"
)

FITNESS_CSV_FILE = Path(
    "fitness_dashboard_data.csv"
)

GYMRUN_RM_CSV_FILE = Path(
    "gymrun_rm_data.csv"
)


# ==========================================================
# Persönliche Daten
# ==========================================================

BIRTHDAY = "1975-01-19"
HEIGHT_CM = 178
SEX = "male"

# ==========================================================
# Diät ab hier laufen 300 und 500 kcal Defiziet waagerecht
# ==========================================================

DIET_START_DATE = "2025-06-14"
DIET_END_DATE = "2026-05-21"

ACTIVITY_FACTOR = 1.12

# ==========================================================
# Ernährungsphasen
# ==========================================================

NUTRITION_PHASES = [

    {
        "phase": 1,
        "name": "Sommer Recomposition 2026 – 1900 kcal",

        "start": "2026-07-11",
        "end": "2030-12-31",

        "calories": 1900,
        "protein_per_kg": 2.0,
        "fat_per_kg": 0.7,
    },

]