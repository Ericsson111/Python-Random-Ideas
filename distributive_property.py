
import os

def clear():
    os.system("cls || clear")

def valid_paranthesis(paranthesis: str) -> bool:
    o1 = "" # open brackets
    c1 = "" # close brackets
    for bracketID in range(len(paranthesis)):
        if paranthesis[bracketID] in ['(', '[', '{']: # If bracket is open 
            o1 += paranthesis[bracketID] 
        elif paranthesis[bracketID] in [')', ']', '}']: # bracket is close 
            c1 += paranthesis[bracketID]
    
    pair = {'(': ')', '[': ']', '{': '}'}
    if paranthesis[:2] not in ['{}', '[]', '()']:
        return ''.join([pair[o] for o in o1])[::-1] == c1
    else:
        return ''.join([pair[o] for o in o1]) == c1

def isInteger(string: str) -> bool:
    try:
        int(string) 
        return True 
    except ValueError:
        return False 

def combining_expression(unknown: str, enclosed_terms: list) -> str:
    # Seperate numeric values with algebraic values 
    unknown_terms = []
    numeric_terms = [] 
    for term in enclosed_terms:
        if unknown not in term:
            numeric_terms.append(term) 
        elif unknown in term:
            # Assign the unknown value with a numeric value (ex: 2)
            # 4x - 2x = 2x 
            # 4*2 - 2*2 = 8 - 4 = 4 
            # x = (4/2) 
            term = term.replace('x', '2')
            unknown_terms.append(term) 
    print(f"enclosed_terms: {enclosed_terms}")
    print(f"unknown_terms: {unknown_terms}")
    print(f"numeric_terms: {numeric_terms}")
    numeric_term = eval(''.join(numeric_terms)) 
    print(f"numeric_term: {numeric_term}")
    simplified_term = eval(str(numeric_term) + ''.join(unknown_terms)) / 2 
    if len(unknown_terms) > 0 or eval(''.join(unknown_terms)) != 0:
        return str(simplified_term) + "*" + unknown
    return str(simplified_term)

def updating_expression(coefficient_and_enclosed_expression, update_expression, update_value):
    for coefficient in coefficient_and_enclosed_expression.keys():
        new_expression = coefficient_and_enclosed_expression[coefficient].replace(update_expression, str(update_value))
        coefficient_and_enclosed_expression[coefficient] = new_expression 
    print(coefficient_and_enclosed_expression)
    return coefficient_and_enclosed_expression

def collecting_like_terms(unknown: str, coefficient_and_enclosed_expression: dict, coefficients: str) -> dict:
    # Multiply coefficient with all terms inside the enclosed expression
    # Begin multiplying from the last item inside the dictionary
    # Replace it's way back in and then simplify the full equation 
    # Collect like terms 
    operations = ['+', '-', '*', '/']
    known_coefficient = ''
    known_enclosed_terms = [] 
    known_enclosed_expression = ''
    
    for coefficient_ind in range(len(coefficient_and_enclosed_expression) - 1, -1, -1):
        coefficient = coefficients[coefficient_ind]
        enclosed_expression = coefficient_and_enclosed_expression[coefficient]
        
        enclosed_terms = [] # term1, term2, term3, ... 
        previous_operation_ind = 0 
        
        print(coefficient, enclosed_expression)
    
        if enclosed_expression.count('(') > 1: 
            # Unknown variable appears
            # Conduct multiplication 
            # coefficient: 22, known_enclosed_expression; (18 - x + 2), known_enclosed_terms: ['18', '-x', '+2)']
            print(f"coefficient: {known_coefficient}, known_enclosed_expression; {known_enclosed_expression}, known_enclosed_terms: {known_enclosed_terms}")
            
            # Combining and rewriting terms 
            combined_expression = combining_expression(unknown, known_enclosed_terms)
            coefficient_and_enclosed_expression = updating_expression(coefficient_and_enclosed_expression, known_enclosed_expression, combined_expression)
            del coefficient_and_enclosed_expression[list(coefficient_and_enclosed_expression.keys())[-1]]
            return coefficient_and_enclosed_expression, known_enclosed_terms 


        for char_ind in range(len(enclosed_expression)):
            char = enclosed_expression[char_ind] 

            if char in operations: 
                term = enclosed_expression[previous_operation_ind:char_ind]
                if previous_operation_ind == 0 and enclosed_expression[previous_operation_ind] not in operations:
                    term = enclosed_expression[previous_operation_ind + 1:char_ind]
                if term != '':
                    previous_operation_ind = char_ind
                    enclosed_terms.append(term) 
        enclosed_terms.append(enclosed_expression[previous_operation_ind:-1])

        known_coefficient = coefficient
        known_enclosed_expression = enclosed_expression
        known_enclosed_terms = enclosed_terms
        
    combined_expression = combining_expression(unknown, known_enclosed_terms)
    coefficient_and_enclosed_expression = updating_expression(coefficient_and_enclosed_expression, known_enclosed_expression, combined_expression)
    del coefficient_and_enclosed_expression[list(coefficient_and_enclosed_expression.keys())[-1]]
    return coefficient_and_enclosed_expression, known_enclosed_terms


def distributive_property(expression: str) -> str:
    # Given an expression with parenthesis and a coefficient "n" in front 
    # Multiply the individual term within the parenthesis with n 

    # Validating the paranthesis in given expression 
    if not valid_paranthesis(expression):
        raise Exception("Paranthesis are invalid.") 
    
    clear()

    # Unknown variable: x, y, ...
    unknown = ''
    
    # ------------------------------- Modifying Input Expression -------------------------------
    char_ind = 0 
    expression_list = list(expression)
    
    while char_ind < len(expression_list):
        char = expression_list[char_ind]
        
        if char.lower() in 'qwertyuiopasdfghjklzxcvbnm':
            unknown = char
        
        # Modify the expression with parentheses
        if char in ('[', '('):
            if char_ind > 0 and expression_list[char_ind - 1].isdigit():
                expression_list.insert(char_ind, '*')
                char_ind += 1  # Increment to skip the inserted '*'
            expression_list[char_ind] = '('
        
        char_ind += 1  
        
    expression = ''.join(expression_list).replace(' ', '')
    print(f"Modified expression: {expression}")
    print(f"unknown: {unknown}")
    
    # Storage
    coefficient_and_enclosed_expression = {} # coefficient: enclosed_term 
    coefficients = [] # Stores all the coefficients
    coefficient_ind = [] # Stores the index position of coefficients
    
    # ------------------------------- Identify Coefficient and Enclosed Expression -------------------------------
    left_pointer = 0 
    right_pointer = len(expression) - 1 
    print(f"expression: {expression}")
    while left_pointer < len(expression):

        if expression[left_pointer] == '(':
            # paranthesis is found 
            coefficient = 1 # Default coefficient
            
            # Find the coefficient of the paranthesis 
            if len(coefficient_ind) == 0:
                # Use everything to the left if no previous coefficient given 
                coefficient = expression[:left_pointer - 1]
                coefficient_ind.append(left_pointer)  
                print(f"coefficient: {expression[:left_pointer - 1]}")
            else:
                previous_open_bracket = coefficient_ind[-1] + 2  
                coefficient = expression[previous_open_bracket - 1:left_pointer - 1]
                coefficient_ind.append(left_pointer) 
                print(f"coefficient1: {expression[previous_open_bracket - 1:left_pointer - 1]}")
            coefficients.append(coefficient)
            # Find the index of closing paranthesis to determine the enclosed expression 
            while right_pointer > left_pointer:
                if expression[right_pointer] == ')':
                    # The index position is found for close paranthesis 
                    enclosed_expression = expression[left_pointer:right_pointer + 1]
                    print(f"enclosed_expression: {enclosed_expression}")
                    coefficient_and_enclosed_expression[coefficient] = enclosed_expression
                    right_pointer -= 1 
                    break 
                right_pointer -= 1 
                
        left_pointer += 1 
    print(f"coefficients: {coefficients}")

    # ------------------------------- Simplifying Enclosed Expression -------------------------------
    # Now given the processed expression we can begin to multiply from inside and work our way out 
    # Simplify the numerical terms and leaving the unknown
    coefficient_ind = -1
    update_enclosed_expression = ''
    update_value = ''
    while abs(coefficient_ind) < len(coefficients) + 1:
        coefficient = coefficients[coefficient_ind]
        enclosed_expression = coefficient_and_enclosed_expression[coefficient] 
        print(f"coefficient: {coefficient}, enclosed_expression: {enclosed_expression}")
        if unknown not in enclosed_expression and unknown not in coefficient:
            if coefficient[0] not in ('*', '/'):
                print("Point A triggered")
                update_enclosed_expression = coefficient + "*" + enclosed_expression
                print(f"update_enclosed_expression: {update_enclosed_expression}")
                update_value = eval(update_enclosed_expression)
                print(update_enclosed_expression, update_value)
                coefficient_ind -= 1 
                del coefficient_and_enclosed_expression[coefficient]
            else:
                raise Exception("Invalid operation symbol placement.")
            
        else:
            print("Point B triggered")
            for coefficient_ind in range(len(coefficient_and_enclosed_expression) - 1, -1, -1):
                coefficient = coefficients[coefficient_ind]
                new_enclosed_expression = coefficient_and_enclosed_expression[coefficient].replace(update_enclosed_expression, str(update_value))
                coefficient_and_enclosed_expression[coefficient] = new_enclosed_expression
            break 

    print("Run Result:\n")
    print(coefficient_and_enclosed_expression)

    # ------------------------------- Multiplying Coefficient with Enclosed Terms -------------------------------
    coefficient_and_enclosed_expression, enclosed_terms = collecting_like_terms(unknown, coefficient_and_enclosed_expression, coefficients)
    coefficient_and_enclosed_expression, enclosed_terms = collecting_like_terms(unknown, coefficient_and_enclosed_expression, coefficients)
    coefficient_and_enclosed_expression, enclosed_terms = collecting_like_terms(unknown, coefficient_and_enclosed_expression, coefficients)
    print(f"-------- {enclosed_terms} --------")
    a = combining_expression(unknown, enclosed_terms)
    print(a)

clear() # Clear Terminal
distributive_property("13(22(3(-2*3 / x / 2)) + x + 2)")


