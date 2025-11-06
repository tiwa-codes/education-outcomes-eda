"""
Generate synthetic education outcomes data for Nigerian states.

This script creates realistic synthetic data for education analysis across
Nigeria's 36 states plus FCT Abuja, with individual-level literacy outcomes
and group-level features.
"""

import numpy as np
import pandas as pd
from pathlib import Path

# Fixed random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Nigeria's 36 states plus FCT Abuja
NIGERIAN_STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue",
    "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu",
    "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi",
    "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo",
    "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara", "FCT Abuja"
]

SEXES = ["M", "F"]
LOCATIONS = ["urban", "rural"]
N_INDIVIDUALS_PER_GROUP = 600  # Total: 37 states × 2 sexes × 2 locations × 600 = 88,800


def generate_group_features():
    """
    Generate group-level features for each state × sex × location combination.
    
    Returns:
        pd.DataFrame: Group-level features with realistic ranges
    """
    groups = []
    
    for state in NIGERIAN_STATES:
        # Add state-specific heterogeneity
        state_effect = np.random.uniform(-0.5, 0.5)
        
        for sex in SEXES:
            for location in LOCATIONS:
                # Generate features with realistic ranges
                # Urban areas generally have better outcomes than rural
                urban_bonus = 15 if location == "urban" else 0
                
                group = {
                    "state": state,
                    "sex": sex,
                    "location": location,
                    "enrollment_rate": np.clip(
                        np.random.uniform(60, 98) + urban_bonus * 0.3, 60, 98
                    ),
                    "pupil_teacher_ratio": np.random.uniform(
                        20 if location == "urban" else 35, 
                        50 if location == "urban" else 80
                    ),
                    "teacher_qualification_rate": np.clip(
                        np.random.uniform(30, 95) + urban_bonus * 0.5, 30, 95
                    ),
                    "household_poverty_rate": np.clip(
                        np.random.uniform(10, 85) - urban_bonus, 10, 85
                    ),
                    "mother_education_years": np.clip(
                        np.random.uniform(0, 14) + urban_bonus * 0.2, 0, 14
                    ),
                    "household_size": np.random.uniform(3, 10),
                    "internet_access_rate": np.clip(
                        np.random.uniform(5, 70) + urban_bonus * 1.5, 5, 70
                    ),
                    "textbook_availability_index": np.clip(
                        np.random.uniform(0.2, 0.95) + urban_bonus * 0.01, 0.2, 0.95
                    ),
                    "travel_time_to_school_min": np.random.uniform(
                        5 if location == "urban" else 15,
                        30 if location == "urban" else 90
                    ),
                    "electricity_access_rate": np.clip(
                        np.random.uniform(10, 95) + urban_bonus * 1.2, 10, 95
                    ),
                    "state_effect": state_effect
                }
                groups.append(group)
    
    return pd.DataFrame(groups)


def calculate_literacy_probability(row):
    """
    Calculate literacy probability using a logistic function.
    
    Features with positive effects: enrollment, teacher qualification, 
    mother education, internet access, textbooks, electricity
    
    Features with negative effects: poverty, pupil-teacher ratio, travel time
    
    Args:
        row: DataFrame row with feature values
        
    Returns:
        float: Probability of literacy (0-1)
    """
    # Standardize features to similar scales for coefficients
    logit = (
        -2.0  # Intercept
        + 0.04 * row["enrollment_rate"]
        - 0.02 * row["pupil_teacher_ratio"]
        + 0.03 * row["teacher_qualification_rate"]
        - 0.02 * row["household_poverty_rate"]
        + 0.15 * row["mother_education_years"]
        - 0.05 * row["household_size"]
        + 0.02 * row["internet_access_rate"]
        + 2.0 * row["textbook_availability_index"]
        - 0.01 * row["travel_time_to_school_min"]
        + 0.01 * row["electricity_access_rate"]
        + row["state_effect"]  # State fixed effect
    )
    
    # Apply logistic function
    probability = 1 / (1 + np.exp(-logit))
    return probability


def generate_individual_data(group_df):
    """
    Generate individual-level data with jitter around group means.
    
    Args:
        group_df: DataFrame with group-level features
        
    Returns:
        pd.DataFrame: Individual-level data with literacy outcomes
    """
    individuals = []
    
    for idx, group_row in group_df.iterrows():
        for i in range(N_INDIVIDUALS_PER_GROUP):
            # Add individual-level jitter around group means
            individual = {
                "state": group_row["state"],
                "sex": group_row["sex"],
                "location": group_row["location"],
                "enrollment_rate": np.clip(
                    group_row["enrollment_rate"] + np.random.normal(0, 3), 0, 100
                ),
                "pupil_teacher_ratio": np.clip(
                    group_row["pupil_teacher_ratio"] + np.random.normal(0, 5), 10, 100
                ),
                "teacher_qualification_rate": np.clip(
                    group_row["teacher_qualification_rate"] + np.random.normal(0, 5), 0, 100
                ),
                "household_poverty_rate": np.clip(
                    group_row["household_poverty_rate"] + np.random.normal(0, 5), 0, 100
                ),
                "mother_education_years": np.clip(
                    group_row["mother_education_years"] + np.random.normal(0, 1), 0, 16
                ),
                "household_size": np.clip(
                    group_row["household_size"] + np.random.normal(0, 1), 1, 15
                ),
                "internet_access_rate": np.clip(
                    group_row["internet_access_rate"] + np.random.normal(0, 5), 0, 100
                ),
                "textbook_availability_index": np.clip(
                    group_row["textbook_availability_index"] + np.random.normal(0, 0.1), 0, 1
                ),
                "travel_time_to_school_min": np.clip(
                    group_row["travel_time_to_school_min"] + np.random.normal(0, 10), 0, 180
                ),
                "electricity_access_rate": np.clip(
                    group_row["electricity_access_rate"] + np.random.normal(0, 5), 0, 100
                ),
                "state_effect": group_row["state_effect"]
            }
            
            # Calculate literacy probability and sample outcome
            prob = calculate_literacy_probability(pd.Series(individual))
            # Add individual noise
            prob = np.clip(prob + np.random.normal(0, 0.05), 0, 1)
            individual["literacy_outcome"] = np.random.binomial(1, prob)
            
            individuals.append(individual)
    
    return pd.DataFrame(individuals)


def create_state_summaries(individual_df):
    """
    Create aggregated summaries by state and by state × sex × location.
    
    Args:
        individual_df: Individual-level data
        
    Returns:
        pd.DataFrame: Aggregated summary statistics
    """
    # Group by state, sex, location
    group_summary = individual_df.groupby(["state", "sex", "location"]).agg({
        "literacy_outcome": "mean",
        "enrollment_rate": "mean",
        "pupil_teacher_ratio": "mean",
        "teacher_qualification_rate": "mean",
        "household_poverty_rate": "mean",
        "mother_education_years": "mean",
        "household_size": "mean",
        "internet_access_rate": "mean",
        "textbook_availability_index": "mean",
        "travel_time_to_school_min": "mean",
        "electricity_access_rate": "mean"
    }).reset_index()
    
    # Rename literacy_outcome to literacy_rate
    group_summary.rename(columns={"literacy_outcome": "literacy_rate"}, inplace=True)
    group_summary["literacy_rate"] *= 100  # Convert to percentage
    
    # Add count
    counts = individual_df.groupby(["state", "sex", "location"]).size().reset_index(name="count")
    group_summary = group_summary.merge(counts, on=["state", "sex", "location"])
    
    return group_summary


def main():
    """
    Main function to generate and save synthetic data.
    """
    print("Generating synthetic education outcomes data for Nigeria...")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"States: {len(NIGERIAN_STATES)}")
    print(f"Groups: {len(NIGERIAN_STATES) * len(SEXES) * len(LOCATIONS)}")
    print(f"Individuals per group: {N_INDIVIDUALS_PER_GROUP}")
    
    # Create output directories
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate group-level features
    print("\nGenerating group-level features...")
    group_df = generate_group_features()
    
    # Generate individual-level data
    print("Generating individual-level data...")
    individual_df = generate_individual_data(group_df)
    print(f"Total individuals: {len(individual_df):,}")
    
    # Save individual data
    individual_path = raw_dir / "education_outcomes_individual.csv"
    print(f"\nSaving individual data to {individual_path}...")
    individual_df.to_csv(individual_path, index=False)
    print(f"Saved {len(individual_df):,} rows")
    
    # Create and save state summaries
    print("\nCreating state summaries...")
    summary_df = create_state_summaries(individual_df)
    summary_path = processed_dir / "education_outcomes_state_summary.csv"
    print(f"Saving state summary to {summary_path}...")
    summary_df.to_csv(summary_path, index=False)
    print(f"Saved {len(summary_df)} summary rows")
    
    # Print sample statistics
    print("\n" + "="*60)
    print("Data Generation Complete!")
    print("="*60)
    print(f"\nOverall literacy rate: {individual_df['literacy_outcome'].mean()*100:.1f}%")
    print(f"Urban literacy rate: {individual_df[individual_df['location']=='urban']['literacy_outcome'].mean()*100:.1f}%")
    print(f"Rural literacy rate: {individual_df[individual_df['location']=='rural']['literacy_outcome'].mean()*100:.1f}%")
    print(f"Male literacy rate: {individual_df[individual_df['sex']=='M']['literacy_outcome'].mean()*100:.1f}%")
    print(f"Female literacy rate: {individual_df[individual_df['sex']=='F']['literacy_outcome'].mean()*100:.1f}%")
    
    print("\nTop 5 states by literacy rate:")
    state_rates = individual_df.groupby("state")["literacy_outcome"].mean().sort_values(ascending=False)
    for state, rate in state_rates.head().items():
        print(f"  {state}: {rate*100:.1f}%")
    
    print("\nBottom 5 states by literacy rate:")
    for state, rate in state_rates.tail().items():
        print(f"  {state}: {rate*100:.1f}%")


if __name__ == "__main__":
    main()
