from datetime import timedelta

import pandas as pd


def get_week_of_month_iso(dates: pd.Series) -> pd.Series:
    """
    Calculate week-of-month for each date, where:
    - Weeks start on Monday and end on Sunday.
    - Week 1 always contains the 1st of the month.
    - If the 1st is on Saturday or Sunday, the week includes up to the next Saturday.
    """
    dates = pd.to_datetime(dates)
    week_of_month = []

    for date in dates:
        first_day = date.replace(day=1)
        first_week_start = first_day - timedelta(
            days=first_day.weekday()
        )  # Monday of the first week

        # Special case: if 1st is Saturday (5) or Sunday (6), shift start of Week 1 to that Saturday
        if first_day.weekday() in [5, 6]:
            first_week_start = first_day - timedelta(
                days=first_day.weekday() - 5
            )

        current_week_start = date - timedelta(days=date.weekday())
        wom = ((current_week_start - first_week_start).days // 7) + 1
        wom = max(wom, 1)  # Ensure minimum of 1
        week_of_month.append(wom)

    return pd.Series(week_of_month, index=dates.index)
