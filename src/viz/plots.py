"""
Visualization helpers for education outcomes analysis.

This module provides functions to create common plots and charts
for the education outcomes EDA project.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, List


# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10


def plot_correlation_heatmap(
    df: pd.DataFrame,
    features: Optional[List[str]] = None,
    output_path: Optional[str] = None,
    title: str = "Feature Correlation Heatmap"
) -> None:
    """
    Create a correlation heatmap for numeric features.
    
    Args:
        df: Input DataFrame
        features: List of features to include (if None, use all numeric)
        output_path: Path to save figure (if None, display only)
        title: Plot title
    """
    # Select numeric columns
    if features is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        # Exclude z-scores and other derived features for clarity
        features = [col for col in numeric_cols if not col.endswith('_zscore')]
    
    # Calculate correlation matrix
    corr = df[features].corr()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Create heatmap
    sns.heatmap(
        corr,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8},
        ax=ax
    )
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved correlation heatmap to {output_path}")
    
    plt.close()


def plot_state_bars(
    df: pd.DataFrame,
    metric: str = "literacy_rate",
    top_n: int = 10,
    output_path: Optional[str] = None,
    title: Optional[str] = None
) -> None:
    """
    Create bar chart of states ranked by a metric.
    
    Args:
        df: Input DataFrame (should have 'state' column)
        metric: Column name to plot
        top_n: Number of top and bottom states to show
        output_path: Path to save figure
        title: Plot title
    """
    # Aggregate by state if individual-level data
    if 'literacy_outcome' in df.columns and metric == 'literacy_rate':
        state_data = df.groupby('state')['literacy_outcome'].mean() * 100
        state_data.name = 'literacy_rate'
    elif 'state' in df.columns:
        state_data = df.groupby('state')[metric].mean()
    else:
        state_data = df[metric]
    
    # Sort and select top and bottom
    state_data_sorted = state_data.sort_values(ascending=False)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Top states
    top_states = state_data_sorted.head(top_n)
    ax1.barh(range(len(top_states)), top_states.values, color='green', alpha=0.7)
    ax1.set_yticks(range(len(top_states)))
    ax1.set_yticklabels(top_states.index)
    ax1.invert_yaxis()
    ax1.set_xlabel(metric.replace('_', ' ').title())
    ax1.set_title(f'Top {top_n} States', fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Bottom states
    bottom_states = state_data_sorted.tail(top_n)
    ax2.barh(range(len(bottom_states)), bottom_states.values, color='red', alpha=0.7)
    ax2.set_yticks(range(len(bottom_states)))
    ax2.set_yticklabels(bottom_states.index)
    ax2.invert_yaxis()
    ax2.set_xlabel(metric.replace('_', ' ').title())
    ax2.set_title(f'Bottom {top_n} States', fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
    else:
        fig.suptitle(f'{metric.replace("_", " ").title()} by State', 
                     fontsize=14, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved state bar chart to {output_path}")
    
    plt.close()


def feature_effect_plot(
    odds_ratios: pd.DataFrame,
    output_path: Optional[str] = None,
    title: str = "Feature Effects (Odds Ratios)"
) -> None:
    """
    Create a forest plot showing odds ratios with confidence intervals.
    
    Args:
        odds_ratios: DataFrame with columns 'odds_ratio', 'or_ci_lower', 'or_ci_upper'
        output_path: Path to save figure
        title: Plot title
    """
    # Exclude intercept if present
    if 'const' in odds_ratios.index:
        odds_ratios = odds_ratios.drop('const')
    
    # Sort by odds ratio
    odds_ratios = odds_ratios.sort_values('odds_ratio')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot odds ratios with confidence intervals
    y_pos = range(len(odds_ratios))
    
    # Color by direction of effect
    colors = ['green' if or_val > 1 else 'red' 
              for or_val in odds_ratios['odds_ratio']]
    
    ax.scatter(odds_ratios['odds_ratio'], y_pos, color=colors, s=100, zorder=3)
    
    # Add confidence intervals
    for i, (idx, row) in enumerate(odds_ratios.iterrows()):
        ax.plot([row['or_ci_lower'], row['or_ci_upper']], [i, i], 
                color=colors[i], linewidth=2, zorder=2)
    
    # Add vertical line at OR = 1 (no effect)
    ax.axvline(x=1, color='black', linestyle='--', linewidth=1, alpha=0.5)
    
    # Formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels([idx.replace('_', ' ').title() for idx in odds_ratios.index])
    ax.set_xlabel('Odds Ratio (with 95% CI)', fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    # Add text annotations for OR values
    for i, (idx, row) in enumerate(odds_ratios.iterrows()):
        ax.text(row['odds_ratio'], i, f"  {row['odds_ratio']:.2f}", 
                va='center', fontsize=9)
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved feature effect plot to {output_path}")
    
    plt.close()


def plot_distribution(
    df: pd.DataFrame,
    column: str,
    by_group: Optional[str] = None,
    output_path: Optional[str] = None,
    title: Optional[str] = None
) -> None:
    """
    Plot distribution of a variable, optionally by group.
    
    Args:
        df: Input DataFrame
        column: Column to plot
        by_group: Optional grouping variable
        output_path: Path to save figure
        title: Plot title
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if by_group and by_group in df.columns:
        # Plot by group
        for group in df[by_group].unique():
            subset = df[df[by_group] == group][column]
            ax.hist(subset, alpha=0.6, label=str(group), bins=30)
        ax.legend()
    else:
        # Single distribution
        ax.hist(df[column], bins=30, alpha=0.7, color='steelblue')
    
    ax.set_xlabel(column.replace('_', ' ').title(), fontweight='bold')
    ax.set_ylabel('Frequency', fontweight='bold')
    
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    else:
        ax.set_title(f'Distribution of {column.replace("_", " ").title()}',
                     fontsize=14, fontweight='bold')
    
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved distribution plot to {output_path}")
    
    plt.close()


def plot_scatter_by_group(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    group_col: str,
    output_path: Optional[str] = None,
    title: Optional[str] = None
) -> None:
    """
    Create scatter plot with different colors for groups.
    
    Args:
        df: Input DataFrame
        x_col: X-axis column
        y_col: Y-axis column
        group_col: Grouping column
        output_path: Path to save figure
        title: Plot title
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    groups = df[group_col].unique()
    colors = sns.color_palette('husl', n_colors=len(groups))
    
    for i, group in enumerate(groups):
        subset = df[df[group_col] == group]
        ax.scatter(subset[x_col], subset[y_col], 
                  alpha=0.6, label=str(group), color=colors[i], s=50)
    
    # Add regression line for overall trend
    x = df[x_col]
    y = df[y_col]
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), "k--", alpha=0.5, linewidth=2, label='Overall trend')
    
    ax.set_xlabel(x_col.replace('_', ' ').title(), fontweight='bold')
    ax.set_ylabel(y_col.replace('_', ' ').title(), fontweight='bold')
    
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    else:
        ax.set_title(f'{y_col.replace("_", " ").title()} vs {x_col.replace("_", " ").title()}',
                     fontsize=14, fontweight='bold')
    
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved scatter plot to {output_path}")
    
    plt.close()


def plot_group_comparison(
    df: pd.DataFrame,
    metric: str,
    group_by: List[str],
    output_path: Optional[str] = None,
    title: Optional[str] = None
) -> None:
    """
    Create bar plot comparing metric across groups.
    
    Args:
        df: Input DataFrame
        metric: Metric to compare
        group_by: List of grouping variables
        output_path: Path to save figure
        title: Plot title
    """
    # Calculate literacy rate if needed
    if metric == 'literacy_rate' and 'literacy_outcome' in df.columns:
        grouped = df.groupby(group_by)['literacy_outcome'].mean() * 100
    else:
        grouped = df.groupby(group_by)[metric].mean()
    
    grouped = grouped.reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if len(group_by) == 1:
        ax.bar(range(len(grouped)), grouped[metric], alpha=0.7)
        ax.set_xticks(range(len(grouped)))
        ax.set_xticklabels(grouped[group_by[0]], rotation=45, ha='right')
    elif len(group_by) == 2:
        # Pivot for grouped bar chart
        pivot = grouped.pivot(index=group_by[0], columns=group_by[1], values=metric)
        pivot.plot(kind='bar', ax=ax, alpha=0.7)
        ax.legend(title=group_by[1].replace('_', ' ').title())
    
    ax.set_ylabel(metric.replace('_', ' ').title(), fontweight='bold')
    ax.set_xlabel(group_by[0].replace('_', ' ').title(), fontweight='bold')
    
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    else:
        ax.set_title(f'{metric.replace("_", " ").title()} by {" and ".join(group_by)}',
                     fontsize=14, fontweight='bold')
    
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved group comparison plot to {output_path}")
    
    plt.close()


def save_all_figures(df: pd.DataFrame, output_dir: str) -> None:
    """
    Generate and save all standard figures for the analysis.
    
    Args:
        df: Input DataFrame
        output_dir: Directory to save figures
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("Generating figures...")
    
    # Correlation heatmap
    numeric_features = [
        'enrollment_rate', 'pupil_teacher_ratio', 'teacher_qualification_rate',
        'household_poverty_rate', 'mother_education_years', 'household_size',
        'internet_access_rate', 'textbook_availability_index',
        'travel_time_to_school_min', 'electricity_access_rate'
    ]
    if 'literacy_outcome' in df.columns:
        numeric_features.append('literacy_outcome')
    
    plot_correlation_heatmap(
        df, 
        features=numeric_features,
        output_path=output_path / "correlation_heatmap.png"
    )
    
    # State rankings
    plot_state_bars(
        df,
        metric='literacy_rate',
        output_path=output_path / "state_literacy_rankings.png"
    )
    
    # Group comparisons
    if 'sex' in df.columns and 'location' in df.columns:
        plot_group_comparison(
            df,
            metric='literacy_rate',
            group_by=['sex'],
            output_path=output_path / "literacy_by_sex.png",
            title="Literacy Rate by Sex"
        )
        
        plot_group_comparison(
            df,
            metric='literacy_rate',
            group_by=['location'],
            output_path=output_path / "literacy_by_location.png",
            title="Literacy Rate by Location (Urban vs Rural)"
        )
    
    print(f"\nAll figures saved to {output_dir}/")


if __name__ == "__main__":
    print("This module provides visualization functions.")
    print("Import and use the functions in your analysis scripts or notebooks.")
