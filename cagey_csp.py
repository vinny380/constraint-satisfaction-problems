import itertools


# 
# =============================
# Student Names: Vinicius Porfirio Purgato, Adam Clarke, Isaac Wood
# Group ID: (A1) 60
# Date: 
# =============================
# CISC 352 - W24
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
# from propagators import *
from heuristics import *

def binary_ne_grid(cagey_grid):
    #IMPLEMENT

    grid_size, grid = cagey_grid 
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
    #IMPLEMENT
    vars = []
    size, grid = cagey_grid

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
    #NOTE Cage_op(12:?:[Var-Cell(1,1), Var-Cell(1,2)])
    size, grid = cagey_grid
    domain = list(range(1, size+1))
    operations_domain = ['?', '+', '-', '*', '/']
    csp, vars = nary_ad_grid(cagey_grid) # get initial constraints and variables
    
    
    for cage in grid:
        operation_variables = []
        target, variables, operation = cage
        cell_variable = Variable(f"Cage_op({target}:{operation}:[{', '.join([f'Var-Cell({x},{y})' for x, y in variables])}])", operations_domain)
        variable_name = cell_variable.name
        print(variable_name)
        operation_variables.append(cell_variable)
        csp.add_var(cell_variable)

        # scope = [variable for variable in operation if variable == variable_name]
        sat_tuples = get_op_sat_tuples(target, variables, operation, domain)
        print(f"Target: {target}\nValid tuples: {sat_tuples}\n Operation:{operation}\n")
        # we have tuple indices from cage, use that to get appropriate variables
        var_objects = get_var_objects_from_index_tuples(vars, variables)
        constraint = Constraint(f"Constraint_target:{target}, variables:{variables}, operation: {operation}", var_objects)
        constraint.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(constraint)
    
    return csp, vars
        



def get_var_objects_from_index_tuples(var_objects, index_tuples):
    found_var_objects = []
    # find out which objects are relevant
    for var_object in var_objects:
        for index_tuple in index_tuples:
            var_name = var_object.name
            # grab numbers from strings to compare coordinates
            idx_str = ''
            for char in var_name:
                if char.isdigit():
                    idx_str += char
            # compare coordinates
            if int(idx_str[0]) == index_tuple[0] and int(idx_str[1]) == index_tuple[1]:
                found_var_objects.append(var_object)
    return found_var_objects



def get_op_sat_tuples(target, variables, operation, domain):
    if len(variables) == 1:
        return [(target,)]
    
    if operation=='+':
        return get_add_sat_tuples(target, variables, domain)
    elif operation == '-':
        return get_sub_sat_tuples(target, variables, domain)
    elif operation == '/':
        return get_div_sat_tuples(target, variables, domain)
    elif operation == '*':
        return get_mult_sat_tuples(target, variables, domain)
    elif operation == '?':
        return get_question_sat_tuples(target, variables, domain)



def get_add_sat_tuples(target, variables, domain):
    # come up with valid solutions
    all_totals = list(itertools.product(domain, repeat = len(variables)))
    valid_tuples = []
    for t in all_totals:
        if sum(list(t)) == target:
            valid_tuples.append(t)
    # print(f"Target: {target}\nValid tuples: {valid_tuples}\n")
    valid_tuples=list(dict.fromkeys(valid_tuples))
    return valid_tuples

    
def get_sub_sat_tuples(target, variables, domain):
    all_tuples = list(itertools.product(domain, repeat = len(variables)))
    valid_tuples = []
    
    for tup in all_tuples:
        sub = tup[0]
        for i in range(1,len(tup)):
            sub-=tup[i]
        if sub == int(target):
            valid_tuples.append(tup)
    valid_tuples=list(dict.fromkeys(valid_tuples))
    return valid_tuples


def get_mult_sat_tuples(target, variables, domain):
    all_tuples = list(itertools.product(domain, repeat = len(variables)))
    valid_tuples = []
    for tup in all_tuples:
        product = 1
        for num in tup:
            product*=num

        if product == int(target):
            valid_tuples.append(tup)
    valid_tuples=list(dict.fromkeys(valid_tuples))
    return valid_tuples


def get_div_sat_tuples(target, variables, domain):
    all_tuples = list(itertools.product(domain, repeat = len(variables)))
    valid_tuples = []
    
    for tup in all_tuples:
        quotient = tup[0]
        for i in range(1,len(tup)):
            quotient/=tup[i]
        if quotient == int(target):
            valid_tups = list(itertools.permutations(tup, len(tup)))
            valid_tuples.extend(valid_tups)

    valid_tuples=list(dict.fromkeys(valid_tuples))
    return valid_tuples

def get_question_sat_tuples(target, variables, domain):    

    summy = get_add_sat_tuples(target, variables, domain)
    diffy = get_sub_sat_tuples(target, variables, domain)
    divvy = get_div_sat_tuples(target, variables, domain)
    multy = get_sub_sat_tuples(target, variables, domain)
    
    return summy+diffy+divvy+multy