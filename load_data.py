import pandas as pd
from pathlib import Path
import sys


def lade_daten():

    # CSV import

    # ===============================
    # Neueste CSV-Datei automatisch finden
    # ===============================

    def finde_neueste_csv(start_string):

        downloads_ordner = Path(r"D:\Downloads")

        # Alle passenden CSV-Dateien suchen
        passende_dateien = list(
            downloads_ordner.rglob(
                f"{start_string}*.csv"
            )
        )

        # Prüfen ob Datei gefunden wurde
        if not passende_dateien:
            sys.exit(
                f"Keine Datei gefunden: {start_string}"
            )

        # Neueste Datei auswählen
        neueste_datei = max(
            passende_dateien,
            key=lambda datei: datei.stat().st_mtime
        )

        return str(neueste_datei)

    # ===============================
    # DATEI 1: Messwerte-Übersicht MyFitnessPal
    # ===============================
    file1 = finde_neueste_csv(
        "Messwerte-Übersicht-202"
    )

    print("Gefundene Datei:")
    print(file1)

    # ===============================
    # Messwerte-Übersicht MyFitnessPal CSV einlesen
    # ===============================

    dfMesswerte = pd.read_csv(file1)

    dfMesswerte["Only Date"] = pd.to_datetime(
        dfMesswerte["Datum"],
        errors="coerce"
    ).dt.date

    dfMesswerte.drop(columns=["Datum"], inplace=True)

    # ===============================
    # DATEI 2: Nährwerte-Übersicht MyFitnessPal
    # ===============================
    file2 = finde_neueste_csv(
        "Nährwerte-Übersicht-202"
    )

    print("Gefundene Datei:")
    print(file2)

    # ===============================
    # Nährwerte-übersicht MyFitnessPal CSV einlesen
    # ===============================

    dfNaehrwerte = pd.read_csv(file2)

    dfNaehrwerte["Only Date"] = pd.to_datetime(
        dfNaehrwerte["Datum"],
        errors="coerce"
    ).dt.date

    dfNaehrwerte.drop(columns=["Datum"], inplace=True)

    for col in dfNaehrwerte.columns:

        if col != "Only Date":
            dfNaehrwerte[col] = pd.to_numeric(
                dfNaehrwerte[col],
                errors="coerce"
            )

    dfNaehrwerte = dfNaehrwerte.groupby(
        "Only Date",
        as_index=False
    ).sum(numeric_only=True)

    # ===============================
    # DATEI 3: Trainingsübersicht MyFitnessPal
    # ===============================
    file3 = finde_neueste_csv(
        "Trainingsübersicht-202"
    )

    print("Gefundene Datei:")
    print(file3)

    # ===============================
    # Trainingsübersicht MyFitnessPal CSV einlesen
    # ===============================

    dfTrainingswerte = pd.read_csv(file3)

    dfTrainingswerte["Only Date"] = pd.to_datetime(
        dfTrainingswerte["Datum"],
        errors="coerce"
    ).dt.date

    dfTrainingswerte.drop(columns=["Datum"], inplace=True)

    for col in dfTrainingswerte.columns:

        if col != "Only Date":
            dfTrainingswerte[col] = pd.to_numeric(
                dfTrainingswerte[col],
                errors="coerce"
            )

    dfTrainingswerte = dfTrainingswerte.groupby(
        "Only Date",
        as_index=False
    ).sum(numeric_only=True)

    # ===============================
    # DATEI 4: TANITA neue Waage
    # ===============================
    fileTanitaNeu = finde_neueste_csv(
        "csv_report_"
    )

    print("Gefundene Datei:")
    print(fileTanitaNeu)

    # ===============================
    # TANITA Altdaten einlesen
    # ===============================

    dfTanitaAlt = pd.read_csv(
        r"D:\Documents\Gesundheit Kai\Diät\Altdaten Tanita Neu fertig.csv"
    )

    # ===============================
    # TANITA aktuelle CSV einlesen
    # ===============================

    dfTanitaNeu = pd.read_csv(fileTanitaNeu)

    # ===============================
    # Beide Dateien zusammenführen
    # ===============================

    dfTanitaNeu = pd.concat(
        [dfTanitaAlt, dfTanitaNeu],
        ignore_index=True
    )

    # ===============================
    # Datentypen umwandeln
    # ===============================

    dfTanitaNeu["Date"] = pd.to_datetime(
        dfTanitaNeu["Date"],
        errors="coerce",
        dayfirst=True
    )
    print(
        "Ungültige Datumswerte:",
        dfTanitaNeu["Date"].isna().sum()
    )


    print("Erstes Tanita-Datum:", dfTanitaNeu["Date"].min())
    print("Letztes Tanita-Datum:", dfTanitaNeu["Date"].max())
    print("Anzahl Tanita-Zeilen:", len(dfTanitaNeu))

    dfTanitaNeu["Only Date"] = dfTanitaNeu["Date"].dt.date

    dfTanitaNeu["Only Date"] = dfTanitaNeu["Date"].dt.date

    dfTanitaNeu["Weight (kg)"] = pd.to_numeric(
        dfTanitaNeu["Weight (kg)"],
        errors="coerce"
    )

    dfTanitaNeu["Body Fat (%)"] = pd.to_numeric(
        dfTanitaNeu["Body Fat (%)"],
        errors="coerce"
    )

    dfTanitaNeu["Muscle Mass (kg)"] = pd.to_numeric(
        dfTanitaNeu["Muscle Mass (kg)"],
        errors="coerce"
    )

    # ===============================
    # Körperfett in kg berechnen
    # ===============================

    dfTanitaNeu["Körperfettanteil kg"] = (
            dfTanitaNeu["Weight (kg)"]
            * dfTanitaNeu["Body Fat (%)"]
            / 100
    ).round(2)

    # ===============================
    # Nach Datum sortieren
    # ===============================

    dfTanitaNeu = (
        dfTanitaNeu
        .sort_values("Date")
        .drop_duplicates(
            subset=["Only Date"],
            keep="last"
        )
    )

    # ===============================
    # MERGE aller Daten
    # ===============================
    dfGesamt = dfMesswerte.copy()

    dfGesamt = dfGesamt.merge(
        dfNaehrwerte,
        on="Only Date",
        how="outer"
    )

    dfGesamt = dfGesamt.merge(
        dfTrainingswerte,
        on="Only Date",
        how="outer"
    )

    dfGesamt = dfGesamt.merge(
        dfTanitaNeu,
        on="Only Date",
        how="outer"
    )

    return dfGesamt