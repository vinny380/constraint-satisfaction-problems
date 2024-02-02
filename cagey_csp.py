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
    
    
    for grid_element in grid:
        operation_variables = []
        target, variables, operation = grid_element
        cell_variable = Variable(f"Cage_op({target}:{operation}:{', '.join([f'Var-Cell({x},{y})' for x, y in variables])})", operations_domain)
        variable_name = cell_variable.name
        operation_variables.append(cell_variable)
        csp.add_var(cell_variable)

        scope = [variable for variable in operation if variable == variable_name]
        sat_tuples = get_op_sat_tuples(target, variables, operation, domain)
        constraint = Constraint(f"Constraint_target:{target}, variables:{variables}, operation: {operation}", scope)
        constraint.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(constraint)
        



def get_op_sat_tuples(target, variables, operation, domain):
    x = 5
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
    all_totals = list(itertools.permutations(domain, len(variables)))
    valid_tuples = []
    for t in all_totals:
        if sum(list(t)) == target:
            valid_tuples.append(t)
    print(f"Target= {target},\nValid tuples: {valid_tuples}\n")

    return valid_tuples

    
def get_sub_sat_tuples(target, variables, domain):
    all_tuples = list(itertools.permutations(domain, len(variables)))
    valid_tuples = []
    
    for tup in all_tuples:
        sub = tup[0]
        for i in range(1,len(tup)):
            sub-=tup[i]
        if sub == int(target):
            valid_tuples.append(tup)

    return valid_tuples

            
def get_mult_sat_tuples(target, variables, domain):
    all_tuples = list(itertools.permutations(domain, len(variables)))
    valid_tuples = []
    for tup in all_tuples:
        product = 1
        for num in tup:
            product*=num

        if product == int(target):
            valid_tuples.append(tup)

    return valid_tuples


def get_div_sat_tuples(target, variables, domain):
    all_tuples = list(itertools.permutations(domain, len(variables)))
    valid_tuples = []
    
    for tup in all_tuples:
        quotient = tup[0]
        for i in range(1,len(tup)):
            quotient/=tup[i]
        if quotient == int(target):
            valid_tuples.append(tup)

    return valid_tuples

def get_question_sat_tuples(target, variables, domain):    
    summy = get_add_sat_tuples(target, variables, domain)
    diffy = get_sub_sat_tuples(target, variables, domain)
    divvy = get_div_sat_tuples(target, variables, domain)
    multy = get_sub_sat_tuples(target, variables, domain)

    return summy+diffy+divvy+multy



cagey_csp_model(b)