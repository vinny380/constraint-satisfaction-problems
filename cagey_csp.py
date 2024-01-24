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
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
from propagators import *
from heuristics import *


b = (6, [(11, [(1, 1), (2, 1)], '+'), (3, [(1, 2), (2, 2)], '*'), (20, [(1, 3), (2, 3), (3, 3)], '*'),
        (2, [(1, 4), (1, 5)], '-'), (6, [(1, 6), (2, 6)], '/'), (6, [(2, 4), (2, 5)], '*'),
        (5, [(3, 1), (4, 1)], '+'), (40, [(3, 2), (4, 2), (5, 2)], '*'), (10, [(3, 4), (4, 4)], '+'),
        (10, [(3, 5), (3, 6)], '*'), (3, [(4, 3), (5, 3)], '-'), (8, [(4, 5), (4, 6), (5, 6)], '+'),
        (1, [(5, 1), (6, 1), (6, 2)], '-'), (11, [(5, 4), (5, 5)], '+'), (1, [(6, 3), (6, 4)], '-'),
        (2, [(6, 5), (6, 6)], '-')])

b2 = (3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

def binary_ne_grid(cagey_grid):
    # Create n^n variables
    vars = []
    size = cagey_grid[0]
    cages = cagey_grid[1]
    domain = [n for n in range(1, size+1)]

    for row in range(size):
        for column in range(size):
            cell_variable = Variable(f"Cell({str(row+1)},{str(column+1)})", domain)
            vars.append(cell_variable)

    constraints = []

    # add rows
    for i in range(size):
        scope = get_relevant_row(i, vars)
        constraint = Constraint(f"Row{i}", scope)
        constraints.append(constraint)

    # add columns
    for i in range(size):
        scope = get_relevant_col(i, vars)
        constraint = Constraint(f"Col{i}", scope)
        constraints.append(constraint)

    satisfying_tuples = itertools.permutations(domain, r = size)

    for constraint in constraints:
        print(constraint)
        constraint.add_satisfying_tuples(satisfying_tuples)
    
    csp = CSP('binary_ne_grid', vars)
    for constraint in constraints:
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
    rel_vars = []
    for v in variables:
        # Cell(6, 4)
        x = int(v.name[5]) # 6
        y = int(v.name[7]) # 4
        # add all elements in same row
        if x == row+1: # i 0 based, n is not
            rel_vars.append(v)

    unsorted = [(v, y) for v in rel_vars]
    sorted_vars = sorted(unsorted, key=lambda x: x[1])
    rel_vars = [f[0] for f in sorted_vars]

    return rel_vars

def get_relevant_col(col, variables):
    rel_vars = []
    for v in variables:
        # Var-Cell(6, 4)
        x = int(v.name[5]) # 6
        y = int(v.name[7]) # 4
        if y == col+1: # i 0 based, n is not
            rel_vars.append(v)
    unsorted = [(v, x) for v in rel_vars]
    sorted_variables = sorted(unsorted, key=lambda x: x[1])
    rel_vars = [f[0] for f in sorted_variables]

    return rel_vars






def main():
    binary_ne_grid(b)

main()
