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
check = numpy.full(p.shape, False, dtype=bool)
np.fill_diagonal(check, True)
print("Is there missing intersection data? ", np.array_equal(np.isnan(p), check))

# Find trees
print("Finding trees...")
results = all_trees(bbl_index_set, p)
print("Complete.")

# Convert indecies back to BBLs
def bbl_from_idx(result_dict):
    result_dict['bbls'] = [bbl_lookup[idx] for idx in list(result_dict['lots_idx'])]

map(bbl_from_idx, results)

# Find best- and worst-case scenarios
best = max(item['number'] for item in results)
print("Max number of units is %d" % best)
best_subset = list(filter(lambda d: d['number'] == best, results))
best_bbls = [d['bbls'] for d in best_subset]
with open('output/best.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerows(best_bbls)

worst = min(item['number'] for item in results)
print("Min number of units is %d" % worst)
worst_subset = list(filter(lambda d: d['number'] == worst, results))
worst_bbls = [d['bbls'] for d in worst_subset]
with open('output/worst.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerows(worst_bbls)
