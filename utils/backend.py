"""
Backend module
"""
import csv


# Read full db as DictReader
def connect_db():
    csv_file = open("utils/synergy_logistics_database.csv", "r")
    return csv.DictReader(csv_file)


def get_headers() -> list:
    return connect_db().fieldnames


def get_options(fieldname: str) -> list:
    result = []
    for row in connect_db():
        if row[fieldname] not in result:
            result.append(row[fieldname])
    return result


def get_total_options() -> dict:
    result = {}
    for field in get_headers():
        result[field] = get_options(field)
    return result


def tester():
    options = get_total_options()
    for o in options:
        print(f'{o}: {len(options[o])}')
