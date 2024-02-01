import itertools


# 
# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
b
'''

from cspbase import *
# from propagators import *
from heuristics import *


b = (6, [(11, [(1, 1), (2, 1)], '+'), (3, [(1, 2), (2, 2)], '*'), (20, [(1, 3), (2, 3), (3, 3)], '*'),
        (2, [(1, 4), (1, 5)], '-'), (6, [(1, 6), (2, 6)], '/'), (6, [(2, 4), (2, 5)], '*'),
        (5, [(3, 1), (4, 1)], '+'), (40, [(3, 2), (4, 2), (5, 2)], '*'), (10, [(3, 4), (4, 4)], '+'),
        (10, [(3, 5), (3, 6)], '*'), (3, [(4, 3), (5, 3)], '-'), (8, [(4, 5), (4, 6), (5, 6)], '+'),
        (1, [(5, 1), (6, 1), (6, 2)], '-'), (11, [(5, 4), (5, 5)], '+'), (1, [(6, 3), (6, 4)], '-'),
        (2, [(6, 5), (6, 6)], '-')])

b2 = (3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

def binary_ne_grid(cagey_grid):
    grid_size, grid = cagey_grid  # Unpack the size from the board definition
    domain = list(range(1, grid_size + 1))
    
    vars = []
    constraints = []
    for row_index in range(grid_size):
        for col_index in range(grid_size):
            var_name = f"Cell({row_index+1},{col_index+1})"
            variable = Variable(var_name, domain)
            vars.append(variable)


    # Initialize the CSP for the Cagey grid
    csp = CSP("binary_ne_grid", vars)
    satisfiable_tuples = list(itertools.permutations(domain, 2))

    # Generate and add binary not-equal constraints for rows and columns
    for base_row in range(grid_size):
        # Generate row constraints
        row_indices = [base_row * grid_size + i for i in range(grid_size)]
        for cell1_index, cell2_index in itertools.combinations(row_indices, 2):
            constraint_name = f"NE_{vars[cell1_index].name}_X_{vars[cell2_index].name}"
            constraint = Constraint(constraint_name, [vars[cell1_index], vars[cell2_index]])
            constraints.append(constraint)

        
        # Generate column constraints
        col_indices = [i * grid_size + base_row for i in range(grid_size)]
        for cell1_index, cell2_index in itertools.combinations(col_indices, 2):
            constraint_name = f"NE_{vars[cell1_index].name}_X_{vars[cell2_index].name}"
            constraint = Constraint(constraint_name, [vars[cell1_index], vars[cell2_index]])
            constraints.append(constraint)
    
    for constraint in constraints:
        constraint.add_satisfying_tuples(satisfiable_tuples)
        csp.add_constraint(constraint)

    return csp, vars


def nary_ad_grid(cagey_grid):
    ## IMPLEMENT
    pass

def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
    pass







#_____________________________HELPER FUNCTIONS_____________________________
def get_relevant_row(row, variables):
    relevant_variables = []
    for variable in variables:
        # Cell(6, 4)
        x = int(variable.name[5]) # 6
        y = int(variable.name[7]) # 4
        # add all elements in same row
        if x == row+1: # i 0 based, n is not
            relevant_variables.append(variable)

    unsorted = [(v, y) for v in relevant_variables]
    sorted_vars = sorted(unsorted, key=lambda x: x[1])
    relevant_variables = [f[0] for f in sorted_vars]

    return relevant_variables

def get_relevant_col(col, variables):
    relevant_variables = []
    for variable in variables:
        # Var-Cell(6, 4)
        x = int(variable.name[5]) # 6
        y = int(variable.name[7]) # 4
        if y == col+1: # i 0 based, n is not
            relevant_variables.append(variable)
    unsorted = [(v, x) for v in relevant_variables]
    sorted_variables = sorted(unsorted, key=lambda x: x[1])
    relevant_variables = [f[0] for f in sorted_variables]

    return relevant_variables






binary_ne_grid(b2)