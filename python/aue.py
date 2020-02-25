import pandas as pd
import numpy as np 
import csv
import os
from aue_calcs import all_trees

if not os.path.exists('output'):
    os.makedirs('output')

# Read pair-wise intersection data
path = "data/intersection.csv"
intersections = pd.read_csv(path).sort_values(by=['t1', 't2'])
converse = intersections.rename(columns={'t1':'t2','t2':'t1'})
intersections_all = intersections.append(converse)
print("Loaded intersection data and appended with converse")

# Pivot intersection table to create matrix
print("Pivoting to create possibility matrix...")
p_df = intersections_all.pivot(index='t2', columns='t1', values='intersection')

# Create BBL-Index lookup, as well as BBL set for tree-creation
bbl_list = list(p_df.index.values)
bbl_lookup = {}
for idx, bbl in enumerate(bbl_list):
    bbl_lookup[idx] = bbl

bbl_set = set(bbl_list)
bbl_index_set = set(bbl_lookup.keys())
print("Number of unique input BBLs: ", len(bbl_set))

# Convert to numpy array and set diagonals to nan
p = p_df.to_numpy()
np.fill_diagonal(p, np.nan)
print("Top left corner of possibility matrix: \n", p[0:12,0:12])

# Check that there are only NAN on the diagonal
check = np.full(p.shape, False, dtype=bool)
np.fill_diagonal(check, True)
print("Check for complete intersection data: ", np.array_equal(np.isnan(p), check))

# Find trees
print("Finding trees...")
results = all_trees(bbl_index_set, p)
print("Complete. Number of trees created: ", len(results))


# Find best- and worst-case scenarios
best = max(item['number'] for item in results)
print("Max number of units is %d" % best)
best_subset = list(filter(lambda d: d['number'] == best, results))
best_lots = np.array([list(d['lots_idx']) for d in best_subset])
best_lots = np.vectorize(bbl_lookup.__getitem__)(best_lots).astype(int)
np.savetxt('output/best.csv', best_lots, delimiter=",", fmt='%d')


worst = min(item['number'] for item in results)
print("Min number of units is %d" % worst)
worst_subset = list(filter(lambda d: d['number'] == worst, results))
worst_lots = np.array([list(d['lots_idx']) for d in worst_subset])
worst_lots = np.vectorize(bbl_lookup.__getitem__)(worst_lots).astype(int)
np.savetxt('output/worst.csv', worst_lots, delimiter=",", fmt='%d')
