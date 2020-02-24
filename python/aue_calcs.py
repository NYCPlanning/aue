import numpy as np

def find_next(branch_set, p):
    possible_children = np.repeat(1, p.shape[0])
    for i in branch_set:
        possible_children = np.multiply(possible_children, p[i-1])
    try:
        branch_set.add(possible_children.tolist().index(1)+1)
    except:
        pass
    return branch_set, possible_children

def make_tree(seed, p):
    possible_children = np.repeat(1, p.shape[0])
    branch_set = {seed}
    while np.nansum(possible_children) > 0:
        branch_set, possible_children = find_next(branch_set, p)
    max_branch = len(branch_set)
    return branch_set, max_branch

def all_trees(bbl_set, p):
    results = []
    while len(bbl_set) > 0:
        seed = bbl_set.pop()
        branch_set, max_branch = make_tree(seed, p)
        results.append({'lots':branch_set, 'number':max_branch})
        bbl_set = bbl_set - branch_set
    return results

if __name__ == '__main__':
    print("===== Example calculation =====\n")
    p = np.array([[np.nan,0,1,1],[0,np.nan,0,1],[1,0,np.nan,1],[1,0,1,np.nan]])
    bbl_set = {1,2,3,4}
    print("Example buffer matrix:\n", p)
    print("Example set of BBL indices:\n", bbl_set)
    results = all_trees(bbl_set, p)
    print("Example results:\n", all_trees)
    print("The best-case scenario is: \n", max(item['number'] for item in results), " establishments")
    print("The worst-case scenario is: \n", min(item['number'] for item in results), " establishments")