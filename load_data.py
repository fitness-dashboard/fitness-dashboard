import pandas as pd
from pathlib import Path
import sys


def lade_daten():

    # ===============================
    # Neueste Tanita CSV finden
    # ===============================

    downloads_ordner = Path(
        r"D:\Documents\Eva\Fitness\CSV-Rohdaten"
    )

    passende_dateien = list(
        downloads_ordner.rglob(
            "csv_report_*.csv"
        )
    )

    if not passende_dateien:

        sys.exit(
            "Keine Tanita Datei gefunden."
        )

    file_tanita = max(
        passende_dateien,
        key=lambda datei: (
            datei.stat().st_mtime
        )
    )

    print(
        "Gefundene Datei:"
    )

    print(
        file_tanita
    )

    # ===============================
    # Tanita CSV laden
    # ===============================

    df = pd.read_csv(
        file_tanita
    )

    # ===============================
    # Datum umwandeln
    # ===============================

    df["Date"] = pd.to_datetime(
        df["Date"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce"
    )

    df["Only Date"] = (
        df["Date"].dt.date
    )

    # ===============================
    # Wichtige Spalten numerisch
    # ===============================

    numeric_columns = [
        "Weight (kg)",
        "BMI",
        "Body Fat (%)",
        "Muscle Mass (kg)",
        "BMR (kcal)",

        "Muscle mass - right arm",
        "Muscle mass - left arm",
        "Muscle mass - right leg",
        "Muscle mass - left leg",
        "Muscle mass - trunk",

        "Body fat (%) - right arm",
        "Body fat (%) - left arm",
        "Body fat (%) - right leg",
        "Body fat (%) - left leg",
        "Body fat (%) - trunk"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # ===============================
    # Muskelmasse Segmente bereinigen
    # ===============================

    segment_spalten = [

        "Muscle mass - right arm",
        "Muscle mass - left arm",
        "Muscle mass - right leg",
        "Muscle mass - left leg",
        "Muscle mass - trunk"
    ]

    for spalte in segment_spalten:

        if spalte in df.columns:

            df[spalte] = (
                df[spalte]
                .replace(
                    0,
                    pd.NA
                )
            )

    # ===============================
    # Körperfett in kg
    # ===============================

    df["Körperfettanteil kg"] = (

        df["Weight (kg)"]
        * df["Body Fat (%)"]
        / 100

    ).round(2)

    # ===============================
    # Nach Datum sortieren
    # ===============================

    df = (

        df
        .sort_values(
            "Date"
        )
        .drop_duplicates(
            subset=["Only Date"],
            keep="last"
        )

    )

    return df