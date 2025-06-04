import gc
from pathlib import Path

import polars as pl


class DataExplorerChain:
    """
    A fluent, chainable interface for loading, exploring, transforming,
    and pivoting datasets using Polars (Rust-based DataFrame), with support for CSV, Excel, Parquet.

    Excel files are loaded via Polars if available, or fallback to Pandas with support for
    `sheet_name` and `skip_rows`.
    """

    def __init__(
        self,
        filepath: str,
        columns: list[str] = None,
        sheet_name=0,
        skip_rows: int = 0,
    ):
        """
        Args:
            filepath (str): Path to the input file (.csv, .xlsx, .parquet)
            columns (list[str], optional): Columns to select
            sheet_name (str or int, optional): Sheet name/index for Excel
            skip_rows (int) : Skip row when excel reading
        """
        self.filepath = Path(filepath)
        self.columns = columns
        self.sheet_name = sheet_name
        # 👇 Translate user-friendly skip_rows into proper Polars read_options
        self.read_options = {"header_row": skip_rows} if skip_rows else {}
        self.df = None

    def load(self):
        """Load dataset based on file extension."""
        ext = self.filepath.suffix.lower()

        if ext == ".csv":
            self.df = pl.read_csv(self.filepath)

        elif ext in [".xls", ".xlsx"]:
            try:
                # Try native Polars Excel read
                print("🔍 df loaded with polars \n")
                self.df = pl.read_excel(
                    source=self.filepath,
                    sheet_name=self.sheet_name,
                    read_options=self.read_options,
                )

            except TypeError:
                # Fallback to Pandas for broader compatibility
                import pandas as pd

                header_row = self.read_options.get("header_row", 0)
                df_pd = pd.read_excel(
                    self.filepath,
                    sheet_name=self.sheet_name,
                    skiprows=header_row,
                    engine="calamine",
                    dtype_backend="pyarrow",
                )
                self.df = pl.from_pandas(df_pd)
                print("🔍 df loaded with pandas \n")

        elif ext == ".parquet":
            self.df = pl.read_parquet(self.filepath)

        else:
            raise ValueError(f"Unsupported file format: {ext}")

        if self.columns:
            self.df = self.df.select(self.columns)

        return self

    def explore(self):
        """Print DataFrame summary and first few rows."""
        if self.df is not None:
            print("⚙️ Column Info:")
            for col in self.df.schema:
                print(f"• {col:25} → {self.df.schema[col]}")
            print("\n📊 Head Preview:")
            print(self.df.head(5))
        return self

    def select_columns(self, columns: list[str]):
        """
        Select a subset of columns from the DataFrame.

        Args:
            columns (list[str]): List of column names to keep. e.g .select_columns(["Region", "Year"]).
        """
        self.df = self.df.select(columns)
        return self

    def pivot(self, index, columns, values, aggregate_function="sum"):
        """Create a pivot table."""
        self.df = self.df.pivot(
            values=values,
            index=index,
            on=columns,
            aggregate_function=aggregate_function,
        )
        return self

    def pivot_format(
        self,
        format: str = "currency",
        decimals: int = 0,
        grand_total: bool = True,
        fill_null=0,
    ):
        """
        Format the pivoted DataFrame like an Excel pivot table.

        Adds grand totals for both rows and columns, fills nulls,
        and formats numeric values (e.g. currency).

        Args:
            format (str): 'currency' to format numeric values.
            decimals (int): Number of decimal places.
            grand_total (bool): Add Total row and column.
            fill_null (Any): Value to replace nulls before formatting.
        """
        if self.df is None:
            raise RuntimeError("Call .pivot() before .pivot_format()")

        group_col = self.df.columns[0]  # the index (e.g., SOURCE_DATA)

        # Fill nulls first
        if fill_null is not None:
            self.df = self.df.fill_null(fill_null)

        if grand_total:
            numeric_cols = [col for col in self.df.columns if col != group_col]

            # ✅ Add total column (row-wise)
            self.df = self.df.with_columns(
                pl.sum_horizontal(numeric_cols).alias("Grand Total")
            )

            # ✅ Add total row (column-wise)
            total_row = self.df.select(
                [
                    pl.lit("Grand Total").alias(group_col),
                    *[
                        pl.sum(col).alias(col)
                        for col in self.df.columns
                        if col != group_col
                    ],
                ]
            )
            self.df = self.df.vstack(total_row)

        # Apply currency formatting
        if format == "currency":
            fmt = f"{{:,.{decimals}f}}"
            for col, dtype in self.df.schema.items():
                if dtype in (pl.Int64, pl.Float64):
                    self.df = self.df.with_columns(
                        [
                            pl.col(col)
                            .map_elements(
                                lambda x: fmt.format(x), return_dtype=pl.String
                            )
                            .alias(col)
                        ]
                    )

        return self

    def filter(self, expr: pl.Expr):
        """Filter DataFrame with Polars expression."""
        self.df = self.df.filter(expr)
        return self

    def get(self) -> pl.DataFrame:
        """Return the Polars DataFrame."""
        return self.df

    def to_pandas(self):
        """Convert current Polars DataFrame to Pandas."""
        if self.df is not None:
            return self.df.to_pandas()
        return None

    def __del__(self):
        del self.df
        gc.collect()
