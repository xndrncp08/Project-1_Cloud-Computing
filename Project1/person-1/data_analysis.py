# Use non-GUI backend (fixes Tkinter error)
import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

print(f"\nAnalysis run at: {datetime.now()}\n")

# -----------------------------
# LOAD DATA
# -----------------------------
print("Loading dataset...")
df = pd.read_csv("All_Diets.csv")

print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

# -----------------------------
# DATA CLEANING
# -----------------------------
print("\nChecking missing values before cleaning:")
print(df.isnull().sum())

numeric_cols = ["Protein(g)", "Carbs(g)", "Fat(g)"]

# Convert to numeric safely
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Fill missing values with column mean
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# -----------------------------
# ANALYSIS 1: Average Macronutrients
# -----------------------------
avg_macros = df.groupby("Diet_type")[numeric_cols].mean()

print("\nAverage macronutrients per diet type:")
print(avg_macros)

# -----------------------------
# ANALYSIS 2: Top 5 Protein Recipes per Diet
# -----------------------------
top_protein = (
    df.sort_values("Protein(g)", ascending=False)
      .groupby("Diet_type")
      .head(5)
)

print("\nTop 5 Protein-rich Recipes per Diet:")
print(top_protein[["Diet_type", "Recipe_name", "Protein(g)"]].to_string(index=False))

# -----------------------------
# ANALYSIS 3: Diet with Highest Protein
# -----------------------------
highest_protein_diet = avg_macros["Protein(g)"].idxmax()
highest_value = avg_macros["Protein(g)"].max()

print(f"\nDiet with highest average protein: {highest_protein_diet}")
print(f"Average protein content: {highest_value:.2f} g")

# -----------------------------
# ANALYSIS 4: Most Common Cuisine per Diet
# -----------------------------
most_common_cuisine = (
    df.groupby("Diet_type")["Cuisine_type"]
      .agg(lambda x: x.mode()[0] if len(x.mode()) > 0 else "N/A")
)

print("\nMost common cuisine per diet type:")
print(most_common_cuisine)

# -----------------------------
# ANALYSIS 5: New Metrics
# -----------------------------
df["Protein_to_Carbs_ratio"] = df["Protein(g)"] / df["Carbs(g)"].replace(0, np.nan)
df["Carbs_to_Fat_ratio"] = df["Carbs(g)"] / df["Fat(g)"].replace(0, np.nan)

print("\nNew metrics added (sample):")
print(df[["Recipe_name", "Protein_to_Carbs_ratio", "Carbs_to_Fat_ratio"]].head())

# Save processed dataset
df.to_csv("processed_diets.csv", index=False)
print("\nProcessed data saved to processed_diets.csv")

# -----------------------------
# VISUALIZATIONS
# -----------------------------
sns.set_style("whitegrid")

# 1️⃣ Bar Chart - Average Protein by Diet Type
plt.figure(figsize=(12,6))
sns.barplot(x=avg_macros.index, y=avg_macros["Protein(g)"])
plt.xticks(rotation=45, ha="right")
plt.title(f"Average Protein by Diet Type\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
plt.ylabel("Average Protein (g)")
plt.tight_layout()
plt.savefig("viz1_avg_protein.png", dpi=300)
plt.close()

# 2️⃣ Heatmap - Macronutrients by Diet Type
plt.figure(figsize=(10,6))
sns.heatmap(avg_macros, annot=True, fmt=".2f", cmap="YlOrRd")
plt.title("Heatmap of Macronutrients by Diet Type")
plt.tight_layout()
plt.savefig("viz2_heatmap.png", dpi=300)
plt.close()

# 3️⃣ Scatter Plot - Top Protein Recipes
plt.figure(figsize=(12,6))
sns.scatterplot(
    data=top_protein,
    x="Protein(g)",
    y="Carbs(g)",
    hue="Diet_type",
    size="Fat(g)",
    sizes=(50, 400),
    alpha=0.7
)
plt.title("Top 5 Protein-Rich Recipes Distribution")
plt.tight_layout()
plt.savefig("viz3_scatter.png", dpi=300)
plt.close()

print("\nANALYSIS COMPLETE.")
print(f"Completed at: {datetime.now()}")