"""
Backend module
"""
import csv


def init_db(path: str) -> dict:
    """
    DB from csv to dict
    """
    data = {}
    with open(path, 'r') as db:
        reader = csv.DictReader(db)
        headers = reader.fieldnames

        for record in reader:
            data[record[headers[0]]] = {
                k: v for k, v in record.items() if k != headers[0]
            }
    return data, headers


PATH = "utils/synergy_logistics_database.csv"
DB, HEADERS = init_db(PATH)


def filter_option(process: str, options: list) -> list:
    """
    Returns filtered registers by 
    """
    result = []
    for r in DB.values():
        flag = True
        for o in options:
            if r[process] != o:
                flag = False
                break
        if flag:
            result.append(r)
    return result
