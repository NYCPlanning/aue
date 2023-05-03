import pandas as pd
import numpy as np
import os
from pathlib import Path
from python.aue_calcs import all_trees

VERSION = os.environ.get("INPUT_VERSION")
OUTPUT_FOLDER_VERSIONED = f"output/{VERSION}"

def model(dbt, session) -> pd.DataFrame:
    # Read pair-wise intersection data
    # intersections_all = pd.read_csv(path).sort_values(by=['t1', 't2'])
    intersections_all = dbt.ref("buffered_lot_intersections").sort_values(by=['t1', 't2'])

    print("Loaded intersection data")
    print(intersections_all.shape)

    # Pivot intersection table to create matrix
    print("Pivoting to create possibility matrix...")
    p_df = intersections_all.pivot(index='t1', columns='t2', values='intersection')
    print(p_df.shape)

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

    # Checks for intersection data
    check = np.full(p.shape, False, dtype=bool)
    np.fill_diagonal(check, True)
    print("Check for complete intersection data: ", np.array_equal(np.isnan(p), check))

    # Find graphs
    print("Finding graphs...")
    results = all_trees(bbl_index_set, p)
    print("Complete. Number of graphs created: ", len(results))

    aue_graphs = pd.DataFrame.from_records(results)

    # NOTE exporting outputs as csvs rather than tables
    # creating output file directory
    Path(OUTPUT_FOLDER_VERSIONED).mkdir(parents=True, exist_ok=True)

    ### Find best- and worst-case scenarios ###
    best = max(item['number'] for item in results)
    print("Max number of units is %d" % best)

    # Find the subset of arrangements for best-case
    best_subset = list(filter(lambda d: d['number'] == best, results))
    best_lots = [list(d['lots_idx']) for d in best_subset]

    # Remove permutations
    best_no_perms = set(map(lambda x: tuple(sorted(x)),best_lots))
    best_lots = np.vectorize(bbl_lookup.__getitem__)(np.array(list(best_no_perms)).transpose()).astype(int)
    header = ','.join("combo_" + str(i+1) for i in range(best_lots.shape[1]))
    print(header)
    np.savetxt(f'{OUTPUT_FOLDER_VERSIONED}/best.csv', best_lots, header=header, comments='', delimiter=",", fmt='%d')

    worst = min(item['number'] for item in results)
    print("Min number of units is %d" % worst)

    # Find the subset of arrangements for worst-case
    worst_subset = list(filter(lambda d: d['number'] == worst, results))
    worst_lots = [list(d['lots_idx']) for d in worst_subset]

    # Remove permutations
    worst_no_perms = set(map(lambda x: tuple(sorted(x)),worst_lots))
    worst_lots = np.vectorize(bbl_lookup.__getitem__)(np.array(list(worst_no_perms)).transpose()).astype(int)
    header = ','.join("combo_" + str(i+1) for i in range(worst_lots.shape[1]))
    print(header)
    np.savetxt(f'{OUTPUT_FOLDER_VERSIONED}/worst.csv', worst_lots, header=header, comments='', delimiter=",", fmt='%d')


    return aue_graphs