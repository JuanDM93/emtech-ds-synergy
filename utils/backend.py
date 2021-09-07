"""
Backend module
"""
import csv


# Read full db as DictReader
def connect_db():
    """
    returns CSV DictReader of db
    """
    csv_file = open("utils/synergy_logistics_database.csv", "r")
    return csv.DictReader(csv_file)


HEADERS = connect_db().fieldnames


def get_all_values(field: str) -> str:
    """
    returns all values from field
    """
    return [row[field] for row in connect_db()]


def get_dif_values(field: str) -> list:
    """
    returns dif values from field
    """
    result = []
    for row in connect_db():
        if row[field] not in result:
            result.append(row[field])
    return result


def get_total_dif_options() -> dict:
    """
    returns values per fieldnames in db
    """
    result = {}
    for field in HEADERS:
        result[field] = get_dif_values(field)
    return result


def tester():
    options = get_total_dif_options()
    for field in HEADERS:
        results = options[field]
        print(f'{field}: {len(results)}')
        print(f'[:10] - {results[:10]}')
        print()
