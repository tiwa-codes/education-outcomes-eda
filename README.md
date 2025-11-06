# Education Outcomes EDA: Nigeria Literacy Analysis

A complete, reproducible data analysis project examining factors associated with basic literacy outcomes across Nigerian states. This project demonstrates end-to-end data science workflows including synthetic data generation, exploratory data analysis, statistical modeling, and interactive visualization.

## 🎯 Project Objective

Analyze factors associated with basic literacy outcomes across Nigeria's 36 states plus FCT Abuja, and present insights through:

- A reproducible Jupyter notebook for data cleaning, EDA, and modeling
- An interactive Streamlit dashboard with state/sex/location filters
- A 2-page policy brief for non-technical audiences
- Complete documentation and clear run instructions

**⚠️ Important:** This project uses **synthetic (computer-generated) data** for demonstration and educational purposes. Results should not be used for real policy decisions.

## 📁 Project Structure

```
education-outcomes-eda/
├── data/
│   ├── raw/                          # Generated raw CSV files
│   └── processed/                     # Cleaned and processed data
├── notebooks/
│   └── 01_education_outcomes_eda.ipynb  # Main analysis notebook
├── src/
│   ├── data/
│   │   ├── generate_synthetic_data.py   # Data generation script
│   │   └── cleaning.py                   # Data cleaning pipeline
│   ├── modeling/
│   │   └── logistic_regression.py        # Modeling script
│   └── viz/
│       └── plots.py                      # Visualization functions
├── dashboards/
│   └── app.py                            # Streamlit dashboard
├── docs/
│   └── data_dictionary.md                # Data documentation
├── reports/
│   ├── figures/                          # Generated plots and charts
│   ├── education_outcomes_brief.md       # Policy brief
│   └── metrics_summary.json              # Model results
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Quickstart

### Prerequisites

- Python 3.11 or higher
- `pip` package manager
- Virtual environment tool (recommended)

### Setup

1. **Clone the repository** (if not already cloned):
   ```bash
   git clone <repository-url>
   cd education-outcomes-eda
   ```

2. **Create and activate virtual environment**:
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate on Linux/Mac
   source .venv/bin/activate
   
   # Activate on Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

#### Step 1: Generate Synthetic Data

```bash
python -m src.data.generate_synthetic_data
```

This creates:
- `data/raw/education_outcomes_individual.csv` (~88,800 individual records)
- `data/processed/education_outcomes_state_summary.csv` (aggregated summaries)

**Output:** You should see summary statistics printed, including overall literacy rates and top/bottom performing states.

#### Step 2: Clean and Process Data

```bash
python -m src.data.cleaning --in data/raw/education_outcomes_individual.csv --out data/processed
```

This creates:
- `data/processed/education_outcomes_cleaned.csv`
- `data/processed/education_outcomes_cleaned.parquet`

Adds derived features like z-scores and categorical bins.

#### Step 3: Run Jupyter Notebook

```bash
jupyter lab
```

Then open and run `notebooks/01_education_outcomes_eda.ipynb`. This notebook:
- Loads and explores the data
- Creates visualizations (correlation heatmaps, state rankings, etc.)
- Fits logistic regression models
- Interprets results in plain language
- Saves figures to `reports/figures/`

#### Step 4: Launch Interactive Dashboard

```bash
streamlit run dashboards/app.py
```

The dashboard will open in your browser at `http://localhost:8501`. Features:
- Filter by states, sex, and location
- View KPIs and trends
- Interactive charts with Plotly
- Download filtered data

## 📊 Key Features

### Synthetic Data Generation

Generates realistic education data with:
- **37 states** (Nigeria's 36 states + FCT Abuja)
- **Sex categories**: Male (M), Female (F)
- **Location types**: Urban, Rural
- **~600 individuals per group** = ~88,800 total records

**Features included:**
- Enrollment rate, pupil-teacher ratio, teacher qualification rate
- Household poverty rate, mother education years, household size
- Internet access, electricity access, textbook availability
- Travel time to school

**Target variable:** Binary literacy outcome (0 = not literate, 1 = literate)

### Data Cleaning

Automated pipeline that:
- Validates data quality (duplicates, missing values, impossible values)
- Standardizes column names and data types
- Creates derived features (z-scores, categorical bins)
- Outputs cleaned CSV and Parquet files

### Exploratory Data Analysis

Comprehensive EDA including:
- Summary statistics by state, sex, and location
- Distribution plots for key features
- Correlation analysis
- State rankings (top/bottom performers)
- Disparity analysis (urban/rural, male/female)

### Statistical Modeling

Logistic regression models using both:
- **statsmodels**: Detailed statistics, odds ratios with 95% CIs
- **scikit-learn**: Performance metrics, predictions

Optional Random Forest model for comparison and feature importance.

### Interactive Dashboard

Streamlit app with:
- Multi-select state filters
- Sex and location filters
- KPI cards (literacy, enrollment, teacher quality, poverty)
- Interactive Plotly visualizations
- Data download functionality

### Policy Brief

2-page brief (`reports/education_outcomes_brief.md`) with:
- Executive summary for non-technical audiences
- Plain-language interpretation of findings
- Actionable recommendations
- Equity insights
- Limitations and next steps

## 📈 Understanding the Results

### Key Findings (Typical Patterns)

The synthetic data is designed to show realistic associations:

**Positive associations with literacy:**
- Higher enrollment rates
- Better teacher qualifications
- More mother education
- Better internet/electricity access
- Greater textbook availability

**Negative associations with literacy:**
- Higher poverty rates
- Higher pupil-teacher ratios (overcrowding)
- Longer travel times to school
- Larger household sizes

**Disparities:**
- Urban areas typically have higher literacy rates than rural areas
- Variations exist across states
- Sex disparities may be present

### Model Interpretation

The logistic regression outputs **odds ratios**:
- OR > 1: Feature associated with higher literacy odds
- OR < 1: Feature associated with lower literacy odds
- OR = 1: No association

Example: OR = 1.05 for enrollment means each 1-point increase in enrollment rate is associated with 5% higher odds of literacy.

## 📚 Documentation

- **Data Dictionary**: `docs/data_dictionary.md` - Complete variable documentation
- **Policy Brief**: `reports/education_outcomes_brief.md` - Non-technical summary
- **Jupyter Notebook**: `notebooks/01_education_outcomes_eda.ipynb` - Full analysis with commentary
- **Code Documentation**: Docstrings in all Python modules

## 🔧 Advanced Usage

### Running Individual Components

**Modeling only:**
```bash
python -m src.modeling.logistic_regression
```

**Generate specific visualizations:**
```python
from src.viz.plots import plot_correlation_heatmap, plot_state_bars
import pandas as pd

df = pd.read_csv('data/processed/education_outcomes_cleaned.csv')
plot_correlation_heatmap(df, output_path='my_heatmap.png')
plot_state_bars(df, metric='literacy_rate', output_path='my_rankings.png')
```

### Customizing Data Generation

Edit parameters in `src/data/generate_synthetic_data.py`:
- `RANDOM_SEED`: Change for different data patterns
- `N_INDIVIDUALS_PER_GROUP`: Adjust sample size
- Feature ranges and coefficients in generation functions

## 🧪 Testing and Validation

### Quick Validation

After setup, run this sequence to validate everything works:

```bash
# Generate data
python -m src.data.generate_synthetic_data

# Clean data  
python -m src.data.cleaning --in data/raw/education_outcomes_individual.csv --out data/processed

# Run modeling
python -m src.modeling.logistic_regression

# Launch dashboard (Ctrl+C to stop)
streamlit run dashboards/app.py
```

Expected outputs:
- CSV files in `data/raw/` and `data/processed/`
- Metrics JSON in `reports/metrics_summary.json`
- Dashboard opens in browser

## 📖 Educational Uses

This project is designed for:

✅ **Learning data science workflows**  
✅ **Teaching statistical analysis and modeling**  
✅ **Demonstrating reproducible research practices**  
✅ **Building portfolios and proof-of-concepts**  
✅ **Training on visualization and dashboards**  

❌ **Not for:**
- Real policy decisions without actual data
- Academic research publications
- Grant applications or funding requests

## 🔗 Data Sources (for Real Analysis)

When working with actual Nigerian education data, consider:

1. **National Bureau of Statistics (NBS)**: [https://nigerianstat.gov.ng/](https://nigerianstat.gov.ng/)
2. **Universal Basic Education Commission (UBEC)**: Education statistics
3. **Federal Ministry of Education**: National education data
4. **UNESCO Institute for Statistics**: [http://uis.unesco.org/](http://uis.unesco.org/)
5. **World Bank Open Data**: [https://data.worldbank.org/](https://data.worldbank.org/)
6. **DHS Program**: Demographic and Health Surveys
7. **UNICEF MICS**: Multiple Indicator Cluster Surveys

## 🤝 Contributing

Suggestions and improvements welcome! Areas for enhancement:

- Additional visualization types
- More sophisticated models (hierarchical, causal inference)
- Real data integration pipelines
- Automated testing
- Performance optimizations

## 📄 License

This project is provided for educational and demonstration purposes. The synthetic data is freely available for learning and teaching.

## 👥 Contact

For questions, feedback, or collaboration:
- Open an issue in the repository
- See documentation in `docs/` folder

## 🙏 Acknowledgments

This project structure follows best practices for reproducible data science:
- Cookiecutter Data Science project template
- Tidyverse style guides
- Jupyter best practices
- Streamlit documentation

**Nigerian Education Context**: While this project uses synthetic data, it's inspired by real challenges in education access and quality across Nigeria. For actual statistics and programs, please refer to official government sources and international organizations working in education development.

---

## Quick Reference

### File Locations

- **Raw data**: `data/raw/education_outcomes_individual.csv`
- **Cleaned data**: `data/processed/education_outcomes_cleaned.parquet`
- **State summaries**: `data/processed/education_outcomes_state_summary.csv`
- **Notebook**: `notebooks/01_education_outcomes_eda.ipynb`
- **Dashboard**: `dashboards/app.py`
- **Figures**: `reports/figures/`
- **Model results**: `reports/metrics_summary.json`

### Common Commands

```bash
# Generate data
python -m src.data.generate_synthetic_data

# Clean data
python -m src.data.cleaning --in data/raw/education_outcomes_individual.csv --out data/processed

# Run modeling
python -m src.modeling.logistic_regression

# Start notebook
jupyter lab

# Launch dashboard
streamlit run dashboards/app.py
```

---

**Version**: 1.0  
**Last Updated**: 2024  
**Python**: 3.11+  
**Status**: ✅ Complete and runnable