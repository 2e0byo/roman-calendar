from datetime import date, datetime, timedelta

latin_months = [
    "",
    "IAN",
    "FEB",
    "MART",
    "APR",
    "MAI",
    "IVN",
    "IVL",
    "AVG",
    "SEPT",
    "OCT",
    "NOV",
    "DEC",
]
latin_words = {"none": "NON.", "kalend": "KAL.", "ide": "ID."}
latin_numerals = [
    "",
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X",
    "XI",
    "XII",
    "XIII",
    "XIV",
    "XV",
    "XVI",
    "XVII",
    "XVIII",
    "XIX",
]


def roman_date(today: date) -> str:
    """
    Calculate roman date given calendar date.

    If you want this to be authentic, you'd better use the Julian
    Calendar.  But note that we don't actually know how the Julian
    calendar worked in antiquity, and dating is very much a guessing
    game.
    """
    next_month = today.month + 1 if today.month < 12 else 1
    next_month_year = today.year if next_month > 1 else today.year + 1

    if today.day == 1:
        kalend = date(day=2, month=today.month, year=today.year)
    else:
        kalend = date(day=2, month=next_month, year=next_month_year)

    long_months = (3, 5, 7, 10)

    if today.day > 15 and today.month in long_months:
        ide_month = next_month
        ide_year = next_month_year
    elif today.day > 13 and today.month not in long_months:
        ide_month = next_month
        ide_year = next_month_year
    else:
        ide_month = today.month
        ide_year = today.year

    if ide_month in long_months:
        ide = date(day=16, month=ide_month, year=ide_year)
    else:
        ide = date(day=14, month=ide_month, year=ide_year)

    none = ide - timedelta(days=8)

    # get next big date
    candidates = {"none": none, "ide": ide, "kalend": kalend}
    keys = sorted(candidates, key=lambda x: candidates[x] - today)
    for key in keys:
        candidate = candidates[key]
        if candidate - today < timedelta(days=0):  # in the past
            continue

        delta = candidate - today
        print(delta, key)

        if not delta:
            if key != "kalend":
                continue
            return f"KAL. {latin_months[candidate.month]}"
        if delta.days == 1:
            return f"{latin_words[key]} {latin_months[candidate.month]}."
        else:
            if delta.days == 2:
                return f"PRID. {latin_words[key]} {latin_months[candidate.month]}."
            else:
                # if key == "ide":
                #     days = delta.days + 1
                # else:
                days = delta.days
                return f"A.D. {latin_numerals[days]} {latin_words[key]} {latin_months[candidate.month]}."


def test_rom_cal():
    from csv import DictReader
    from pathlib import Path

    non_leap = {}
    leap = {}
    with Path("./cal.csv").open() as f:
        reader = DictReader(f)
        leaping = False
        for row in reader:
            if row["Modern"] == "Non-leap year":
                continue
            if row["Modern"] == "Leap year":
                leaping = True
                continue
            if row["Modern"] == "01 Mar":
                leaping = False

            if leaping:
                leap[row["Modern"]] = row["Full date"]
            else:
                non_leap[row["Modern"]] = row["Full date"]

    # 2021 is not a leap year
    for modern, old in non_leap.items():
        print(modern, old)
        d = datetime.strptime(f"{modern} 2021", "%d %b %Y").date()
        assert roman_date(d) == old

    # 2024 is
    non_leap.update(leap)
    for modern, old in non_leap.items():
        d = datetime.strptime(f"{modern} 2021", "%d %b %Y").date()
        assert roman_date(d) == old


if __name__ == "__main__":

    roman_date(date.today())
