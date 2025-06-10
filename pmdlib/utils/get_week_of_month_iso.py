import pandas as pd


def get_week_of_month_iso(dates: pd.Series) -> pd.Series:
    """
    Return ISO-based week of the month for a datetime Series.

    Week 1 is based on the ISO calendar (starting on Monday).
    usage : df['week_of_month'] = get_week_of_month_iso(df['datetime_column']).
    """
    # Ensure datetime format
    dates = pd.to_datetime(dates)

    # Calculate ISO week
    iso_week = dates.dt.isocalendar().week

    # First ISO week of each month
    first_week = dates.dt.to_period("M").apply(
        lambda x: pd.Timestamp(x.start_time).isocalendar().week
    )

    return iso_week - first_week + 1
