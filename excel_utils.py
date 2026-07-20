def sheet_exists(workbook, sheet_name):

    return sheet_name in [
        sheet.name
        for sheet in workbook.sheets
    ]


def delete_sheet_if_exists(workbook, sheet_name):

    if not sheet_exists(
            workbook,
            sheet_name
    ):

        return False

    workbook.sheets[
        sheet_name
    ].delete()

    return True


def get_or_create_sheet(workbook, sheet_name):

    if sheet_exists(
            workbook,
            sheet_name
    ):

        return workbook.sheets[
            sheet_name
        ]

    return workbook.sheets.add(
        sheet_name
    )
