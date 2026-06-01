import pandas as pd
import numpy as np

def berechne_werte(dfGesamt):
    # ===============================
    # TAGES-AGGREGATION
    # ===============================
    dfGesamt["Only Date"] = pd.to_datetime(
        dfGesamt["Only Date"]
    )

    numeric_cols = dfGesamt.select_dtypes(
        include="number"
    ).columns.tolist()


    dfGesamt = dfGesamt.groupby(
        "Only Date",
        as_index=False
    )[numeric_cols].sum()

    segment_spalten = [
        "Muscle mass - right arm",
        "Muscle mass - left arm",
        "Muscle mass - right leg",
        "Muscle mass - left leg",
        "Muscle mass - trunk"
    ]

    for spalte in segment_spalten:
        dfGesamt[spalte] = (
            dfGesamt[spalte]
            .replace(0, np.nan)
        )
    # ===============================
    # LÜCKENLOSE ZEITREIHE erzeugen
    # ===============================
    alle_tage = pd.date_range(
        start=dfGesamt["Only Date"].min(),
        end=dfGesamt["Only Date"].max(),
        freq="D"
    )


    dfGesamt = (
        dfGesamt
        .set_index("Only Date")
        .reindex(alle_tage)
        .reset_index()
    )


    dfGesamt.rename(
        columns={"index": "Only Date"},
        inplace=True
    )


    dfGesamt["Only Date"] = pd.to_datetime(
        dfGesamt["Only Date"]
    )

    # ===============================
    # 0-Werte ignorieren damit Tage Durchschnitt nicht verfälscht wird
    # ===============================

    dfGesamt["Muscle Mass (kg)"] = (
        dfGesamt["Muscle Mass (kg)"]
        .replace(0, np.nan)
    )

    dfGesamt["Körperfettanteil kg"] = (
        dfGesamt["Körperfettanteil kg"]
        .replace(0, np.nan)
    )

    dfGesamt["Body Fat (%)"] = (
        dfGesamt["Body Fat (%)"]
        .replace(0, np.nan)
    )

    dfGesamt["Weight (kg)"] = (
        dfGesamt["Weight (kg)"]
        .replace(0, np.nan)
    )
    # ===============================
    # 7-Tage-Durchschnitt berechnen
    # ===============================
    dfGesamt["Muscle Mass (kg) 7 Tage"] = (
        dfGesamt["Muscle Mass (kg)"]
        .rolling(window=7, min_periods=1)
        .mean()
        .round(2)
    )

    dfGesamt["Körperfettanteil kg 7 Tage"] = (
        dfGesamt["Körperfettanteil kg"]
        .rolling(window=7, min_periods=1)
        .mean()
        .round(2)
    )

    dfGesamt["Body Fat (%) 7 Tage"] = (
        dfGesamt["Body Fat (%)"]
        .rolling(window=7, min_periods=1)
        .mean()
        .round(2)
    )

    dfGesamt["Weight (kg) 7 Tage"] = (
        dfGesamt["Weight (kg)"]
        .rolling(window=7, min_periods=1)
        .mean()
        .round(2)
    )

    # ===============================
    # Fett % Soll berechnen
    # ===============================

    start_datum = pd.Timestamp("2025-11-21")
    start_wert = 26.2

    # tägliche Reduktion
    reduktion_pro_tag = 1 / 30

    # Tage seit Startdatum berechnen
    tage_seit_start = (
        dfGesamt["Only Date"] - start_datum
    ).dt.days

    # Zielwert berechnen
    dfGesamt["Fett % Soll"] = (
        start_wert - tage_seit_start * reduktion_pro_tag
    ).round(2)

    # ===============================
    # Gewicht 500 kcal Soll berechnen
    # ===============================

    start_datum = pd.Timestamp("2025-06-14")

    start_wert_500kcal = (
        dfGesamt.loc[
            dfGesamt["Only Date"] == start_datum,
            "Weight (kg)"
        ]
        .iloc[0]
    )

    # tägliche Reduktion
    reduktion_pro_tag_500kcal = 1 / 14

    # Tage seit Startdatum berechnen
    tage_seit_start = (
            dfGesamt["Only Date"] - start_datum
    ).dt.days

    # Zielwert berechnen
    dfGesamt["Weight (kg) 500kcal"] = (
            start_wert_500kcal
            - tage_seit_start * reduktion_pro_tag_500kcal
    ).round(2)

    # ===============================
    # Gewicht 300 kcal Soll berechnen
    # ===============================

    start_datum = pd.Timestamp("2025-06-14")

    start_wert_300kcal = (
        dfGesamt.loc[
            dfGesamt["Only Date"] == start_datum,
            "Weight (kg)"
        ]
        .iloc[0]
    )

    reduktion_pro_tag_300kcal = 1 / 23.33

    tage_seit_start = (
            dfGesamt["Only Date"] - start_datum
    ).dt.days

    dfGesamt["Weight (kg) 300kcal"] = (
            start_wert_300kcal
            - tage_seit_start * reduktion_pro_tag_300kcal
    ).round(2)

    # ===============================
    # Kalorien durch Gewichtsänderung
    # ===============================

    dfGesamt["Kalorien Gewichtsreduktion"] = (
        (
            dfGesamt["Weight (kg)"].shift(1)
            - dfGesamt["Weight (kg)"]
        )
        * 7000
    ).round(0)


    # ===============================
    # Summe Kalorien aus Trainig letzte 30 Tage
    # ===============================

    dfGesamt["Kalorien aus Training Summe 30 Tage"] = (
        dfGesamt["Kalorien aus Training"]
        .rolling(window=30, min_periods=30)
        .sum()
        .round(0)
    )

    # ===============================
    # Summe Kalorien aus Essen letzte 30 Tage
    # ===============================

    dfGesamt["Kalorien aus Essen Summe 30 Tage"] = (
        dfGesamt["Kalorien"]
        .rolling(window=30, min_periods=30)
        .sum()
        .round(0)
    )

    # ===============================
    # Summe Kalorien aus Training letzte 60 Tage
    # ===============================

    dfGesamt["Kalorien aus Training Summe 60 Tage"] = (
        dfGesamt["Kalorien aus Training"]
        .rolling(window=60, min_periods=60)
        .sum()
        .round(0)
    )

    # ===============================
    # Summe Kalorien aus Essen letzte 60 Tage
    # ===============================

    dfGesamt["Kalorien aus Essen Summe 60 Tage"] = (
        dfGesamt["Kalorien"]
        .rolling(window=60, min_periods=60)
        .sum()
        .round(0)
    )

    # ===============================
    # Kalorien durch Gewichtsänderung
    # Vergleich heute vs vor 30 Tagen
    # ===============================

    gewicht_vor_30_tagen = (
        dfGesamt["Weight (kg) 7 Tage"]
        .shift(30)
    )

    dfGesamt["Kalorien Gewichtsänderung heute vs vor 30 Tage"] = (
            (
                    gewicht_vor_30_tagen
                    - dfGesamt["Weight (kg) 7 Tage"]
            )
            * 7000
    ).where(
        gewicht_vor_30_tagen.notna()
        &
        dfGesamt["Weight (kg) 7 Tage"].notna()
    ).round(0)


    # ===============================
    # Grundumsatz pro Tag errechnet 30 Tage
    # ===============================

    dfGesamt["Grundumsatz pro Tag errechnet 30 Tage"] = (
        (
            dfGesamt["Kalorien aus Essen Summe 30 Tage"]
            - dfGesamt["Kalorien aus Training Summe 30 Tage"]
            + dfGesamt["Kalorien Gewichtsänderung heute vs vor 30 Tage"]
        )
        / 30
    ).where(
        dfGesamt["Kalorien Gewichtsänderung heute vs vor 30 Tage"].notna()
    ).round(0)

    # ===============================
    # Kalorien durch Gewichtsänderung
    # Vergleich heute vs vor 60 Tagen
    # ===============================

    gewicht_vor_60_tagen = (
        dfGesamt["Weight (kg) 7 Tage"]
        .shift(60)
    )

    dfGesamt["Kalorien Gewichtsänderung heute vs vor 60 Tage"] = (
            (
                    gewicht_vor_60_tagen
                    - dfGesamt["Weight (kg) 7 Tage"]
            )
            * 7000
    ).where(
        gewicht_vor_60_tagen.notna()
        &
        dfGesamt["Weight (kg) 7 Tage"].notna()
    ).round(0)

    # ===============================
    # Grundumsatz pro Tag errechnet 60 Tage
    # ===============================

    dfGesamt["Grundumsatz pro Tag errechnet 60 Tage"] = (
            (
                    dfGesamt["Kalorien aus Essen Summe 60 Tage"]
                    - dfGesamt["Kalorien aus Training Summe 60 Tage"]
                    + dfGesamt["Kalorien Gewichtsänderung heute vs vor 60 Tage"]
            )
            / 60
    ).where(
        dfGesamt["Kalorien Gewichtsänderung heute vs vor 60 Tage"].notna()
    ).round(0)






    # ===============================
    # Grundumsatz nach Mifflin-St.-Jeor mit Faktor 1,12 (Den habe ich für mich rausgefunden)
    # ===============================

    geburtsdatum = pd.Timestamp("1975-01-19")

    # Alter berechnen
    dfGesamt["Alter"] = (
        (
            dfGesamt["Only Date"] - geburtsdatum
        ).dt.days / 365.25
    ).astype(int)

    # Mifflin-St.-Jeor Formel (Mann)
    dfGesamt["Grundumsatz Mifflin-St.-Jeor mit Faktor 1,12"] = (
        (
            10 * dfGesamt["Weight (kg)"]
            + 6.25 * 178
            - 5 * dfGesamt["Alter"]
            + 5
        )
        * 1.12
    ).round(0)

    return dfGesamt