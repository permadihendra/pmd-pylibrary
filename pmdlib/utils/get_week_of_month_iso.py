import pandas as pd


def get_week_of_month_iso(dates: pd.Series) -> pd.Series:
    """
    Return ISO-based week of the month for a datetime Series.

    Week 1 is based on the ISO calendar (starting on Monday).
    usage : df['week_of_month'] = get_week_of_month_iso(df['datetime_column']).
    """
    # Ensure datetime format
    dates = pd.to_datetime(dates)

    # Extract year and month
    year_month = dates.dt.to_period("M")

    # Create a DataFrame to hold results
    temp_df = pd.DataFrame({"date": dates})
    temp_df["year_month"] = year_month
    temp_df["iso_week"] = temp_df["date"].dt.isocalendar().week

    # Get the first ISO week for each month from the actual dates
    first_weeks = temp_df.groupby("year_month")["iso_week"].transform("min")

    # Week of month = ISO week - first ISO week of *that month* + 1
    temp_df["week_of_month"] = temp_df["iso_week"] - first_weeks + 1

    return temp_df["week_of_month"]
