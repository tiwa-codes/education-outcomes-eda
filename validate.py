#!/usr/bin/env python
"""
Validation script to test the entire education outcomes EDA workflow.

Run this after setup to ensure everything is working correctly.
"""

import sys
from pathlib import Path


def test_imports():
    """Test that all required packages are installed."""
    print("Testing imports...")
    try:
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import plotly
        import streamlit
        import sklearn
        import statsmodels
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("  Run: pip install -r requirements.txt")
        return False


def test_data_generation():
    """Test data generation."""
    print("\nTesting data generation...")
    try:
        from src.data.generate_synthetic_data import generate_group_features
        df = generate_group_features()
        assert len(df) == 148, f"Expected 148 groups, got {len(df)}"
        print(f"✓ Data generation works (generated {len(df)} groups)")
        return True
    except Exception as e:
        print(f"✗ Data generation failed: {e}")
        return False


def test_data_files():
    """Test that data files exist."""
    print("\nTesting data files...")
    required_files = [
        "data/raw/education_outcomes_individual.csv",
        "data/processed/education_outcomes_state_summary.csv"
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size / 1024  # KB
            print(f"✓ {file_path} exists ({size:.1f} KB)")
        else:
            print(f"✗ {file_path} not found")
            all_exist = False
    
    if not all_exist:
        print("  Run: python -m src.data.generate_synthetic_data")
    
    return all_exist


def test_data_cleaning():
    """Test data cleaning."""
    print("\nTesting data cleaning...")
    try:
        import pandas as pd
        raw_path = Path("data/raw/education_outcomes_individual.csv")
        
        if not raw_path.exists():
            print("✗ Raw data not found. Run data generation first.")
            return False
        
        df = pd.read_csv(raw_path)
        print(f"✓ Can load raw data ({len(df):,} rows)")
        
        # Check for cleaned data
        cleaned_path = Path("data/processed/education_outcomes_cleaned.parquet")
        if cleaned_path.exists():
            df_clean = pd.read_parquet(cleaned_path)
            print(f"✓ Cleaned data exists ({len(df_clean):,} rows, {len(df_clean.columns)} columns)")
        else:
            print("⚠ Cleaned data not found")
            print("  Run: python -m src.data.cleaning --in data/raw/education_outcomes_individual.csv --out data/processed")
        
        return True
    except Exception as e:
        print(f"✗ Data cleaning test failed: {e}")
        return False


def test_modeling():
    """Test modeling."""
    print("\nTesting modeling...")
    try:
        metrics_path = Path("reports/metrics_summary.json")
        
        if metrics_path.exists():
            import json
            with open(metrics_path) as f:
                metrics = json.load(f)
            print(f"✓ Model metrics found (Test accuracy: {metrics['metrics']['test_accuracy']:.3f})")
        else:
            print("⚠ Model metrics not found")
            print("  Run: python -m src.modeling.logistic_regression")
        
        return True
    except Exception as e:
        print(f"✗ Modeling test failed: {e}")
        return False


def test_visualization():
    """Test visualization module."""
    print("\nTesting visualization...")
    try:
        from src.viz.plots import plot_correlation_heatmap
        print("✓ Visualization module imports successfully")
        return True
    except Exception as e:
        print(f"✗ Visualization test failed: {e}")
        return False


def test_dashboard():
    """Test dashboard."""
    print("\nTesting dashboard...")
    try:
        dashboard_path = Path("dashboards/app.py")
        if dashboard_path.exists():
            print("✓ Dashboard file exists")
            print("  To run: streamlit run dashboards/app.py")
        else:
            print("✗ Dashboard file not found")
            return False
        return True
    except Exception as e:
        print(f"✗ Dashboard test failed: {e}")
        return False


def test_documentation():
    """Test documentation files."""
    print("\nTesting documentation...")
    doc_files = [
        "README.md",
        "docs/data_dictionary.md",
        "reports/education_outcomes_brief.md",
        "notebooks/01_education_outcomes_eda.ipynb"
    ]
    
    all_exist = True
    for file_path in doc_files:
        if Path(file_path).exists():
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} not found")
            all_exist = False
    
    return all_exist


def main():
    """Run all validation tests."""
    print("="*60)
    print("Education Outcomes EDA - Validation Script")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Data Generation", test_data_generation),
        ("Data Files", test_data_files),
        ("Data Cleaning", test_data_cleaning),
        ("Modeling", test_modeling),
        ("Visualization", test_visualization),
        ("Dashboard", test_dashboard),
        ("Documentation", test_documentation)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("Validation Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! The project is ready to use.")
        print("\nNext steps:")
        print("  1. Run: jupyter lab")
        print("  2. Open: notebooks/01_education_outcomes_eda.ipynb")
        print("  3. Run: streamlit run dashboards/app.py")
        return 0
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
