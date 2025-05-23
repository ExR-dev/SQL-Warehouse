
def table_to_string(column_names: list[str], rows):
    """
    Converts the contents of a table to a string, formatted as a table.

    :param column_names: List of names for each column
    :param rows: Uniformly nested list of data
    """
    table_str = ""
    column_lengths = []

    for column_name in column_names:
        column_lengths.append(len(column_name)+2)

    for row in rows:
        column_i = 0
        for column in row:
            column_lengths[column_i] = max(column_lengths[column_i], len(str(column))+2)
            column_i += 1
            
    table_length = 1
    for column_length in column_lengths:
        table_length += column_length + 1

    table_str += ("—"*table_length) + "\n|"

    for column_i in range(len(column_names)):
        name = column_names[column_i]

        column_length = column_lengths[column_i]
        name_length = len(name)
        padding = max(0, column_length - name_length - 1)

        table_str += " " + name + (" "*padding) + "|"

    table_str += "\n" + ("—"*table_length) + "\n"

    for row in rows:
        table_str += "|"
        column_i = 0
        for column in row:
            data_string = str(column)

            column_length = column_lengths[column_i]
            data_length = len(data_string)
            padding = max(0, column_length - data_length - 1)
            table_str += " " + data_string + (" "*padding) + "|"
            column_i += 1
        table_str += "\n" + ("—"*table_length) + "\n"

    return table_str.removesuffix("\n")

def print_table(column_names: list[str], rows):
    """
    Print the contents of a table.

    :param column_names: List of names for each column
    :param rows: Uniformly nested list of data
    """
    print(table_to_string(column_names, rows))