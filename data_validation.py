def validate_required_columns(
        dataframe,
        required_columns,
        source_name
):

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:

        missing_columns_text = ", ".join(
            missing_columns
        )

        raise ValueError(
            f"{source_name}: Pflichtspalten fehlen: "
            f"{missing_columns_text}"
        )


def validate_non_empty_dataframe(
        dataframe,
        source_name
):

    if dataframe.empty:

        raise ValueError(
            f"{source_name}: Die Datei enthält keine Daten."
        )


def validate_dates(
        dataframe,
        date_column,
        source_name
):

    if dataframe[date_column].notna().any():

        return

    raise ValueError(
        f"{source_name}: Die Spalte {date_column} "
        f"enthält keine gültigen Datumswerte."
    )
