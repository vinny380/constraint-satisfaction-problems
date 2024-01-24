# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic '''
    # IMPLEMENT

    max_degree_var = None

    for var in csp.get_all_unasgn_vars:
        degree = 0
        for constraint in csp.get_cons_with_var:
            if constraint.get_n_unasgn() > 1:
                degree += 1
        if degree > max_degree:
            max_degree = degree
            var_with_max_degree = var

    return var_with_max_degree

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT
    min_domain_size = int('-inf')
    min_var = None

    for var in csp.get_all_unasgn_vars:
        domain_size = var.cur_domain_size()
        
        if domain_size <= min_domain_size:
            min_domain_size = domain_size
            min_var = var

    return min_var
