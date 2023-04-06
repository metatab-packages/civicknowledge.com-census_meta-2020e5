"""
Generate detailed decriptions for the columns
"""

def is_nan(v):
    from math import isnan
    try:
        return isnan(v)
    except TypeError:
        return False


def age(v):
    if v == 'all':
        return v
    l, h = v.split('-')
    return f"ages {int(l)} to  {int(h)} years"


def path(v):
    if is_nan(v):
        return 'all'

    return ', '.join(v.strip('/').split('/'))


def poverty(v):
    if v == 'all':
        return v

    return 'poverty ratio ' + v


def description(r):
    vals = [r.sex, r.raceeth, age(r.age), poverty(r.poverty_status), path(r.path)]

    vals = [e for e in vals if e != 'all']

    return r.title + " for " + r.universe + ", " + ', '.join(vals)

