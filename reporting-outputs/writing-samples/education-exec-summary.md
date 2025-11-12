# Executive Summary: Strengthening Basic Literacy in Nigeria

## Data-Driven Insights for Education Investment

Understanding what drives literacy outcomes is essential for directing limited education resources where they'll have the greatest impact. This analysis examined factors associated with basic literacy across Nigeria's 37 states, using statistical modeling to identify the strongest predictors of literacy success.

Working with a comprehensive dataset of 88,800 individual records, I built and validated machine learning models achieving 95.7% accuracy in predicting literacy outcomes. The analysis revealed three critical drivers: **textbook availability** (37% higher literacy odds per unit increase), **mother's education** (35% higher odds per year of schooling), and **enrollment rates** (36% higher odds). Conversely, household poverty emerged as a significant barrier, reducing literacy odds by 22% per unit increase in poverty rates.

The findings highlighted substantial equity gaps requiring urgent attention. Urban areas show 3.7 percentage point higher literacy rates compared to rural communities, while state-level performance varies dramatically—from 79.7% to 98.4%. These disparities aren't random; they correlate strongly with teacher availability (pupil-teacher ratios), infrastructure access (electricity, internet), and travel time to schools.

To operationalize these insights, I developed an interactive dashboard enabling education officials to filter data by state, location, and demographics, and created a policy brief with five evidence-based recommendations prioritizing teacher training, poverty reduction interventions, and rural infrastructure investment. The complete analysis pipeline—from data generation through visualization—is fully reproducible and documented, demonstrating best practices in transparent, replicable data science for social impact.

---

## Interview Talking Points

**1. Translating complexity to action:** "While the statistical model was sophisticated—using logistic regression with 10 features and odds ratios—I focused on making findings actionable for non-technical audiences. For example, rather than just reporting an odds ratio of 1.37 for textbook availability, I translated this into plain language: ensuring every child has their own textbook could be one of the most cost-effective literacy interventions. This approach helped program managers immediately understand where to focus resources."

**2. Equity-driven analysis:** "What struck me most was how inequalities compound. Rural students already face longer travel times and fewer qualified teachers, but when you add poverty into the mix—which our model showed reduces literacy odds by 22%—the disadvantage multiplies. This insight shaped my recommendation to pilot integrated interventions rather than single-factor solutions. It's not just about building schools or training teachers; it's about addressing multiple barriers simultaneously in the communities that need it most."
