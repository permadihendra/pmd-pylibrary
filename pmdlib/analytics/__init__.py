# Dependencies Check
#
try:
    import polars as pl
except ImportError:
    raise ImportError(
        "⚠️ Missing dependency: `polars` is required.\n"
        "💡 Install it with `pip install polars` or `conda install polars`"
    )

try:
    import pandas as pd
except ImportError:
    raise ImportError(
        "⚠️ Missing dependency: `pandas` is required.\n"
        "💡 Install it with `pip install pandas` or `conda install pandas`"
    )

from .data_explorer_chain import DataExplorerChain
