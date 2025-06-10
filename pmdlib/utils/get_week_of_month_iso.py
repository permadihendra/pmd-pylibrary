from datetime import timedelta

import pandas as pd


def get_week_of_month_iso(dates: pd.Series) -> pd.Series:
    """
    Calculate week-of-month for each date, where:
    - Weeks start on Monday and end on Sunday.
    - Week 1 starts from the first Monday in the same calendar month.
    - usage : df['week_of_month'] = get_week_of_month_iso(df['datetime_column']).
    """
    dates = pd.to_datetime(dates)
    week_of_month = []

    for date in dates:
        # Get the Monday of the week the date belongs to
        current_week_start = date - timedelta(days=date.weekday())

        # Get the first day of the month
        first_day = date.replace(day=1)

        # Find the first Monday in the same month
        first_monday = first_day
        while first_monday.weekday() != 0:
            first_monday += timedelta(days=1)

        # Ensure the Monday is in the same month
        if first_monday.month != date.month:
            first_monday += timedelta(days=7)

        # Calculate week number
        wom = ((current_week_start - first_monday).days // 7) + 1
        week_of_month.append(max(wom, 1))  # Clamp to minimum of 1

    return pd.Series(week_of_month, index=dates.index)
