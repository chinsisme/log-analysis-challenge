def generate_insert_query(table_name, list_of_column_names, list_of_rows):
    columns = str(list_of_column_names).replace(
        "'", '').replace('[', '(').replace(']', ')')
    list_of_rows_string = []
    for row in list_of_rows:
        list_of_rows_string.append(
            str(row).replace('[', '(').replace(']', ')'))
    rows_string = ',\n'.join(list_of_rows_string)

    query = """
    INSERT INTO {} {}
    VALUES {};
    """.format(table_name, columns, rows_string)
    return query
