import pandas as pd
from pathlib import Path

from sqlalchemy import text

from connection import engine


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Excel file
EXCEL_FILE = PROJECT_ROOT / "companies list.xlsx"


def load_excel():
    """Read company master data from Excel."""
    df = pd.read_excel(EXCEL_FILE)

    # Standardize column names
    df.columns = df.columns.str.strip()

    return df


def clean_data(df):
    """Clean and validate company data."""

    # Remove completely empty rows
    df = df.dropna(how="all").copy()

    # Remove leading/trailing spaces from text columns
    text_columns = [
        "Category",
        "Company/App Name",
        "Headquarters",
        "Website",
        "Industry Type"
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()

    # Convert founded year to numeric
    if "Founded Year" in df.columns:
        df["Founded Year"] = pd.to_numeric(
            df["Founded Year"],
            errors="coerce"
        )

    # Check duplicate company names
    duplicates = df[
        df["Company/App Name"].duplicated(keep=False)
    ]

    if not duplicates.empty:
        print("\nWarning: Duplicate company names found:")
        print(duplicates["Company/App Name"].tolist())

    # Check missing company names
    missing_names = df["Company/App Name"].isna().sum()

    if missing_names > 0:
        print(f"\nWarning: {missing_names} rows have no company name.")

    return df


def get_industries():
    """Fetch industries from PostgreSQL."""

    query = text("""
        SELECT industry_id, industry_name
        FROM industries
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return {
            row.industry_name: row.industry_id
            for row in result
        }


def load_brands(df):
    """Insert companies into PostgreSQL."""

    industries = get_industries()

    print("\nIndustries found in database:")
    for industry, industry_id in industries.items():
        print(f"{industry_id}: {industry}")

    with engine.begin() as connection:

        for _, row in df.iterrows():

            industry_name = row["Category"]

            if industry_name not in industries:
                print(
                    f"Skipping {row['Company/App Name']} - "
                    f"industry not found: {industry_name}"
                )
                continue

            query = text("""
                INSERT INTO brands (
                    brand_name,
                    industry_id,
                    founded_year,
                    headquarters,
                    website,
                    industry_type
                )
                VALUES (
                    :brand_name,
                    :industry_id,
                    :founded_year,
                    :headquarters,
                    :website,
                    :industry_type
                )
                ON CONFLICT (brand_name) DO NOTHING;
            """)

            connection.execute(
                query,
                {
                    "brand_name": row["Company/App Name"],
                    "industry_id": industries[industry_name],
                    "founded_year": (
                        int(row["Founded Year"])
                        if pd.notna(row["Founded Year"])
                        else None
                    ),
                    "headquarters": (
                        row["Headquarters"]
                        if pd.notna(row["Headquarters"])
                        else None
                    ),
                    "website": (
                        row["Website"]
                        if pd.notna(row["Website"])
                        else None
                    ),
                    "industry_type": (
                        row["Industry Type"]
                        if pd.notna(row["Industry Type"])
                        else None
                    ),
                }
            )

    print("\nBrands loaded successfully!")


def main():

    print("===================================")
    print("BehaviorLens - Brand Data Loader")
    print("===================================")

    # 1. Read Excel
    df = load_excel()

    print(f"\nRows loaded from Excel: {len(df)}")

    # 2. Clean and validate
    df = clean_data(df)

    print(f"Rows after cleaning: {len(df)}")

    # 3. Load into PostgreSQL
    load_brands(df)


if __name__ == "__main__":
    main()