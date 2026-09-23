"""CSV storage for SplitIt. Every table is one file inside the data/ folder."""

import csv
import os

# The folder that holds the CSV files. Tests point this somewhere else.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# The columns of each table, in the order they appear in the file.
COLUMNS = {
    "groups": ["id", "name", "created_on"],
    "members": ["id", "group_id", "name"],
    "expenses": ["id", "group_id", "payer_id", "description", "amount", "date", "category"],
}


def table_path(table_name):
    """Return the full path of the CSV file behind one table."""
    return os.path.join(DATA_DIR, table_name + ".csv")


def load_table(table_name):
    """Read a whole table and return it as a list of dicts, one dict per row."""
    rows = []
    with open(table_path(table_name), newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows


def save_table(table_name, rows):
    """Overwrite a table with the given rows (a list of dicts)."""
    with open(table_path(table_name), "w", newline="", encoding="utf-8") as file:
        # lineterminator so the file looks the same on every computer
        writer = csv.DictWriter(file, fieldnames=COLUMNS[table_name], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def append_row(table_name, row):
    """Add one row (a dict) to the end of a table without rewriting the rest."""
    with open(table_path(table_name), "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS[table_name], lineterminator="\n")
        writer.writerow(row)


def next_id(table_name):
    """Return the id a new row of this table should get: the biggest id so far, plus one."""
    biggest = 0
    for row in load_table(table_name):
        if int(row["id"]) > biggest:
            biggest = int(row["id"])
    return biggest + 1
