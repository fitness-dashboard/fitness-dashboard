import pandas as pd
from pathlib import Path
import sys


def lade_gymrun():

    # ==========================================
    # Neueste GymRun CSV finden
    # ==========================================

    downloads_ordner = Path(r"D:\Documents\Eva\Fitness\CSV-Rohdaten")

    dateien = list(
        downloads_ordner.rglob(
            "GymRun_*.csv"
        )
    )

    if not dateien:
        sys.exit(
            "Keine GymRun-Datei gefunden"
        )

    gymrun_datei = max(
        dateien,
        key=lambda x: x.stat().st_mtime
    )

    print("GymRun Datei gefunden:")
    print(gymrun_datei)

    # ==========================================
    # CSV laden
    # ==========================================

    dfGymRun = pd.read_csv(
        gymrun_datei,
        sep=";",
        decimal="."
    )

    # ==========================================
    # Datum umwandeln
    # ==========================================

    dfGymRun["Date"] = pd.to_datetime(
        dfGymRun["Date"],
        format="%d.%m.%Y",
        errors="coerce"
    )

    # ==========================================
    # Numerische Felder
    # ==========================================

    for col in [
        "Weight",
        "Reps"
    ]:

        if col in dfGymRun.columns:

            dfGymRun[col] = pd.to_numeric(
                dfGymRun[col],
                errors="coerce"
            )

    # ==========================================
    # Volumen berechnen
    # ==========================================

    dfGymRun["Volume"] = (
        dfGymRun["Weight"]
        * dfGymRun["Reps"]
    )

    # ==========================================
    # Brzycki 1RM
    # ==========================================

    dfGymRun["RM Brzycki"] = (
        dfGymRun["Weight"]
        * 36
        / (37 - dfGymRun["Reps"])
    )

    dfGymRun["RM Brzycki"] = (
        dfGymRun["RM Brzycki"]
        .round(1)
    )

    # ==========================================
    # Ungültige Werte entfernen
    # ==========================================

    dfGymRun.loc[
        dfGymRun["Reps"] >= 37,
        "RM Brzycki"
    ] = pd.NA

    # ==========================================
    # Sortieren
    # ==========================================

    dfGymRun = (
        dfGymRun
        .sort_values("Date")
        .reset_index(drop=True)
    )

    return dfGymRun