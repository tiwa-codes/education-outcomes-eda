"""
Data cleaning and validation for education outcomes data.

This script loads raw data, performs validation, standardizes formats,
and creates derived features for analysis.
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to snake_case.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with standardized column names
    """
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate data and handle issues.
    
    Checks:
    - Duplicates
    - Missing values
    - Impossible values (e.g., rates > 100, negative values)
    
    Args:
        df: Input DataFrame
        
    Returns:
        Validated DataFrame
    """
    print(f"Initial rows: {len(df):,}")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"Removing {duplicates} duplicate rows...")
        df = df.drop_duplicates()
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print("\nMissing values per column:")
        print(missing[missing > 0])
        print("Dropping rows with missing values...")
        df = df.dropna()
    
    # Validate percentage fields (0-100)
    percentage_cols = [
        "enrollment_rate", "teacher_qualification_rate",
        "household_poverty_rate", "internet_access_rate",
        "electricity_access_rate"
    ]
    
    for col in percentage_cols:
        if col in df.columns:
            invalid = ((df[col] < 0) | (df[col] > 100)).sum()
            if invalid > 0:
                print(f"Clipping {invalid} invalid values in {col}")
                df[col] = df[col].clip(0, 100)
    
    # Validate textbook_availability_index (0-1)
    if "textbook_availability_index" in df.columns:
        invalid = ((df["textbook_availability_index"] < 0) | 
                   (df["textbook_availability_index"] > 1)).sum()
        if invalid > 0:
            print(f"Clipping {invalid} invalid values in textbook_availability_index")
            df["textbook_availability_index"] = df["textbook_availability_index"].clip(0, 1)
    
    # Validate literacy_outcome (0 or 1)
    if "literacy_outcome" in df.columns:
        invalid = (~df["literacy_outcome"].isin([0, 1])).sum()
        if invalid > 0:
            print(f"Warning: {invalid} invalid literacy_outcome values")
            df = df[df["literacy_outcome"].isin([0, 1])]
    
    # Validate non-negative fields
    nonneg_cols = [
        "pupil_teacher_ratio", "mother_education_years",
        "household_size", "travel_time_to_school_min"
    ]
    
    for col in nonneg_cols:
        if col in df.columns:
            invalid = (df[col] < 0).sum()
            if invalid > 0:
                print(f"Clipping {invalid} negative values in {col}")
                df[col] = df[col].clip(0, None)
    
    print(f"Final rows after validation: {len(df):,}")
    return df


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived features for analysis.
    
    Features added:
    - Z-scores for key continuous features
    - Bins for continuous features
    - Literacy rate by group (if individual data)
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with derived features
    """
    # Create z-scores for key features
    z_score_cols = [
        "enrollment_rate", "pupil_teacher_ratio",
        "teacher_qualification_rate", "household_poverty_rate"
    ]
    
    for col in z_score_cols:
        if col in df.columns:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                df[f"{col}_zscore"] = (df[col] - mean) / std
    
    # Create bins for poverty rate
    if "household_poverty_rate" in df.columns:
        df["poverty_category"] = pd.cut(
            df["household_poverty_rate"],
            bins=[0, 20, 40, 60, 100],
            labels=["Low", "Medium", "High", "Very High"]
        )
    
    # Create bins for mother education
    if "mother_education_years" in df.columns:
        df["mother_education_category"] = pd.cut(
            df["mother_education_years"],
            bins=[-1, 0, 6, 12, 16],
            labels=["None", "Primary", "Secondary", "Tertiary"]
        )
    
    # Create bins for enrollment rate
    if "enrollment_rate" in df.columns:
        df["enrollment_category"] = pd.cut(
            df["enrollment_rate"],
            bins=[0, 70, 85, 95, 100],
            labels=["Low", "Medium", "High", "Very High"]
        )
    
    return df


def enforce_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enforce proper data types for columns.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with enforced data types
    """
    # Categorical columns
    categorical_cols = ["state", "sex", "location"]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")
    
    # Binary outcome
    if "literacy_outcome" in df.columns:
        df["literacy_outcome"] = df["literacy_outcome"].astype(int)
    
    # Float columns (rates and continuous features)
    float_cols = [
        "enrollment_rate", "pupil_teacher_ratio",
        "teacher_qualification_rate", "household_poverty_rate",
        "mother_education_years", "household_size",
        "internet_access_rate", "textbook_availability_index",
        "travel_time_to_school_min", "electricity_access_rate"
    ]
    
    for col in float_cols:
        if col in df.columns:
            df[col] = df[col].astype(float)
    
    return df


def clean_and_save(raw_path: str, out_dir: str) -> None:
    """
    Main cleaning pipeline: load, validate, transform, and save.
    
    Args:
        raw_path: Path to raw CSV file
        out_dir: Output directory for cleaned data
    """
    print("="*60)
    print("Data Cleaning Pipeline")
    print("="*60)
    
    # Load data
    print(f"\nLoading data from {raw_path}...")
    df = pd.read_csv(raw_path)
    print(f"Loaded {len(df):,} rows, {len(df.columns)} columns")
    
    # Standardize column names
    print("\nStandardizing column names...")
    df = standardize_column_names(df)
    
    # Enforce data types
    print("\nEnforcing data types...")
    df = enforce_dtypes(df)
    
    # Validate data
    print("\nValidating data...")
    df = validate_data(df)
    
    # Add derived features
    print("\nAdding derived features...")
    df = add_derived_features(df)
    
    # Save cleaned data
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Save as both CSV and Parquet
    csv_path = out_path / "education_outcomes_cleaned.csv"
    parquet_path = out_path / "education_outcomes_cleaned.parquet"
    
    print(f"\nSaving cleaned data...")
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV to {csv_path}")
    
    df.to_parquet(parquet_path, index=False)
    print(f"Saved Parquet to {parquet_path}")
    
    # Print summary statistics
    print("\n" + "="*60)
    print("Cleaning Complete!")
    print("="*60)
    print(f"Final dataset: {len(df):,} rows, {len(df.columns)} columns")
    
    if "literacy_outcome" in df.columns:
        print(f"\nLiteracy rate: {df['literacy_outcome'].mean()*100:.1f}%")
        
        if "location" in df.columns:
            print("\nBy location:")
            for loc in df["location"].cat.categories:
                rate = df[df["location"]==loc]["literacy_outcome"].mean()
                print(f"  {loc.capitalize()}: {rate*100:.1f}%")
        
        if "sex" in df.columns:
            print("\nBy sex:")
            for s in df["sex"].cat.categories:
                rate = df[df["sex"]==s]["literacy_outcome"].mean()
                print(f"  {s}: {rate*100:.1f}%")


def main():
    """
    Command-line interface for data cleaning.
    """
    parser = argparse.ArgumentParser(
        description="Clean and validate education outcomes data"
    )
    parser.add_argument(
        "--in",
        dest="input_path",
        type=str,
        required=True,
        help="Path to raw CSV file"
    )
    parser.add_argument(
        "--out",
        dest="output_dir",
        type=str,
        required=True,
        help="Output directory for cleaned data"
    )
    
    args = parser.parse_args()
    
    clean_and_save(args.input_path, args.output_dir)


if __name__ == "__main__":
    main()
