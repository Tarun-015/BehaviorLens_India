import pandas as pd
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Excel file
EXCEL_FILE = PROJECT_ROOT / "companies list.xlsx"


def load_excel():
    """Read and inspect the company master Excel file."""

    print(f"Reading file: {EXCEL_FILE}")

    df = pd.read_excel(EXCEL_FILE)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nShape:")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))

    return df


if __name__ == "__main__":
    load_excel()