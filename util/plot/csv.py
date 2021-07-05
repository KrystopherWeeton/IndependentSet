import csv


def write_2d_to_csv(
    row_headers, 
    col_headers, 
    M, 
    file_name, 
    delim=','
):
    if len(row_headers) != len(M):
        raise Exception("Size mismatch when writing to csv file.")
    rows: int = len(row_headers)
    cols: int = len(col_headers)

    with open(f"{file_name}.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=delim, quotechar='|', quoting=csv.QUOTE_MINIMAL)

        #? Write column headers
        first_row: [str] = [""] + col_headers
        m = [first_row] + [[row_headers[i]] + M[i] for i in range(rows)]
        writer.writerows(m)