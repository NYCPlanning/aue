import numpy as np

def find_next(branch_set, p):
    '''
    For a given set of lots already containing
    establishments, finds the lots where it
    is possible to place the next establisment.

    In this case, lots are referred to by index.
    Current extablishment lot indices are stored in 
    branch_set.

    Parameters
    ----------
    branch_set: set
        Contains indices of lots where an establishment
        has already been hypothetically placed.
    p: numpy 2D array
        nXn array, 0 for lots that are too close,
        1 for lots that aren't, and null on diagonal

    Returns
    -------
    branch_set: set
        Same as input branch set, but with new children added
    possible_children: numpy 1D array
        Contains 1 for possible next lots, 0 for ones that
        are too close to existing lots, and null for lots
        already "visited"
    '''
    # Initialize all next steps as possible
    possible_children = np.repeat(1, p.shape[0])
    for i in branch_set:
        # Find next possible based on proximity to all previous
        possible_children = np.multiply(possible_children, p[i])
    try:
        # Add the first possible next step to the list
        branch_set.add(possible_children.tolist().index(1))
    except:
        pass
    return branch_set, possible_children

def make_tree(seed, p):
    '''
    Starts by placing an establishment
    on the seed lot, then iteratively calls
    find_next to add establishments. Continues
    this process until there are no more possible
    establishments to add.

    Parameters
    ----------
    seed: int
        Index of the first lot to assign to an establishment
    p: numpy 2D array
        nXn array, 0 for lots that are too close,
        1 for lots that aren't, and null on diagonal

    Returns
    -------
    branch_set: set
        Contains the indices of all of the lots that can simultaneously
        have establishments, given the seed lot
    max_branch: int
        Number of lots that can have establishments given this seed
    '''
    # Initialize all next steps as possible
    possible_children = np.repeat(1, p.shape[0])
    branch_set = {seed}
    # Find possible next lot until there are no more possible
    while np.nansum(possible_children) > 0:
        branch_set, possible_children = find_next(branch_set, p)
    # Calculate number of lots assigned
    max_branch = len(branch_set)
    return branch_set, max_branch

def all_trees(bbl_set, p):
    '''
    Given a set of lot indices and the associated possibility
    matrix, finds all possible arrangements.

    Parameters
    ----------
    bbl_set: set
        Set of all input BBLs -- indexes
    p: numpy 2D array
        nXn array, 0 for lots that are too close,
        1 for lots that aren't, and null on diagonal

    Returns
    -------
    results: list of dicts
        Each record is a possible arrangement of establishments
        The dictionaries have the following:
             'lots_idx', contining the indices of lots assigned to 
                            establishments, 
             'number', containing the integer count of lots with
                            establishments for this arrangement
    '''
    results = []
    # Run algorithm on new seeds until all have been used
    while len(bbl_set) > 0:
        seed = bbl_set.pop()
        branch_set, max_branch = make_tree(seed, p)
        results.append({'lots_idx':branch_set, 'number':max_branch})
        bbl_set = bbl_set - branch_set
    return results

if __name__ == '__main__':
    print("===== Example calculation =====\n")
    p = np.array([[np.nan,0,1,1],[0,np.nan,0,1],[1,0,np.nan,1],[1,1,1,np.nan]])
    bbl_set = {1,2,3,4}
    print("Example buffer matrix:\n", p)
    print("Example set of BBL indices:\n", bbl_set)
    results = all_trees(bbl_set, p)
    print("Example results:\n", all_trees)
    print("The best-case scenario is: \n", max(item['number'] for item in results), " establishments")
    print("The worst-case scenario is: \n", min(item['number'] for item in results), " establishments")