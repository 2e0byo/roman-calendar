from datetime import date, timedelta


def roman_date(today: date) -> str:
    """
    Calculate roman date given calendar date.

    If you want this to be authentic, you'd better use the Julian
    Calendar.  But note that we don't actually know how the Julian
    calendar worked in antiquity, and dating is very much a guessing
    game.
    """
    today = date.today()
    next_month = today.month + 1 if today.month < 12 else 1
    next_month_year = today.year if next_month > 1 else today.year + 1
    kalend = date(day=1, month=next_month, year=next_month_year)

    long_months = (3, 5, 7, 10)

    if today.day > 15 and today.month in long_months:
        ide_month = next_month
        ide_year = next_month_year
    elif today.day > 13:
        ide_month = next_month
        ide_year = next_month_year
    else:
        ide_month = today.month
        ide_year = today.year

    if ide_month in long_months:
        ide = date(day=15, month=ide_month, year=ide_year)
    else:
        ide = date(day=13, month=ide_month, year=ide_year)

    none = ide - timedelta(days=7)

    # get next big date
    candidates = {"none": none, "ide": ide, "kalend": kalend}
    keys = sorted(candidates, key=lambda x: candidates[x] - today)

    for key in keys:
        candidate = candidates[key]
        if candidate - today < timedelta(days=0):  # in the past
            continue
        return f"{(candidate - today).days} days before {key} of {candidate.month}th month year {candidate.year}"


roman_date(date.today())
