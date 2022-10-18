from csv import DictReader


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
