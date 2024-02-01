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

   # Add binary not-equal constraints for each row and column
    for current_row in range(grid_size):
        for current_col in range(grid_size):
            # Row constraints
            for comparing_cell in range(current_col + 1, grid_size):
                row_constraint = Constraint(f"Row{current_row+1}_Cell{current_col+1}_NE_Cell{comparing_cell+1}", [vars[current_row*grid_size + current_col], vars[current_row*grid_size + comparing_cell]])
                constraints.append(row_constraint)

            # Column constraints
            for comparing_cell in range(current_row + 1, grid_size):
                col_constraint = Constraint(f"Col{current_col+1}_Cell{current_row+1}_NE_Cell{comparing_cell+1}", [vars[current_row*grid_size + current_col], vars[comparing_cell*grid_size + current_col]])
                constraints.append(col_constraint)


    #add satisfiable tuple to each constraint, and push it to the csp.
    for constraint in constraints:
        constraint.add_satisfying_tuples(satisfiable_tuples)
        csp.add_constraint(constraint)

    return csp, vars


def nary_ad_grid(cagey_grid):
    # Create n^n variables
    vars = []
    size, grid = cagey_grid  # Unpack the size from the board definition

    domain = list(range(1, size + 1))

    for row in range(size):
        for column in range(size):
            cell_variable = Variable(f"Cell({str(row+1)},{str(column+1)})", domain)
            vars.append(cell_variable)

    constraints = []
    satisfying_tuples = list(itertools.permutations(domain, r = size))

    # add rows
    for i in range(size):
        # scope = get_relevant_row(i, vars)
        scope = [variable for variable in vars if int(variable.name.split('(')[1].split(',')[1].rstrip(')')) == i+1]
        constraint = Constraint(f"Row{i+1}", scope)
        constraint.add_satisfying_tuples(satisfying_tuples)
        constraints.append(constraint)

    # add columns
    for i in range(size):
        scope = [variable for variable in vars if int(variable.name.split('(')[1].split(',')[0]) == i+1]
        constraint = Constraint(f"Col{i+1}", scope)
        constraint.add_satisfying_tuples(satisfying_tuples)
        constraints.append(constraint)

        
    csp = CSP('nary_ad_grid', vars)
    for constraint in constraints:
        csp.add_constraint(constraint)

    return csp, vars



def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
    pass