Person 1: Data Analysis (Task 1 + Task 5 Enhancement)
TASK 1: Dataset Analysis and Insights
Step 1: Set Up Python Environment
bashcd ~/cloud-diet-analysis
mkdir task1_analysis
cd task1_analysis

# Install required Python packages

pip3 install pandas matplotlib seaborn --break-system-packages
Step 2: Copy the Dataset
bashcp ~/diet-project/All_Diets.csv .

Step 3: Create the Data Analysis Script
Create a file called data_analysis.py:
bashcode data_analysis.py

Add the following code:
pythonimport pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Print current date/time for screenshot verification

print(f"Analysis run at: {datetime.now()}")

# Load the dataset

print("Loading dataset...")
df = pd.read_csv('All_Diets.csv')

# Display basic info

print(f"\nDataset shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())

# ===== DATA CLEANING =====

print("\n" + "="*50)
print("DATA CLEANING")
print("="*50)

# Check for missing values

print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Handle missing values - fill with mean for numeric columns

numeric_columns = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
for col in numeric_columns:
if df[col].isnull().any():
mean_value = df[col].mean()
df[col].fillna(mean_value, inplace=True)
print(f"Filled {col} missing values with mean: {mean_value:.2f}")

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# ===== ANALYSIS 1: Average Macronutrient Content by Diet Type =====

print("\n" + "="*50)
print("ANALYSIS 1: Average Macronutrients by Diet Type")
print("="*50)

avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
print("\nAverage macronutrients per diet type:")
print(avg_macros)

# ===== ANALYSIS 2: Top 5 Protein-Rich Recipes per Diet Type =====

print("\n" + "="*50)
print("ANALYSIS 2: Top 5 Protein-Rich Recipes per Diet Type")
print("="*50)

top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
print("\nTop protein recipes:")
print(top_protein[['Diet_type', 'Recipe_name', 'Protein(g)']].to_string())

# ===== ANALYSIS 3: Diet Type with Highest Protein =====

print("\n" + "="*50)
print("ANALYSIS 3: Diet Type with Highest Protein Content")
print("="*50)

highest_protein_diet = avg_macros['Protein(g)'].idxmax()
highest_protein_value = avg_macros['Protein(g)'].max()
print(f"\nDiet type with highest average protein: {highest_protein_diet}")
print(f"Average protein content: {highest_protein_value:.2f}g")

# ===== ANALYSIS 4: Most Common Cuisines per Diet Type =====

print("\n" + "="*50)
print("ANALYSIS 4: Most Common Cuisines per Diet Type")
print("="*50)

most_common_cuisines = df.groupby('Diet_type')['Cuisine_type'].agg(lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A')
print("\nMost common cuisine per diet type:")
print(most_common_cuisines)

# ===== ANALYSIS 5: Create New Metrics =====

print("\n" + "="*50)
print("ANALYSIS 5: Creating New Metrics")
print("="*50)

# Protein-to-Carbs ratio (handle division by zero)

df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)'].replace(0, np.nan)

# Carbs-to-Fat ratio (handle division by zero)

df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)'].replace(0, np.nan)

print("\nNew metrics added:")
print(df[['Recipe_name', 'Protein_to_Carbs_ratio', 'Carbs_to_Fat_ratio']].head(10))

# Save processed data

df.to_csv('processed_diets.csv', index=False)
print("\nProcessed data saved to 'processed_diets.csv'")

# ===== VISUALIZATIONS =====

print("\n" + "="*50)
print("CREATING VISUALIZATIONS")
print("="*50)

# Set style

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Visualization 1: Bar Chart - Average Protein by Diet Type

print("\nCreating Bar Chart: Average Protein by Diet Type...")
plt.figure(figsize=(12, 6))
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'], palette='viridis')
plt.title(f'Average Protein by Diet Type - {datetime.now().strftime("%Y-%m-%d %H:%M")}', fontsize=16, fontweight='bold')
plt.xlabel('Diet Type', fontsize=12)
plt.ylabel('Average Protein (g)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('viz1_avg_protein_bar.png', dpi=300, bbox_inches='tight')
print("Saved: viz1_avg_protein_bar.png")
plt.show()

# Visualization 2: Bar Chart - All Macronutrients by Diet Type

print("\nCreating Bar Chart: All Macronutrients by Diet Type...")
avg_macros_reset = avg_macros.reset_index()
avg_macros_melted = avg_macros_reset.melt(id_vars='Diet_type',
value_vars=['Protein(g)', 'Carbs(g)', 'Fat(g)'],
var_name='Macronutrient',
value_name='Average (g)')

plt.figure(figsize=(14, 6))
sns.barplot(data=avg_macros_melted, x='Diet_type', y='Average (g)', hue='Macronutrient', palette='Set2')
plt.title(f'Average Macronutrient Content by Diet Type - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
fontsize=16, fontweight='bold')
plt.xlabel('Diet Type', fontsize=12)
plt.ylabel('Average Content (g)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Macronutrient')
plt.tight_layout()
plt.savefig('viz2_all_macros_bar.png', dpi=300, bbox_inches='tight')
print("Saved: viz2_all_macros_bar.png")
plt.show()

# Visualization 3: Heatmap - Macronutrient Content by Diet Type

print("\nCreating Heatmap: Macronutrient Content by Diet Type...")
plt.figure(figsize=(10, 8))
sns.heatmap(avg_macros, annot=True, fmt='.2f', cmap='YlOrRd', linewidths=0.5)
plt.title(f'Heatmap: Macronutrient Content by Diet Type - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
fontsize=16, fontweight='bold')
plt.xlabel('Macronutrient', fontsize=12)
plt.ylabel('Diet Type', fontsize=12)
plt.tight_layout()
plt.savefig('viz3_heatmap_macros.png', dpi=300, bbox_inches='tight')
print("Saved: viz3_heatmap_macros.png")
plt.show()

# Visualization 4: Scatter Plot - Top Protein Recipes by Cuisine

print("\nCreating Scatter Plot: Top Protein Recipes Distribution...")
plt.figure(figsize=(14, 8))
sns.scatterplot(data=top_protein,
x='Protein(g)',
y='Carbs(g)',
hue='Diet_type',
size='Fat(g)',
sizes=(50, 400),
alpha=0.7,
palette='tab10')
plt.title(f'Top 5 Protein-Rich Recipes Distribution - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
fontsize=16, fontweight='bold')
plt.xlabel('Protein (g)', fontsize=12)
plt.ylabel('Carbs (g)', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('viz4_scatter_top_protein.png', dpi=300, bbox_inches='tight')
print("Saved: viz4_scatter_top_protein.png")
plt.show()

# Visualization 5: Scatter Plot by Cuisine

print("\nCreating Scatter Plot: Protein Distribution by Cuisine...")
plt.figure(figsize=(14, 8))
top_cuisines = df['Cuisine_type'].value_counts().head(10).index
df_top_cuisines = df[df['Cuisine_type'].isin(top_cuisines)]

sns.scatterplot(data=df_top_cuisines,
x='Protein(g)',
y='Fat(g)',
hue='Cuisine_type',
alpha=0.6,
palette='husl')
plt.title(f'Protein vs Fat Distribution by Top Cuisines - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
fontsize=16, fontweight='bold')
plt.xlabel('Protein (g)', fontsize=12)
plt.ylabel('Fat (g)', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('viz5_scatter_cuisine.png', dpi=300, bbox_inches='tight')
print("Saved: viz5_scatter_cuisine.png")
plt.show()

print("\n" + "="*50)
print("ANALYSIS COMPLETE!")
print("="*50)
print(f"Completed at: {datetime.now()}")
Step 4: Run the Analysis
bashpython3 data_analysis.py
Take screenshots showing:

The terminal output with date/time visible
Each visualization as it appears
The processed_diets.csv file

Step 5: Commit to GitHub
bashgit add data_analysis.py \*.png processed_diets.csv
git commit -m "Person 1: Completed Task 1 - Data Analysis"
git push origin main
