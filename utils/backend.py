"""
Backend module
"""
import csv


PATH = "utils/synergy_logistics_database.csv"


def init_db(path: str) -> dict:
    """
    DB from csv to dict
    """
    data = {}
    countries = []
    transports = []
    with open(path, 'r') as db:
        reader = csv.DictReader(db)
        headers = reader.fieldnames
        for r in reader:
            # Dict
            data[r[headers[0]]] = {
                k: v for k, v in r.items() if k != headers[0]
            }
            # countries
            if r['destination'] not in countries:
                countries.append(r['destination'])
            if r['origin'] not in countries:
                countries.append(r['origin'])
            # transports
            if r['transport_mode'] not in transports:
                transports.append(r['transport_mode'])
    return data, countries, transports


DB, COUNTRIES, TRANSPORTS = init_db(PATH)


def directions():
    """
    # Imports - Exports
    """
    exports = [r for r in DB.values() if r['direction'] == 'Exports']
    imports = [r for r in DB.values() if r['direction'] == 'Imports']
    return exports, imports


def transported():
    """
    # Transport
    """
    return {
        t: [
            r for r in DB.values() if t == r['transport_mode']
        ] for t in TRANSPORTS
    }


def countries():
    """
    # Country
    """
    origin = {
        p: [r for r in DB.values() if p == r['origin']] for p in COUNTRIES
    }

    destin = {
        p: [r for r in DB.values() if p == r['destination']] for p in COUNTRIES
    }
    return origin, destin
