"""
Logistic regression modeling for literacy outcomes.

This script fits logistic regression models using both statsmodels and 
scikit-learn, and outputs coefficient tables with odds ratios and 
performance metrics.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, confusion_matrix
import statsmodels.api as sm
from typing import Tuple, Dict


# Feature set for modeling
FEATURE_COLUMNS = [
    "enrollment_rate",
    "pupil_teacher_ratio",
    "teacher_qualification_rate",
    "household_poverty_rate",
    "mother_education_years",
    "household_size",
    "internet_access_rate",
    "textbook_availability_index",
    "travel_time_to_school_min",
    "electricity_access_rate"
]


def prepare_data(df: pd.DataFrame, test_size: float = 0.2) -> Tuple:
    """
    Prepare data for modeling: select features, split, and scale.
    
    Args:
        df: Input DataFrame
        test_size: Proportion of data for test set
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test, scaler, feature_names)
    """
    # Select features and target
    X = df[FEATURE_COLUMNS].copy()
    y = df["literacy_outcome"].copy()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Convert back to DataFrames for easier handling
    X_train_scaled = pd.DataFrame(
        X_train_scaled, columns=FEATURE_COLUMNS, index=X_train.index
    )
    X_test_scaled = pd.DataFrame(
        X_test_scaled, columns=FEATURE_COLUMNS, index=X_test.index
    )
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, FEATURE_COLUMNS


def fit_statsmodels_logit(X_train: pd.DataFrame, y_train: pd.Series) -> sm.Logit:
    """
    Fit logistic regression using statsmodels for detailed statistics.
    
    Args:
        X_train: Training features
        y_train: Training target
        
    Returns:
        Fitted statsmodels Logit model
    """
    # Add constant for intercept
    X_with_const = sm.add_constant(X_train)
    
    # Fit model
    model = sm.Logit(y_train, X_with_const)
    result = model.fit(disp=0)
    
    return result


def get_odds_ratios_table(model_result) -> pd.DataFrame:
    """
    Extract odds ratios and confidence intervals from statsmodels result.
    
    Args:
        model_result: Fitted statsmodels model result
        
    Returns:
        DataFrame with coefficients, odds ratios, and CIs
    """
    # Get coefficients and confidence intervals
    params = model_result.params
    conf_int = model_result.conf_int()
    pvalues = model_result.pvalues
    
    # Calculate odds ratios
    odds_ratios = np.exp(params)
    or_ci_lower = np.exp(conf_int[0])
    or_ci_upper = np.exp(conf_int[1])
    
    # Create table
    table = pd.DataFrame({
        "coefficient": params,
        "odds_ratio": odds_ratios,
        "or_ci_lower": or_ci_lower,
        "or_ci_upper": or_ci_upper,
        "p_value": pvalues
    })
    
    # Add significance stars
    table["significant"] = table["p_value"].apply(
        lambda p: "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
    )
    
    return table


def fit_sklearn_logistic(
    X_train: pd.DataFrame, 
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Tuple[LogisticRegression, Dict]:
    """
    Fit logistic regression using scikit-learn and evaluate performance.
    
    Args:
        X_train: Training features
        y_train: Training target
        X_test: Test features
        y_test: Test target
        
    Returns:
        Tuple of (fitted model, metrics dictionary)
    """
    # Fit model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    y_test_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    metrics = {
        "train_accuracy": accuracy_score(y_train, y_train_pred),
        "test_accuracy": accuracy_score(y_test, y_test_pred),
        "test_roc_auc": roc_auc_score(y_test, y_test_proba),
        "confusion_matrix": confusion_matrix(y_test, y_test_pred).tolist(),
        "classification_report": classification_report(y_test, y_test_pred, output_dict=True)
    }
    
    return model, metrics


def interpret_odds_ratio(feature: str, odds_ratio: float) -> str:
    """
    Generate plain-language interpretation of odds ratio.
    
    Args:
        feature: Feature name
        odds_ratio: Odds ratio value
        
    Returns:
        Plain-language interpretation
    """
    if odds_ratio > 1:
        pct_increase = (odds_ratio - 1) * 100
        return (f"Each unit increase in {feature} is associated with "
                f"{pct_increase:.1f}% higher odds of literacy")
    else:
        pct_decrease = (1 - odds_ratio) * 100
        return (f"Each unit increase in {feature} is associated with "
                f"{pct_decrease:.1f}% lower odds of literacy")


def run_analysis(data_path: str, output_dir: str) -> None:
    """
    Run complete modeling analysis pipeline.
    
    Args:
        data_path: Path to cleaned data file
        output_dir: Directory for output files
    """
    print("="*60)
    print("Logistic Regression Analysis")
    print("="*60)
    
    # Load data
    print(f"\nLoading data from {data_path}...")
    if data_path.endswith('.parquet'):
        df = pd.read_parquet(data_path)
    else:
        df = pd.read_csv(data_path)
    print(f"Loaded {len(df):,} rows")
    
    # Prepare data
    print("\nPreparing data...")
    X_train, X_test, y_train, y_test, scaler, features = prepare_data(df)
    print(f"Training set: {len(X_train):,} samples")
    print(f"Test set: {len(X_test):,} samples")
    
    # Fit statsmodels model
    print("\nFitting statsmodels Logit model...")
    sm_result = fit_statsmodels_logit(X_train, y_train)
    print("Model fitted successfully")
    
    # Get odds ratios table
    or_table = get_odds_ratios_table(sm_result)
    print("\nOdds Ratios (excluding intercept):")
    print(or_table.iloc[1:].to_string())  # Skip intercept
    
    # Fit sklearn model and evaluate
    print("\n\nFitting scikit-learn LogisticRegression...")
    sk_model, metrics = fit_sklearn_logistic(X_train, y_train, X_test, y_test)
    print("Model fitted successfully")
    
    print("\nPerformance Metrics:")
    print(f"  Training Accuracy: {metrics['train_accuracy']:.3f}")
    print(f"  Test Accuracy: {metrics['test_accuracy']:.3f}")
    print(f"  Test ROC-AUC: {metrics['test_roc_auc']:.3f}")
    
    print("\nConfusion Matrix (Test Set):")
    cm = metrics['confusion_matrix']
    print(f"  True Negatives:  {cm[0][0]}")
    print(f"  False Positives: {cm[0][1]}")
    print(f"  False Negatives: {cm[1][0]}")
    print(f"  True Positives:  {cm[1][1]}")
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save odds ratios table
    or_table_path = output_path / "odds_ratios_table.csv"
    or_table.to_csv(or_table_path)
    print(f"\nSaved odds ratios table to {or_table_path}")
    
    # Save metrics summary
    summary = {
        "model_type": "Logistic Regression",
        "features": features,
        "train_size": len(X_train),
        "test_size": len(X_test),
        "metrics": {
            "train_accuracy": float(metrics['train_accuracy']),
            "test_accuracy": float(metrics['test_accuracy']),
            "test_roc_auc": float(metrics['test_roc_auc'])
        },
        "confusion_matrix": metrics['confusion_matrix'],
        "key_findings": []
    }
    
    # Add key findings based on odds ratios
    for feature in features:
        if feature in or_table.index:
            or_val = or_table.loc[feature, "odds_ratio"]
            pval = or_table.loc[feature, "p_value"]
            if pval < 0.05:  # Only significant features
                summary["key_findings"].append({
                    "feature": feature,
                    "odds_ratio": float(or_val),
                    "interpretation": interpret_odds_ratio(feature, or_val)
                })
    
    metrics_path = output_path / "metrics_summary.json"
    with open(metrics_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Saved metrics summary to {metrics_path}")
    
    # Print key findings
    print("\n" + "="*60)
    print("Key Findings (Plain Language)")
    print("="*60)
    for finding in summary["key_findings"][:5]:  # Top 5
        print(f"\n• {finding['interpretation']}")
    
    print("\n" + "="*60)
    print("Analysis Complete!")
    print("="*60)
    print("\nNote: This analysis uses synthetic data for demonstration purposes.")
    print("Associations shown do not represent causal effects and should not be")
    print("used for real policy decisions without validation on actual data.")


def main():
    """
    Main entry point for modeling script.
    """
    # Default paths
    data_path = "data/processed/education_outcomes_cleaned.parquet"
    output_dir = "reports"
    
    # Check if data exists
    if not Path(data_path).exists():
        # Try CSV version
        data_path = "data/processed/education_outcomes_cleaned.csv"
        if not Path(data_path).exists():
            print(f"Error: Could not find cleaned data file.")
            print("Please run data cleaning first:")
            print("  python -m src.data.cleaning --in data/raw/education_outcomes_individual.csv --out data/processed")
            return
    
    run_analysis(data_path, output_dir)


if __name__ == "__main__":
    main()
