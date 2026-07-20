import pandas as pd
from pathlib import Path
from config import (
    DOWNLOADS_FOLDER,
    TANITA_FOLDER,
    TANITA_OLDDATA_FILE,
    MFP_ARCHIVE_FOLDER
)
from file_utils import (
    archive_csv_file
)
from data_validation import (
    validate_dates,
    validate_non_empty_dataframe,
    validate_required_columns
)
from datetime import datetime

def lade_daten():

    # CSV import

    # ===============================
    # Neueste CSV-Datei automatisch finden
    # ===============================

    def finde_neueste_csv(
            start_string,
            suchordner
    ):

        suchordner = Path(suchordner)

        passende_dateien = list(
            suchordner.rglob(
                f"{start_string}*.csv"
            )
        )

        if not passende_dateien:
            raise FileNotFoundError(
                f"Keine Datei gefunden: {start_string}"
            )

        neueste_datei = max(
            passende_dateien,
            key=lambda datei: datei.stat().st_mtime
        )

        return str(neueste_datei)

    # ===============================
    # DATEI 1: Messwerte-Übersicht MyFitnessPal
    # ===============================
    file1 = finde_neueste_csv(
        "Messwerte-Übersicht-202",
        DOWNLOADS_FOLDER
    )

    print("Gefundene Datei:")
    print(file1)

    # ===============================
    # Messwerte-Übersicht MyFitnessPal CSV einlesen
    # ===============================

    dfMesswerte = pd.read_csv(file1)

    validate_non_empty_dataframe(
        dfMesswerte,
        "MyFitnessPal Messwerte"
    )

    validate_required_columns(
        dfMesswerte,
        [
            "Datum"
        ],
        "MyFitnessPal Messwerte"
    )

    dfMesswerte["Only Date"] = pd.to_datetime(
        dfMesswerte["Datum"],
        errors="coerce"
    ).dt.date

    validate_dates(
        dfMesswerte,
        "Only Date",
        "MyFitnessPal Messwerte"
    )

    dfMesswerte.drop(columns=["Datum"], inplace=True)

    # ===============================
    # DATEI 2: Nährwerte-Übersicht MyFitnessPal
    # ===============================

    file2 = finde_neueste_csv(
        "Nährwerte-Übersicht-202",
        DOWNLOADS_FOLDER
    )

    print("Gefundene Datei:")
    print(file2)

    # ===============================
    # Nährwerte-übersicht MyFitnessPal CSV einlesen
    # ===============================

    dfNaehrwerte = pd.read_csv(file2)

    validate_non_empty_dataframe(
        dfNaehrwerte,
        "MyFitnessPal Nährwerte"
    )

    validate_required_columns(
        dfNaehrwerte,
        [
            "Datum",
            "Kalorien",
            "Fett (g)",
            "Kohlenhydrate (g)",
            "Eiweiß (g)"
        ],
        "MyFitnessPal Nährwerte"
    )

    dfNaehrwerte["Only Date"] = pd.to_datetime(
        dfNaehrwerte["Datum"],
        errors="coerce"
    ).dt.date

    validate_dates(
        dfNaehrwerte,
        "Only Date",
        "MyFitnessPal Nährwerte"
    )

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
        "Trainingsübersicht-202",
        DOWNLOADS_FOLDER
    )

    print("Gefundene Datei:")
    print(file3)

    # ===============================
    # Zeitstempel für Archiv
    # ===============================

    import_timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    # ===============================
    # MyFitnessPal CSV-Dateien archivieren
    # ===============================

    archive_csv_file(
        file1,
        MFP_ARCHIVE_FOLDER,
        import_timestamp
    )

    archive_csv_file(
        file2,
        MFP_ARCHIVE_FOLDER,
        import_timestamp
    )

    archive_csv_file(
        file3,
        MFP_ARCHIVE_FOLDER,
        import_timestamp
    )

    # ===============================
    # Trainingsübersicht MyFitnessPal CSV einlesen
    # ===============================

    dfTrainingswerte = pd.read_csv(file3)

    validate_non_empty_dataframe(
        dfTrainingswerte,
        "MyFitnessPal Training"
    )

    validate_required_columns(
        dfTrainingswerte,
        [
            "Datum",
            "Kalorien aus Training",
            "Minuten für dieses Training"
        ],
        "MyFitnessPal Training"
    )

    dfTrainingswerte["Only Date"] = pd.to_datetime(
        dfTrainingswerte["Datum"],
        errors="coerce"
    ).dt.date

    validate_dates(
        dfTrainingswerte,
        "Only Date",
        "MyFitnessPal Training"
    )

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
        "csv_report_",
        TANITA_FOLDER
    )

    print("Gefundene Datei:")
    print(fileTanitaNeu)

    # ===============================
    # TANITA Altdaten einlesen
    # ===============================

    dfTanitaAlt = pd.read_csv(
        TANITA_OLDDATA_FILE
    )

    tanita_required_columns = [
        "Date",
        "Weight (kg)",
        "BMI",
        "Body Fat (%)",
        "Visc Fat",
        "Muscle Mass (kg)",
        "Bone Mass (kg)",
        "BMR (kcal)",
        "Metab Age",
        "Body Water (%)",
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

    validate_non_empty_dataframe(
        dfTanitaAlt,
        "Tanita Altdaten"
    )

    validate_required_columns(
        dfTanitaAlt,
        tanita_required_columns,
        "Tanita Altdaten"
    )

    # ===============================
    # TANITA aktuelle CSV einlesen
    # ===============================

    dfTanitaNeu = pd.read_csv(fileTanitaNeu)

    validate_non_empty_dataframe(
        dfTanitaNeu,
        "Tanita aktuelle Daten"
    )

    validate_required_columns(
        dfTanitaNeu,
        tanita_required_columns,
        "Tanita aktuelle Daten"
    )

    # ===============================
    # Datumsfelder getrennt umwandeln
    # ===============================

    dfTanitaAlt["Date"] = pd.to_datetime(
        dfTanitaAlt["Date"],
        format="%d.%m.%Y",
        errors="coerce"
    )

    dfTanitaNeu["Date"] = pd.to_datetime(
        dfTanitaNeu["Date"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce"
    )

    validate_dates(
        dfTanitaAlt,
        "Date",
        "Tanita Altdaten"
    )

    validate_dates(
        dfTanitaNeu,
        "Date",
        "Tanita aktuelle Daten"
    )

    # ===============================
    # Beide Dateien zusammenführen
    # ===============================

    dfTanitaNeu = pd.concat(
        [dfTanitaAlt, dfTanitaNeu],
        ignore_index=True
    )



    dfTanitaNeu["Only Date"] = (
        dfTanitaNeu["Date"].dt.date
    )

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
        dfTanitaNeu[spalte] = pd.to_numeric(
            dfTanitaNeu[spalte],
            errors="coerce"
        )

        dfTanitaNeu[spalte] = (
            dfTanitaNeu[spalte]
            .replace(0, pd.NA)
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
