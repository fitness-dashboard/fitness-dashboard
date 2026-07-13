from pathlib import Path
from shutil import copy2


# ==========================================================
# CSV-Datei archivieren
# ==========================================================

def archive_csv_file(
        source_file,
        destination_folder,
        timestamp
):
    """
    Kopiert eine CSV-Datei in das Archiv
    und ergänzt den Dateinamen um einen Zeitstempel.

    Beispiel:

    Messwerte-Übersicht-2025-05-31-bis-2026-07-13.csv

    →

    Messwerte-Übersicht_20260713_183015.csv
    """

    source = Path(source_file)

    destination = Path(
        destination_folder
    )

    # Zielordner bei Bedarf erstellen

    destination.mkdir(
        parents=True,
        exist_ok=True
    )

    # Dateinamen ohne Datumsbereich erzeugen

    base_name = source.stem.split(
        "-20"
    )[0]

    # Neuer Dateiname

    new_name = (
        f"{base_name}_{timestamp}"
        f"{source.suffix}"
    )

    # Datei kopieren

    copy2(
        source,
        destination / new_name
    )

    print(
        f"Archiviert: {new_name}"
    )