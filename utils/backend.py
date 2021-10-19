"""
Backend module
"""
from csv import DictReader


PATH = "utils/synergy_logistics_database.csv"


def init_db(path: str) -> dict:
    """
    DB from csv to dict
    """
    data = {}
    with open(path, 'r') as db:
        reader = DictReader(db)
        for r in reader:
            data[r['register_id']] = {
                k: v for k, v in r.items()
            }
    return data


DB = init_db(PATH)


def get_directions(direction: str = 'Imports', data=DB) -> dict:
    """
    Imports - Exports
    """
    imports = []
    exports = []
    for d in data:
        if data[d]['direction'] == direction:
            imports.append(data[d])
        else:
            exports.append(data[d])

    routes = []
    res_routes = {}
    for r in imports:
        route = f"{r['origin']}-{r['destination']}"
        if route not in routes:
            routes.append(route)
            res_routes[route] = {
                'cont': 0,
                'value': 0,
            }
        res_routes[route]['cont'] += 1
        res_routes[route]['value'] += int(r['total_value'])
    return res_routes


def get_transported(direction: str, data=DB) -> dict:
    """
    Transport
    """
    transports = []
    transported = {}
    for d in data:
        if direction != 'Globals':
            if data[d]['direction'] != direction:
                continue
        transport = data[d]['transport_mode']
        if transport not in transports:
            transports.append(transport)
            transported[transport] = {
                'cont': 0,
                'value': 0,
            }
        transported[transport]['cont'] += 1
        transported[transport]['value'] += int(data[d]['total_value'])

    return transported


def get_countries(direction: str, data=DB) -> dict:
    """
    Country
    """
    countries = []
    countries_dict = {}

    for d in data:
        if direction != 'Globals':
            if direction != data[d]['direction']:
                continue

        origin = data[d]['origin']
        if origin not in countries:
            countries.append(origin)
            countries_dict[origin] = {
                'origin': [],
                'destination': [],
            }
        countries_dict[origin]['origin'].append(data[d])

        destin = data[d]['destination']
        if destin not in countries:
            countries.append(destin)
            countries_dict[destin] = {
                'origin': [],
                'destination': [],
            }
        countries_dict[destin]['destination'].append(data[d])

    count_countries = {}
    for c in countries_dict:

        dest = {'cont': 0, 'value': 0}
        for r in countries_dict[c]['destination']:
            dest['cont'] += 1
            dest['value'] += int(r['total_value'])

        orig = {'cont': 0, 'value': 0}
        for r in countries_dict[c]['origin']:
            orig['cont'] += 1
            orig['value'] += int(r['total_value'])

        t_count = orig['cont'] + dest['cont']
        t_value = orig['value'] + dest['value']

        count_countries[c] = {
            'origin': orig,
            'dest': dest,
            't_count': t_count,
            't_value': t_value,
        }
    return count_countries


def custom_sort(data: dict, key: str) -> dict:
    """
    Custom sorts dict from key
    """
    return sorted(
        data.items(),
        reverse=True,
        key=lambda item: item[-1][key]
    )
