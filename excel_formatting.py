

# ==========================================================
# Bedingte Formatierung für Prozentwerte
# ==========================================================

def color_percentage_column(sheet, column):

    last_row = sheet.range(
        f"{column}" + str(sheet.cells.last_cell.row)
    ).end("up").row

    for row in range(2, last_row + 1):

        cell = sheet.range(
            f"{column}{row}"
        )

        value = cell.value

        if value is None:
            continue

        # =====================================
        # Rot (< 90 % oder > 110 %)
        # =====================================

        if value < 90 or value > 110:

            cell.color = (
                255,
                199,
                206
            )

        # =====================================
        # Gelb (90–95 % oder 105–110 %)
        # =====================================

        elif value < 95 or value > 105:

            cell.color = (
                255,
                235,
                156
            )

        # =====================================
        # Grün (95–105 %)
        # =====================================

        else:

            cell.color = (
                198,
                239,
                206
            )


# ==========================================================
# Tabellen formatieren
# ==========================================================

def format_table(sheet, cell_range):

    table = sheet.range(
        cell_range
    )

    table.api.Borders.Weight = 2

# ==========================================================
# Bedingte Formatierung für Veränderungen
# ==========================================================

def color_change_column(
    sheet,
    column,
    positive_good=True,
    first_row=2
):

    last_row = sheet.range(
        f"{column}" + str(sheet.cells.last_cell.row)
    ).end("up").row

    for row in range(first_row, last_row + 1):

        cell = sheet.range(
            f"{column}{row}"
        )

        value = cell.value

        if not isinstance(
                value,
                (int, float)
        ):
            continue


        # =====================================
        # Positive Veränderung ist gut
        # =====================================

        if positive_good:

            if value > 0:

                cell.color = (
                    198,
                    239,
                    206
                )

            elif value < 0:

                cell.color = (
                    255,
                    199,
                    206
                )

            else:

                cell.color = (
                    255,
                    235,
                    156
                )

        # =====================================
        # Negative Veränderung ist gut
        # =====================================

        else:

            if value < 0:

                cell.color = (
                    198,
                    239,
                    206
                )

            elif value > 0:

                cell.color = (
                    255,
                    199,
                    206
                )

            else:

                cell.color = (
                    255,
                    235,
                    156
                )