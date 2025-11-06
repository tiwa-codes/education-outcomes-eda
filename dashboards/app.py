"""
Streamlit dashboard for education outcomes analysis.

This interactive dashboard allows users to explore literacy rates and 
associated factors across Nigerian states with dynamic filters.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np


# Page configuration
st.set_page_config(
    page_title="Nigeria Education Outcomes Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_data():
    """Load processed state summary data."""
    # Try to load the state summary
    summary_path = Path("data/processed/education_outcomes_state_summary.csv")
    
    if not summary_path.exists():
        st.error(f"Data file not found: {summary_path}")
        st.info("Please run data generation first: `python -m src.data.generate_synthetic_data`")
        st.stop()
    
    df = pd.read_csv(summary_path)
    return df


def filter_data(df, states, sex, location):
    """Apply filters to the data."""
    filtered = df.copy()
    
    if states and len(states) > 0:
        filtered = filtered[filtered['state'].isin(states)]
    
    if sex != "All":
        filtered = filtered[filtered['sex'] == sex]
    
    if location != "All":
        filtered = filtered[filtered['location'] == location]
    
    return filtered


def main():
    """Main dashboard function."""
    
    # Header
    st.title("📚 Nigeria Education Outcomes Dashboard")
    st.markdown("""
    Explore literacy rates and associated factors across Nigerian states.
    **Note:** This dashboard uses synthetic data for demonstration purposes.
    """)
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # State selection
    all_states = sorted(df['state'].unique())
    selected_states = st.sidebar.multiselect(
        "Select States",
        options=all_states,
        default=all_states[:5],  # Default to first 5 states
        help="Select one or more states to analyze"
    )
    
    # Sex filter
    sex_filter = st.sidebar.selectbox(
        "Sex",
        options=["All", "M", "F"],
        help="Filter by sex"
    )
    
    # Location filter
    location_filter = st.sidebar.selectbox(
        "Location",
        options=["All", "urban", "rural"],
        help="Filter by location type"
    )
    
    # Apply filters
    if not selected_states:
        st.warning("Please select at least one state from the sidebar.")
        st.stop()
    
    filtered_df = filter_data(df, selected_states, sex_filter, location_filter)
    
    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters. Please adjust your selection.")
        st.stop()
    
    # Key metrics
    st.header("📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_literacy = filtered_df['literacy_rate'].mean()
        st.metric("Literacy Rate", f"{avg_literacy:.1f}%")
    
    with col2:
        avg_enrollment = filtered_df['enrollment_rate'].mean()
        st.metric("Enrollment Rate", f"{avg_enrollment:.1f}%")
    
    with col3:
        avg_teacher_qual = filtered_df['teacher_qualification_rate'].mean()
        st.metric("Teacher Qualification Rate", f"{avg_teacher_qual:.1f}%")
    
    with col4:
        avg_poverty = filtered_df['household_poverty_rate'].mean()
        st.metric("Poverty Rate", f"{avg_poverty:.1f}%")
    
    # Main visualizations
    st.header("📈 Visualizations")
    
    # Tab layout
    tab1, tab2, tab3, tab4 = st.tabs([
        "Literacy by State", 
        "Enrollment vs Literacy", 
        "Teacher Ratio Impact",
        "Poverty & Education"
    ])
    
    with tab1:
        st.subheader("Literacy Rate by State")
        
        # Aggregate by state for the chart
        state_literacy = filtered_df.groupby('state')['literacy_rate'].mean().reset_index()
        state_literacy = state_literacy.sort_values('literacy_rate', ascending=True)
        
        fig = px.bar(
            state_literacy,
            x='literacy_rate',
            y='state',
            orientation='h',
            title='Literacy Rate by State',
            labels={'literacy_rate': 'Literacy Rate (%)', 'state': 'State'},
            color='literacy_rate',
            color_continuous_scale='viridis'
        )
        fig.update_layout(height=max(400, len(state_literacy) * 25))
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Enrollment Rate vs Literacy Rate")
        
        fig = px.scatter(
            filtered_df,
            x='enrollment_rate',
            y='literacy_rate',
            color='location',
            size='count',
            hover_data=['state', 'sex'],
            title='Enrollment Rate vs Literacy Rate',
            labels={
                'enrollment_rate': 'Enrollment Rate (%)',
                'literacy_rate': 'Literacy Rate (%)',
                'location': 'Location'
            },
            trendline='ols'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **Insight:** Higher enrollment rates are generally associated with higher literacy rates.")
    
    with tab3:
        st.subheader("Pupil-Teacher Ratio vs Literacy Rate")
        
        fig = px.scatter(
            filtered_df,
            x='pupil_teacher_ratio',
            y='literacy_rate',
            color='location',
            size='count',
            hover_data=['state', 'sex'],
            title='Pupil-Teacher Ratio vs Literacy Rate',
            labels={
                'pupil_teacher_ratio': 'Pupil-Teacher Ratio',
                'literacy_rate': 'Literacy Rate (%)',
                'location': 'Location'
            },
            trendline='ols'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **Insight:** Lower pupil-teacher ratios (better staffing) are associated with higher literacy rates.")
    
    with tab4:
        st.subheader("Poverty Rate and Education Access")
        
        # Create a combined view
        fig = go.Figure()
        
        # Poverty vs Literacy
        fig.add_trace(go.Scatter(
            x=filtered_df['household_poverty_rate'],
            y=filtered_df['literacy_rate'],
            mode='markers',
            name='Poverty vs Literacy',
            marker=dict(size=10, opacity=0.6),
            text=filtered_df['state'],
            hovertemplate='<b>%{text}</b><br>Poverty: %{x:.1f}%<br>Literacy: %{y:.1f}%<extra></extra>'
        ))
        
        # Add trendline
        z = np.polyfit(filtered_df['household_poverty_rate'], filtered_df['literacy_rate'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(
            filtered_df['household_poverty_rate'].min(),
            filtered_df['household_poverty_rate'].max(),
            100
        )
        fig.add_trace(go.Scatter(
            x=x_trend,
            y=p(x_trend),
            mode='lines',
            name='Trend',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title='Household Poverty Rate vs Literacy Rate',
            xaxis_title='Household Poverty Rate (%)',
            yaxis_title='Literacy Rate (%)',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **Insight:** Higher poverty rates are associated with lower literacy rates.")
    
    # Additional insights section
    st.header("🎯 Disparities Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("By Sex")
        sex_comparison = df.groupby('sex')['literacy_rate'].mean().reset_index()
        fig = px.bar(
            sex_comparison,
            x='sex',
            y='literacy_rate',
            color='sex',
            title='Average Literacy Rate by Sex',
            labels={'literacy_rate': 'Literacy Rate (%)', 'sex': 'Sex'},
            color_discrete_map={'M': 'blue', 'F': 'pink'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("By Location")
        location_comparison = df.groupby('location')['literacy_rate'].mean().reset_index()
        fig = px.bar(
            location_comparison,
            x='location',
            y='literacy_rate',
            color='location',
            title='Average Literacy Rate by Location',
            labels={'literacy_rate': 'Literacy Rate (%)', 'location': 'Location'},
            color_discrete_map={'urban': 'green', 'rural': 'brown'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.header("📋 Filtered Data Summary")
    
    # Display summary statistics
    display_cols = [
        'state', 'sex', 'location', 'literacy_rate', 'enrollment_rate',
        'pupil_teacher_ratio', 'teacher_qualification_rate', 'household_poverty_rate'
    ]
    
    st.dataframe(
        filtered_df[display_cols].sort_values('literacy_rate', ascending=False),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_education_data.csv",
        mime="text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **About This Dashboard**
    
    This dashboard presents synthetic data for demonstration and educational purposes.
    The data simulates education outcomes across Nigeria's 36 states plus FCT Abuja.
    
    **Limitations:**
    - Data is synthetic and does not represent actual education statistics
    - Associations shown are not causal relationships
    - Should not be used for actual policy decisions
    
    For questions or feedback, refer to the project documentation.
    """)


if __name__ == "__main__":
    main()
