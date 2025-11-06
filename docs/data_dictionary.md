# Data Dictionary: Nigeria Education Outcomes Dataset

## Overview

This dataset contains synthetic individual-level and aggregated data on education outcomes across Nigeria's 36 states plus FCT Abuja. The data is designed to simulate realistic patterns for educational analysis but **does not represent actual statistics**.

## Purpose

This synthetic dataset is created for:
- Demonstrating exploratory data analysis techniques
- Teaching statistical modeling methods
- Building example dashboards and visualizations
- Educational and training purposes

**⚠️ Important:** Do not use this data for real policy decisions or research publications.

---

## Data Files

### 1. `education_outcomes_individual.csv`
Individual-level records with literacy outcomes and feature values.

**Rows:** ~88,800 individuals (600 per state × sex × location combination)

### 2. `education_outcomes_state_summary.csv`
Aggregated summary statistics by state, sex, and location.

**Rows:** 296 groups (37 states × 2 sexes × 2 locations + 2 locations)

### 3. `education_outcomes_cleaned.csv` / `.parquet`
Cleaned individual data with derived features and validation.

---

## Variables

### Categorical Variables

| Variable | Type | Values | Description |
|----------|------|--------|-------------|
| `state` | Categorical | 37 states | Nigerian state name (36 states + FCT Abuja) |
| `sex` | Categorical | M, F | Sex of individual |
| `location` | Categorical | urban, rural | Location type |

### Target Variable

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `literacy_outcome` | Binary | 0, 1 | Whether individual achieved basic literacy (1 = literate, 0 = not literate) |
| `literacy_rate` | Float | 0-100 | Percentage of individuals literate in a group (aggregated data only) |

### Feature Variables

#### Education System Features

| Variable | Type | Range | Unit | Description |
|----------|------|-------|------|-------------|
| `enrollment_rate` | Float | 60-98 | Percentage | School enrollment rate in the area |
| `pupil_teacher_ratio` | Float | 20-80 | Ratio | Number of pupils per teacher |
| `teacher_qualification_rate` | Float | 30-95 | Percentage | Proportion of qualified teachers |
| `textbook_availability_index` | Float | 0.2-0.95 | Index (0-1) | Measure of textbook availability and quality |
| `travel_time_to_school_min` | Float | 5-90 | Minutes | Average travel time to nearest school |

#### Household & Socioeconomic Features

| Variable | Type | Range | Unit | Description |
|----------|------|-------|------|-------------|
| `household_poverty_rate` | Float | 10-85 | Percentage | Proportion of households below poverty line |
| `mother_education_years` | Float | 0-14 | Years | Years of formal education of mother/guardian |
| `household_size` | Float | 3-10 | Count | Number of people in household |

#### Infrastructure Features

| Variable | Type | Range | Unit | Description |
|----------|------|-------|------|-------------|
| `internet_access_rate` | Float | 5-70 | Percentage | Proportion with internet access |
| `electricity_access_rate` | Float | 10-95 | Percentage | Proportion with reliable electricity access |

### Derived Features (Cleaned Data Only)

| Variable | Type | Description |
|----------|------|-------------|
| `*_zscore` | Float | Z-score (standardized) version of key features |
| `poverty_category` | Categorical | Binned poverty rate: Low, Medium, High, Very High |
| `mother_education_category` | Categorical | Binned education: None, Primary, Secondary, Tertiary |
| `enrollment_category` | Categorical | Binned enrollment: Low, Medium, High, Very High |

---

## Data Generation Method

### Synthetic Data Generation Process

1. **Group-Level Features:** For each state × sex × location combination:
   - Base feature values sampled from realistic ranges
   - Urban areas given systematic advantage (higher enrollment, lower poverty, etc.)
   - State-level random effects added for heterogeneity

2. **Individual-Level Data:** For each group:
   - 600 individuals generated with jitter around group means
   - Individual variation added using normal distributions

3. **Literacy Outcome:** Binary outcome generated via:
   - Logistic function applied to weighted combination of features
   - Positive weights: enrollment, teacher qualification, mother education, internet, textbooks, electricity
   - Negative weights: poverty, pupil-teacher ratio, travel time, household size
   - State fixed effects and individual-level noise added
   - Outcome sampled from Bernoulli distribution with calculated probability

4. **Reproducibility:** Fixed random seed (42) ensures consistent data generation

---

## Data Quality Notes

### Validation Steps Applied

- **Duplicates:** Removed duplicate records
- **Missing Values:** No missing values in generated data
- **Range Validation:** 
  - Percentages clipped to 0-100
  - Index values clipped to 0-1
  - Non-negative constraints enforced
- **Data Types:** Proper type enforcement (categorical, integer, float)

### Known Limitations

1. **Synthetic Nature:** Data follows programmed patterns; real-world data is messier
2. **Simplified Relationships:** Linear associations in logistic model; reality is more complex
3. **Omitted Variables:** Many important factors not included (school quality, teacher motivation, etc.)
4. **No Measurement Error:** Real data has noise from measurement and reporting issues
5. **No Temporal Variation:** Cross-sectional snapshot only
6. **Ecological Fallacy Risk:** Group-level patterns may not hold at individual level

---

## Ethical Considerations

### Privacy

- **No Real Data:** All data is synthetically generated
- **No Identifiable Information:** No names, addresses, or identifiable details
- **Aggregation:** Individual data aggregated to protect privacy in reports

### Bias and Fairness

- **Programmed Patterns:** Data generation includes realistic disparities (urban/rural, etc.)
- **Not for Discrimination:** Should not be used to make decisions about real individuals or communities
- **Awareness:** Users should be aware that real-world biases may be different

### Appropriate Use

✅ **Appropriate Uses:**
- Learning data analysis and modeling techniques
- Demonstrating visualization and dashboard tools
- Teaching statistics and data science
- Prototyping analysis pipelines

❌ **Inappropriate Uses:**
- Real policy decisions without actual data
- Academic research publications
- Grant applications or funding decisions
- Stigmatizing or stereotyping real communities

---

## Data Sources (for Real Data)

When working with actual Nigerian education data, consider these sources:

1. **National Bureau of Statistics (NBS):** Education statistics and surveys
2. **Universal Basic Education Commission (UBEC):** Primary education data
3. **Federal Ministry of Education:** National education statistics
4. **UNESCO Institute for Statistics:** International education indicators
5. **World Bank:** Development indicators including education
6. **DHS (Demographic and Health Surveys):** Household survey data
7. **MICS (Multiple Indicator Cluster Surveys):** Child and household data

---

## Contact and Updates

For questions about this synthetic dataset or suggestions for improvements:

- **Repository:** [GitHub repository URL]
- **Documentation:** See README.md and notebooks/
- **Version:** 1.0 (synthetic demonstration data)

---

## Changelog

- **v1.0 (2024):** Initial synthetic dataset creation with individual and aggregated data

---

**Last Updated:** 2024

**License:** This synthetic dataset is provided for educational purposes. Feel free to use and modify for learning and demonstration purposes.
