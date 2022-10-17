def custom_sort(data: dict, key: str) -> dict:
    """
    Custom sorts dict from key
    """
    return sorted(
        data.items(),
        reverse=True,
        key=lambda item: item[-1][key]
    )
