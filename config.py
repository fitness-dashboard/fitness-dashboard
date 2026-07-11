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
    r"D:\Documents\GymRun Laptop"
)

TANITA_OLDDATA_FOLDER = Path(
    r"D:\Documents\Gesundheit Kai\Diät"
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
# Diät
# ==========================================================

DIET_START_DATE = "2025-06-14"
DIET_END_DATE = "2026-05-21"

ACTIVITY_FACTOR = 1.12