# Ericsson Cui 
# 2024/6/20 
# Linear Equation Solver
# The program is only used for add/subtract and no multiply/divide
# Best to not leave un-simplified equation

def split_by_plus_or_minus(string):
    term = [] 
    string = ''.join([char if char != ' ' else '' for char in string ])

    for char_ind in range(len(string)):
        if string[char_ind] in ('+', '-'):
            if char_ind == 0: # First term is negative
                end_ind = [ind+1 for ind in range(len(string[1:])) if string[ind+1] in ('+', '-')]
                if len(end_ind) > 0:
                    end_ind = end_ind[0] 
                    term += [string[:end_ind]]
                    term += [string[end_ind:]] 
                else:
                    term += [str(string)]
            else:
                term += [string[:char_ind]] 
                term += [string[char_ind:]]
            break 
     
    if len(term) > 0:
        return term 
    return [string]
    
def isInteger(string):
    try:
        int(string)
        return True 
    except ValueError:
        return False 

def solve_linear_equation(input_expression: str):
    # Add necessary symbols to conduct multiplication and division 
    expression = ""
    for char_ind in range(len(input_expression)):

        if input_expression[char_ind] == 'x':
            phase_expression = ''
            
            if char_ind == 0:
                expression += '1*x'
            
            else:
                if input_expression[char_ind - 1] != '*':
                    phase_expression += '*x'
                    
            expression += phase_expression
      
        else:
            expression += input_expression[char_ind] 
            
    print(f"expression: {expression}") 
    
    left_side, right_side = expression.split("=")
    
    left_side = split_by_plus_or_minus(left_side)
    right_side = split_by_plus_or_minus(right_side)

    # Prevent index position error for later 
    if len(left_side) > len(right_side):
        right_side = right_side + ['0'] * (len(left_side) - len(right_side)) 
    elif len(right_side) > len(left_side):
        left_side = left_side + ['0'] * (len(right_side) - len(left_side))   
    
    print(f"Before: {left_side} = {right_side}")
    
    # Sort numeric values to one side and x to the other 
    for elem_ind in range(max(len(left_side), len(right_side))):
        # left_side for all the unknowns 
        # right_side for all numeric values 
        if 'x' in right_side[elem_ind]:
            
            # find the numeric value on left side -> element without 'x'
            left_numeric_ind = [ind for ind in range(len(left_side)) if 'x' not in left_side[ind]][0] 
            
            # Switching signs(+/-) when switching sides 
            left_numeric_val = -1 * int(left_side[left_numeric_ind]) 
            right_side_x_coefficient = [right_side[ind][:-2] for ind in range(len(right_side)) if 'x' in right_side[ind]]
            right_side_unknown = str(-1 * int(right_side_x_coefficient[0])) + '*x'

            right_side[elem_ind], left_side[left_numeric_ind] = str(left_numeric_val), right_side_unknown
            
    print(f"After: {left_side} = {right_side}")
    
    # Combine unknown(x) coefficients 
    combined_coefficients = sum([int(coef[:-2]) for coef in left_side])
    combined_right_side = sum([int(num) for num in right_side]) 
    unknown_val = combined_right_side / combined_coefficients 
    print(f"Sol: x = {combined_right_side} / {combined_coefficients}\n     x = {unknown_val:.2f}")

# Main code 
while True:
    equation = input("Enter your linear algebra equation(q: quit): ")
    if equation.lower() == 'q':
        break 
    else:
        solve_linear_equation(equation)


