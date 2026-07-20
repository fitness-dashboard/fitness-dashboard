from pathlib import Path

# ==========================================================
# Projektinformationen
# ==========================================================

DASHBOARD_NAME = "Dashboard Kai"
VERSION = "2.5"

# ==========================================================
# Ordner
# ==========================================================

# Download-Ordner
# (MyFitnessPal ZIP-Export)

DOWNLOADS_FOLDER = Path(
    r"D:\Downloads"
)

# GymRun CSV-Dateien
# (Google Drive Synchronisation)

GYMRUN_FOLDER = Path(
    r"D:\Documents\Gesundheit Kai\Fitness\CSV-Datei GymRun Laptop"
)

# TANITA aktuelle CSV-Dateien

TANITA_FOLDER = Path(
    r"D:\Documents\Gesundheit Kai\Fitness\CSV-Dateien Tanita"
)

# MyFitnessPal Archiv

MFP_ARCHIVE_FOLDER = Path(
    r"D:\Documents\Gesundheit Kai\Fitness\CSV-Dateien MyFitnessPal"
)

# TANITA Altdaten

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
    / "Gewicht mit Python Kai.xlsm"
)

# ==========================================================
# Export-Dateien
# ==========================================================

DAILY_FITNESS_DATA_CSV_FILE = Path(
    "daily_fitness_data.csv"
)

GYMRUN_RM_CSV_FILE = Path(
    "gymrun_rm_data.csv"
)

NUTRITION_CSV_FILE = Path(
    "nutrition_data.csv"
)

BODY_CSV_FILE = Path(
    "body_data.csv"
)

NUTRITION_PHASE_SUMMARY_CSV_FILE = Path(
    "nutrition_phase_summary.csv"
)

TRAINING_BLOCK_SUMMARY_CSV_FILE = Path(
    "training_block_summary.csv"
)

TRAINING_BLOCK_PROGRESS_CSV_FILE = Path(
    "training_block_progress.csv"
)

TRAINING_DATA_CSV_FILE = Path(
    "training_data.csv"
)


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
        "name": "One Year Cut – 1600 kcal",

        "start": "2025-06-21",
        "end": "2026-01-21",

        "calories": 1600,
        "protein_per_kg": 2.0,
        "fat_per_kg": 0.7,
    },
    {
        "phase": 2,
        "name": "One Year Cut – 1400 kcal",

        "start": "2026-01-22",
        "end": "2026-06-07",

        "calories": 1400,
        "protein_per_kg": 2.0,
        "fat_per_kg": 0.7,
    },
    {
        "phase": 3,
        "name": "Sommer Recomposition 2026 – 1600 kcal",

        "start": "2026-06-08",
        "end": "2026-07-10",

        "calories": 1600,
        "protein_per_kg": 2.0,
        "fat_per_kg": 0.7,
    },
    {
        "phase": 4,
        "name": "Sommer Recomposition 2026 – 1900 kcal",

        "start": "2026-07-11",
        "end": "2030-12-31",

        "calories": 1900,
        "protein_per_kg": 2.0,
        "fat_per_kg": 0.7,
    },

]
# ==========================================================
# Trainingsblöcke
# ==========================================================

TRAINING_BLOCKS = [

    {
        "block": 1,
        "name": "One Year Cut",
        "start": "2025-06-21",
        "end": "2026-06-08",
    },
    {
        "block": 2,
        "name": "Clean Bulk No. 1",
        "start": "2026-06-09",
        "end": "2026-12-31",
    },


]
