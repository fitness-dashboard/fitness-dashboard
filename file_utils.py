from pathlib import Path
from shutil import copy2
from datetime import datetime


# ==========================================================
# CSV-Datei archivieren
# ==========================================================

def archive_csv_file(
    source_file,
    destination_folder
):

    source = Path(source_file)

    destination = Path(
        destination_folder
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    new_name = (
        source.stem.split("-20")[0]
        + "_"
        + timestamp
        + source.suffix
    )

    copy2(
        source,
        destination / new_name
    )

    print(
        f"Archiviert: {new_name}"
    )

    if __name__ == "__main__":
        print("Test gestartet")

        archive_csv_file(
            ...
        )