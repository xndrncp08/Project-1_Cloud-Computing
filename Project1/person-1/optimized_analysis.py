import pandas as pd
import numpy as np
import time
from datetime import datetime

print(f"\nOptimization test started at: {datetime.now()}")

# Load dataset
df = pd.read_csv("All_Diets.csv")

# Ensure numeric columns
numeric_cols = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# =============================
# ORIGINAL METHOD
# =============================
start_time = time.time()

avg_macros_old = df.groupby('Diet_type')[numeric_cols].mean()

top_protein_old = (
    df.sort_values('Protein(g)', ascending=False)
      .groupby('Diet_type')
      .head(5)
)

original_time = time.time() - start_time
print(f"\nOriginal method time: {original_time:.6f} seconds")

# =============================
# OPTIMIZED METHOD
# =============================
start_time = time.time()

# Optimization 1: Convert to categorical
df['Diet_type'] = df['Diet_type'].astype('category')
df['Cuisine_type'] = df['Cuisine_type'].astype('category')

# Optimization 2: Vectorized ratio calculations
df['Protein_to_Carbs_ratio'] = np.where(
    df['Carbs(g)'] != 0,
    df['Protein(g)'] / df['Carbs(g)'],
    np.nan
)

df['Carbs_to_Fat_ratio'] = np.where(
    df['Fat(g)'] != 0,
    df['Carbs(g)'] / df['Fat(g)'],
    np.nan
)

# Optimization 3: Efficient aggregation
avg_macros_new = df.groupby('Diet_type', observed=True).agg({
    'Protein(g)': 'mean',
    'Carbs(g)': 'mean',
    'Fat(g)': 'mean'
})

# Optimization 4: Use nlargest instead of full sort
top_protein_new = (
    df.groupby('Diet_type', observed=True)
      .apply(lambda x: x.nlargest(5, 'Protein(g)'))
      .reset_index(drop=True)
)

optimized_time = time.time() - start_time
print(f"Optimized method time: {optimized_time:.6f} seconds")

# =============================
# PERFORMANCE RESULTS
# =============================
if optimized_time > 0:
    improvement = ((original_time - optimized_time) / original_time) * 100
    speed_factor = original_time / optimized_time
else:
    improvement = 0
    speed_factor = 1

print(f"\nPerformance improvement: {improvement:.2f}%")
print(f"Speed increase: {speed_factor:.2f}x faster")

print(f"\nOptimization test completed at: {datetime.now()}")