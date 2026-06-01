import xlwings as xw
import pandas as pd
import numpy as np

def exportiere_excel(dfGesamt):
    print("Excel Export gestartet")
    # ===============================
    # Excel-Datei öffnen oder vorhandene Instanz verwenden
    # ===============================

    excel_datei = r"D:\Documents\Gesundheit Kai\Diät\Gewicht mit Python.xlsm"

    if xw.apps.count > 0:
        app = xw.apps.active
    else:
        app = xw.App(visible=True)

    workbook = None

    # Prüfen ob Workbook bereits geöffnet ist
    for wb in app.books:

        if wb.fullname.lower() == excel_datei.lower():
            workbook = wb
            break

    # Falls nicht geöffnet → öffnen
    if workbook is None:
        workbook = app.books.open(excel_datei)

    # Worksheet auswählen
    wsData = workbook.sheets["Data"]

    # Excel schneller machen
    # app.screen_updating = False

    # Inhalte löschen
    wsData.clear_contents()
    wsData.clear_formats()

    print(
        dfGesamt[
            [
                "Muscle mass - right arm",
                "Muscle mass - left arm",
                "Muscle mass - right leg",
                "Muscle mass - left leg",
                "Muscle mass - trunk"
            ]
        ].describe()
    )

    # DataFrame schreiben
    wsData.range("A2").value = dfGesamt

    # ===============================
    # EXCEL Formatierung
    # ===============================
    wsData.range("A1").value = "Nr"

    wsData.api.Range("B1:C1").Merge()
    wsData.api.Range("B1:C1").Interior.Color = 5296274
    wsData.range("B1").api.HorizontalAlignment = -4108
    wsData.range("B1").value = "FitnessPal Messwerte"

    wsData.api.Range("D1:V1").Merge()
    wsData.api.Range("D1:V1").Interior.Color = 65535
    wsData.range("D1").api.HorizontalAlignment = -4108
    wsData.range("D1").value = "FitnessPal Nährwerte"

    wsData.api.Range("W1:AE1").Merge()
    wsData.api.Range("W1:AE1").Interior.Color = 16764057
    wsData.range("W1").api.HorizontalAlignment = -4108
    wsData.range("W1").value = "FitnessPal Training"

    wsData.api.Range("AF1:BE1").Merge()
    wsData.api.Range("AF1:BE1").Interior.Color = 255
    wsData.range("AF1").api.HorizontalAlignment = -4108
    wsData.range("AF1").value = "Waage Tanita Neu"



    # ===============================
    # Speichern
    # ===============================
    workbook.save()

    print("Excel-Datei erfolgreich aktualisiert.")

    return workbook
