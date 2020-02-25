import pandas as pd
import numpy as np 
import csv
from aue_calcs import all_trees


# Read pair-wise intersection data
path = "data/intersection.csv"
intersections = pd.read_csv(path).sort_values(by=['t1', 't2'])
converse = intersections.rename(columns={'t1':'t2','t2':'t1'})
intersections_all = intersections.append(converse)
print("Loaded intersection data and appended with converse")

# Create BBL-Index lookup, as well as BBL set for tree-creation
bbl_list = intersections['t1'].unique().tolist()
bbl_lookup = {}
for idx, bbl in enumerate(bbl_list):
    bbl_lookup[idx] = bbl
#TODO: Output bbl_lookup so that results can be mapped back to BBLs for QA
bbl_set = set(bbl_list)
bbl_index_set = set(bbl_lookup.keys())
print("Minimum index: ", min(bbl_index_set))
print("Number of unique input BBLs: ", len(bbl_set))

# Pivot intersection table to create matrix
print("Pivoting to create possibility matrix...")
p_df = intersections_all.pivot(index='t2', columns='t1', values='intersection')

# Convert to numpy array and set diagonals to nan
p = p_df.to_numpy()
np.fill_diagonal(p, np.nan)
print("Top left corner of possibility matrix: \n", p[0:12,0:12])

# Find trees
print("Finding trees...")
results = all_trees(bbl_index_set, p)

# Find best- and worst-case scenarios
best = max(item['number'] for item in results)
print("Max number of units is %d" % best)
#TODO: Output BBL combos associated with best-case scenario
best_bbls = list(filter(lambda d: d['number'] == best, results))
print(best_bbls)

worst = min(item['number'] for item in results)
print("Min number of units is %d" % worst)
#TODO: Output BBL combos associated with worst-case scenario
worst_bbls = list(filter(lambda d: d['number'] == worst, results))
print(worst_bbls)
