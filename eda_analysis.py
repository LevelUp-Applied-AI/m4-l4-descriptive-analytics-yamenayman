'''
"""Lab 4 — Descriptive Analytics: Student Performance EDA

Conduct exploratory data analysis on the student performance dataset.
Produce distribution plots, correlation analysis, hypothesis tests,
and a written findings report.

Usage:
    python eda_analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def load_and_profile(filepath):
    """Load the dataset and generate a data profile report.

    Args:
        filepath: path to the CSV file (e.g., 'data/student_performance.csv')

    Returns:
        DataFrame: the loaded dataset

    Side effects:
        Saves a text profile to output/data_profile.txt containing:
        - Shape (rows, columns)
        - Data types for each column
        - Missing value counts per column
        - Descriptive statistics for numeric columns
    """
    # TODO: Load the dataset and report its shape, data types, missing values,
    #       and descriptive statistics to output/data_profile.txt
    pass


def plot_distributions(df):
    """Create distribution plots for key numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least 3 distribution plots (histograms with KDE or box plots)
        as PNG files in the output/ directory. Each plot should have a
        descriptive title that states what the distribution reveals.
    """
    # TODO: Create distribution plots for numeric columns like GPA,
    #       study hours, attendance, and commute minutes
    # TODO: Use histograms with KDE overlay (sns.histplot) or box plots
    # TODO: Save each plot to the output/ directory
    pass


def plot_correlations(df):
    """Analyze and visualize relationships between numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least one correlation visualization to the output/ directory
        (e.g., a heatmap, scatter plot, or pair plot).
    """
    # TODO: Compute the correlation matrix for numeric columns
    # TODO: Create a heatmap or scatter plots showing key relationships
    # TODO: Save the visualization(s) to the output/ directory
    pass


def run_hypothesis_tests(df):
    """Run statistical tests to validate observed patterns.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        dict: test results with keys like 'internship_ttest', 'dept_anova',
              each containing the test statistic and p-value

    Side effects:
        Prints test results to stdout with interpretation.

    Tests to consider:
        - t-test: Does GPA differ between students with and without internships?
        - ANOVA: Does GPA differ across departments?
        - Correlation test: Is the correlation between study hours and GPA significant?
    """
    # TODO: Run at least two hypothesis tests on patterns you observe in the data
    # TODO: Report the test statistic, p-value, and your interpretation
    pass


def main():
    """Orchestrate the full EDA pipeline."""
    os.makedirs("output", exist_ok=True)

    # TODO: Load and profile the dataset
    # TODO: Generate distribution plots
    # TODO: Analyze correlations
    # TODO: Run hypothesis tests
    # TODO: Write a FINDINGS.md summarizing your analysis


if __name__ == "__main__":
    main()
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os


os.makedirs('output', exist_ok=True)

def task1_inspect_and_clean(df):
    """Task 1: Data Inspection and Cleaning"""
    profile_path = 'output/data_profile.txt'
    
    with open(profile_path, 'w') as f:
        f.write("=== Data Profile ===\n\n")
        f.write(f"1. Shape (rows, columns): {df.shape}\n\n")
        f.write("2. Data Types:\n")
        f.write(f"{df.dtypes.to_string()}\n\n")
        
        f.write("3. Missing Values (Count and Percentage):\n")
        missing_count = df.isnull().sum()
        missing_pct = (df.isnull().sum() / len(df)) * 100
        missing_df = pd.DataFrame({'Count': missing_count, 'Percentage %': missing_pct})
        f.write(f"{missing_df.to_string()}\n\n")
        
        f.write("4. Handling Decisions:\n")
        f.write("- commute_minutes: Imputed with the median. Reasoning: It's a numerical variable with ~10% missing (MCAR), and median is robust to outliers.\n")
        f.write("- study_hours_weekly: Dropped rows with missing values. Reasoning: It represents ~5% (MCAR), dropping them won't significantly impact the large sample size.\n")
        
    # Cleaning
    df['commute_minutes'] = df['commute_minutes'].fillna(df['commute_minutes'].median())
    
    df_cleaned = df.dropna(subset=['study_hours_weekly'])
    
    df_cleaned['scholarship'] = df_cleaned['scholarship'].fillna('None')
    return df_cleaned

def task2_distributions(df):
    """Task 2: Distribution Analysis"""

    cols_to_plot = ['gpa', 'study_hours_weekly', 'attendance_pct']
    for col in cols_to_plot:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col], kde=True, bins=30)
        plt.title(f'Distribution of {col}')
        plt.savefig(f'output/dist_{col}.png')
        plt.close()


    plt.figure(figsize=(10, 6))
    sns.boxplot(x='department', y='gpa', data=df)
    plt.title('GPA Distribution across Departments')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output/gpa_by_department.png')
    plt.close()


    plt.figure(figsize=(8, 5))
    sns.countplot(x='scholarship', data=df, palette='viridis')
    plt.title('Distribution of Scholarship Types')
    plt.savefig('output/scholarship_distribution.png')
    plt.close()

def task3_correlation(df):
    """Task 3: Correlation Analysis"""

    numeric_df = df.select_dtypes(include=[np.number])
    

    corr_matrix = numeric_df.corr()
    

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix Heatmap')
    plt.tight_layout()
    plt.savefig('output/correlation_heatmap.png')
    plt.close()


    plt.figure(figsize=(8, 5))
    sns.scatterplot(x='study_hours_weekly', y='gpa', data=df, alpha=0.5)
    plt.title('Scatter Plot: Study Hours vs GPA')
    plt.savefig('output/scatter_study_gpa.png')
    plt.close()

def task4_hypothesis_testing(df):
    """Task 4: Hypothesis Testing"""
    print("\n" + "="*40)
    print("TASK 4: HYPOTHESIS TESTING RESULTS")
    print("="*40)
    

    interns = df[df['has_internship'] == 'Yes']['gpa'].dropna()
    non_interns = df[df['has_internship'] == 'No']['gpa'].dropna()
    
    t_stat, p_val_t = stats.ttest_ind(interns, non_interns, equal_var=False)
    

    n1, n2 = len(interns), len(non_interns)
    var1, var2 = interns.var(), non_interns.var()
    pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    cohens_d = (interns.mean() - non_interns.mean()) / np.sqrt(pooled_var)
    
    print("\n--- Hypothesis 1 ---")
    print("H1: Students with internships have a higher GPA than students without internships.")
    print(f"Independent t-test -> t-statistic: {t_stat:.4f}, p-value: {p_val_t:.4e}")
    print(f"Cohen's d: {cohens_d:.4f}")
    if p_val_t < 0.05:
        print("Interpretation: There is a statistically significant difference in GPA between students with and without internships.")
    else:
        print("Interpretation: There is NO statistically significant difference in GPA.")


    print("\n--- Hypothesis 2 ---")
    print("H2: Scholarship status is associated with department.")
    contingency_table = pd.crosstab(df['scholarship'], df['department'])
    chi2, p_val_chi, dof, expected = stats.chi2_contingency(contingency_table)
    
    print(f"Chi-square test -> Chi2 statistic: {chi2:.4f}, p-value: {p_val_chi:.4e}, Degrees of Freedom: {dof}")
    if p_val_chi < 0.05:
        print("Interpretation: There is a statistically significant association between the department and the type of scholarship received.")
    else:
        print("Interpretation: There is NO statistically significant association between department and scholarship status.")
    print("="*40 + "\n")

def main():

    df = pd.read_csv('data/student_performance.csv')
    

    df_clean = task1_inspect_and_clean(df)
    task2_distributions(df_clean)
    task3_correlation(df_clean)
    task4_hypothesis_testing(df_clean)
    print("EDA completed successfully. All files saved to the 'output' directory.")

if __name__ == "__main__":
    main()