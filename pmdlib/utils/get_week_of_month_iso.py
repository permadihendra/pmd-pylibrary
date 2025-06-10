import pandas as pd


def get_week_of_month_iso(dates: pd.Series) -> pd.Series:
    """
    Return ISO-based week of the month for a datetime Series.

    Week 1 is based on the ISO calendar (starting on Monday).
    usage : df['week_of_month'] = get_week_of_month_iso(df['datetime_column']).
    """
    dates = pd.to_datetime(dates)
    result = []

    for date in dates:
        # First day of month
        first_day = date.replace(day=1)
        # ISO week of the first day of the month
        first_iso_week = first_day.isocalendar()[1]
        current_iso_week = date.isocalendar()[1]

        # Handle January case where first week can be 52 or 53
        if first_iso_week > current_iso_week:
            week_of_month = current_iso_week
        else:
            week_of_month = current_iso_week - first_iso_week + 1

        result.append(week_of_month)

    return pd.Series(result, index=dates.index)
