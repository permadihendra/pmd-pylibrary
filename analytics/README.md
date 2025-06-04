# 📊 DataExplorerChain

Effortless, memory-optimized data exploration in Python using **Polars**, inspired by Rust's ownership principles.
Designed for analysts and developers who want **clean syntax**, **low RAM usage**, and **chainable** methods like pandas but smarter.

## 🚀 Features

- 🔍 Simple `.load().explore()` workflow
- 📊 Pivot tables with `.pivot()` and `.pivot_format()` (supports subtotals and formatting)
- 🧠 Auto memory cleanup when no longer needed
- 🔗 Chainable methods: `.select_columns()`, `.to_pandas()`, `.get()`
- ⚡ Powered by **Polars** for speed and low memory footprint
- 🧼 Optional `.drop_unused()` to keep only what's needed
- 🧾 Supports `.csv`, `.parquet`, and `.xlsx` with sheet name and skip rows

## 📦 Installation

### 🐍 Using `pip`:

```bash
pip install polars pandas pyarrow
```

Or from this repo:

```bash
git clone git@github.com:permadihendra/my-pymodules.git
cd my-pymodules/data-explorer-chain
pip install -e .
```

## 🧪 Using conda (recommended for isolated environments):

```bash
conda create -n new-env python=3.10 -y
conda activate new-env

conda install -c conda-forge polars pandas pyarrow openpyxl
```

⚠️ openpyxl is needed for Excel support in Polars

## 🛠️ Example Usage

```python
from data_explorer import DataExplorerChain

df = (
    DataExplorerChain("data.xlsx", sheet_name="Sales", skip_rows=2)
    .load()
    .explore()
    .pivot(index="Region", columns="Month", values="Revenue", aggregate_function="sum")
    .pivot_format(format="currency", decimals=0, grand_total=True)
    .select_columns(["Region", "Jan", "Feb", "Total"])
    .to_pandas()
)
```

## 💡 Why Use This?

- Built with performance in mind (no memory bloat)
- Safer data handling inspired by Rust `(__enter__, __del__)`
- Clean interface for exploration without keeping unnecessary variables
- Perfect for Jupyter or production ETL steps

## 🧪 Coming Soon

- Excel export with styles
- Semantic profiling reports
- Smart filters (.filter_contains(), .filter_top_n())
