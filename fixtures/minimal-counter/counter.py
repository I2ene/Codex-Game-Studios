"""Non-game fixture for workflow verification, with no private project data."""


def increment(value, limit):
    if isinstance(value, bool) or isinstance(limit, bool) or not isinstance(value, int) or not isinstance(limit, int):
        raise TypeError('integer inputs required')
    if value < 0 or limit < 0 or value > limit:
        raise ValueError('expected 0 <= value <= limit')
    return min(value + 1, limit)
