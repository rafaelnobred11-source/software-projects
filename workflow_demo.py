"""Run two synthetic examples of business workflow validation."""

from datetime import datetime, time, timedelta


def working_minutes(start, end, windows):
    """Count complete weekday minutes in ordered, non-overlapping local windows."""
    if end < start:
        raise ValueError("End precedes start")
    if start.tzinfo is not None or end.tzinfo is not None:
        raise ValueError("Use local timestamps without timezone offsets")
    windows = tuple(windows)
    for i, (opens, closes) in enumerate(windows):
        if opens >= closes or (i and windows[i - 1][1] > opens):
            raise ValueError("Use ordered working windows that do not overlap")
    elapsed = timedelta()
    day = start.date()
    while True:
        if day.weekday() < 5:
            for opens, closes in windows:
                overlap = min(end, datetime.combine(day, closes)) - max(
                    start, datetime.combine(day, opens)
                )
                elapsed += max(timedelta(), overlap)
        if day == end.date():
            break
        day += timedelta(days=1)
    return elapsed // timedelta(minutes=1)


def build_validation_rows(reference, template_keys):
    """Populate template keys from a reference export and flag missing values."""
    source = {}
    for key, cents in reference:
        if key in source:
            raise ValueError(f"Duplicate reference key: {key}")
        source[key] = cents

    rows = []
    seen = set()
    for key in template_keys:
        if key in seen:
            raise ValueError(f"Duplicate template key: {key}")
        seen.add(key)
        rows.append((key, source.get(key, 0), "matched" if key in source else "missing"))
    return rows


def main():
    workday = ((time(8), time(12)), (time(13), time(17)))
    friday = datetime(2026, 1, 9, 16, 30)
    monday = datetime(2026, 1, 12, 9, 15)
    print(f"Synthetic SLA: {working_minutes(friday, monday, workday)} minutes")

    matched = ("DEMO-01", "NORTH", "ITEM-A")
    missing = ("DEMO-01", "SOUTH", "ITEM-A")
    real_zero = ("DEMO-02", "NORTH", "ITEM-A")
    for key, cents, status in build_validation_rows(
        [(matched, 12500), (real_zero, 0)], [matched, missing, real_zero]
    ):
        print(*key, cents, status)


if __name__ == "__main__":
    main()
