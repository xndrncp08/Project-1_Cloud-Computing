import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

print(f"Analysis run at: {datetime.now()}")

# Load dataset
df = pd.read_csv("All_Diets.csv")
print(f"Dataset shape: {df.shape}")
print(df.head())

# ===== DATA CLEANING =====
print("\nDATA CLEANING")
numeric_columns = ['Protein(g)','Carbs(g)','Fat(g)']
for col in numeric_columns:
    if df[col].isnull().any():
        df[col].fillna(df[col].mean(), inplace=True)
        print(f"Filled missing values in {col}")

# ===== ANALYSIS 1: Average Macronutrients by Diet Type =====
avg_macros = df.groupby('Diet_type')[['Protein(g)','Carbs(g)','Fat(g)']].mean()
print("\nAverage macronutrients per diet type:\n", avg_macros)

# ===== ANALYSIS 2: Top 5 Protein Recipes per Diet Type =====
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
print("\nTop protein recipes:\n", top_protein[['Diet_type','Recipe_name','Protein(g)']])

# ===== ANALYSIS 3: Diet Type with Highest Protein =====
highest_protein_diet = avg_macros['Protein(g)'].idxmax()
highest_protein_value = avg_macros['Protein(g)'].max()
print(f"\nHighest protein diet: {highest_protein_diet} ({highest_protein_value}g)")

# ===== ANALYSIS 4: Most Common Cuisines =====
most_common_cuisines = df.groupby('Diet_type')['Cuisine_type'].agg(lambda x: x.mode()[0])
print("\nMost common cuisine per diet type:\n", most_common_cuisines)

# ===== ANALYSIS 5: New Metrics =====
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)'].replace(0,np.nan)
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)'].replace(0,np.nan)
print("\nNew metrics added (Protein_to_Carbs_ratio, Carbs_to_Fat_ratio)")
print(df.head())

# Save processed data
df.to_csv("output/processed_diets.csv", index=False)
print("\nProcessed data saved to output/processed_diets.csv")

# ===== VISUALIZATIONS =====
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10,5)

# Average protein by diet type
plt.figure()
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'], palette='viridis')
plt.title(f'Average Protein by Diet Type - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
plt.xlabel('Diet Type')
plt.ylabel('Protein (g)')
plt.tight_layout()
plt.savefig("output/viz_avg_protein.png")
plt.close()

# All macronutrients by diet type
avg_macros_reset = avg_macros.reset_index()
avg_macros_melted = avg_macros_reset.melt(id_vars='Diet_type', value_vars=['Protein(g)','Carbs(g)','Fat(g)'], var_name='Macronutrient', value_name='Average (g)')
plt.figure()
sns.barplot(data=avg_macros_melted, x='Diet_type', y='Average (g)', hue='Macronutrient', palette='Set2')
plt.title(f'Average Macronutrients by Diet Type - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
plt.tight_layout()
plt.savefig("output/viz_all_macros.png")
plt.close()

print("\nANALYSIS COMPLETE!")
