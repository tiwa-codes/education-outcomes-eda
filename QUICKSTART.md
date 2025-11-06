# Quick Start Guide

This guide will get you up and running with the Education Outcomes EDA project in 5 minutes.

## Step 1: Setup (2 minutes)

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd education-outcomes-eda

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Linux/Mac
# OR
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Validate Installation (30 seconds)

```bash
python validate.py
```

You should see all tests pass with a "🎉 All tests passed!" message.

## Step 3: Generate and Explore Data (2 minutes)

```bash
# Generate synthetic data (~88,800 records)
python -m src.data.generate_synthetic_data

# Clean and process data
python -m src.data.cleaning --in data/raw/education_outcomes_individual.csv --out data/processed

# Run modeling and generate insights
python -m src.modeling.logistic_regression
```

## Step 4: Explore Results

### Option A: Interactive Dashboard (Recommended)

```bash
streamlit run dashboards/app.py
```

This opens an interactive dashboard in your browser where you can:
- Filter by state, sex, and location
- View key metrics (literacy, enrollment, poverty rates)
- Explore interactive charts
- Download filtered data

### Option B: Jupyter Notebook

```bash
jupyter lab
```

Then open `notebooks/01_education_outcomes_eda.ipynb` and run all cells to see:
- Detailed exploratory data analysis
- Correlation analysis
- State rankings
- Statistical modeling with interpretations
- Generated figures

### Option C: Read the Policy Brief

Open `reports/education_outcomes_brief.md` for a 2-page non-technical summary of findings and recommendations.

## What You'll Find

### Data
- **88,800 individual records** across Nigeria's 36 states + FCT Abuja
- **10 feature variables**: enrollment rates, teacher quality, poverty, infrastructure
- **Binary outcome**: literacy (0 = not literate, 1 = literate)

### Key Insights
- Urban-rural literacy gap
- Impact of teacher quality and class size
- Association between poverty and outcomes
- Mother's education spillover effects
- Infrastructure disparities

### Outputs
- **Figures**: `reports/figures/*.png`
- **Model results**: `reports/metrics_summary.json`
- **Odds ratios**: `reports/odds_ratios_table.csv`
- **Data dictionary**: `docs/data_dictionary.md`

## Common Issues

### Import Errors
```bash
# Make sure you activated the virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Reinstall dependencies if needed
pip install -r requirements.txt
```

### Data Not Found
```bash
# Run data generation first
python -m src.data.generate_synthetic_data
```

### Dashboard Won't Start
```bash
# Check if Streamlit is installed
pip install streamlit

# Try specifying port explicitly
streamlit run dashboards/app.py --server.port 8501
```

## Next Steps

1. **Explore the Dashboard**: Filter by different states and locations to see patterns
2. **Read the Notebook**: Detailed analysis with code and interpretations
3. **Review the Policy Brief**: Non-technical summary for stakeholders
4. **Customize**: Modify data generation parameters or add new features

## File Structure Reference

```
├── data/                    # Generated data (CSV and Parquet)
├── notebooks/               # Jupyter analysis notebook
├── src/                     # Python modules
│   ├── data/               # Data generation and cleaning
│   ├── modeling/           # Statistical models
│   └── viz/                # Visualization functions
├── dashboards/             # Streamlit app
├── reports/                # Outputs (figures, metrics, brief)
└── docs/                   # Documentation
```

## Important Notes

⚠️ **Synthetic Data**: All data is computer-generated for demonstration purposes. Do not use for real policy decisions.

✅ **Reproducible**: Fixed random seed ensures consistent results across runs.

📚 **Educational**: Designed for learning data science workflows and best practices.

## Help and Support

- **Full Documentation**: See `README.md`
- **Data Variables**: See `docs/data_dictionary.md`
- **Policy Brief**: See `reports/education_outcomes_brief.md`
- **Issues**: Open an issue in the repository

---

**Estimated Time**: 5 minutes from clone to interactive dashboard  
**Difficulty**: Beginner-friendly  
**Requirements**: Python 3.11+, pip, basic terminal knowledge
