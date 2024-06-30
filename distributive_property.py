# Ericsson Cui
# 2024/06/29 

import os

# Clear Terminal
def clear():
    os.system("cls || clear")

# Validating the parenthesis of input expression
def valid_parenthesis(expression: str) -> bool:
    stack = []
    pair = {'(': ')', '[': ']', '{': '}'}
    for char in expression:
        if char in pair:
            stack.append(char)
        elif char in pair.values():
            if not stack or pair[stack.pop()] != char:
                return False
    return not stack

# Determine if the given string is numeric
def isNumeric(string: str) -> bool:
    try:
        float(string) 
        return True 
    except ValueError:
        return False

# Modifying the given expression to satisfy future process
def modify_expression(expression: str) -> tuple:
    unknown = None
    modified_expression = []

    for char in expression:
        if char.lower() in 'abcdefghijklmnopqrstuvwxyz':
            unknown = char
        if char in ['[', '(']:
            if modified_expression and modified_expression[-1].isdigit():
                modified_expression.append('*')
            modified_expression.append('(')
        else:
            modified_expression.append(char)

    modified_expression = ''.join(modified_expression).replace(' ', '')
    print(f"Modified expression: {modified_expression}")
    print(f"Unknown variable: {unknown}")

    if unknown is None:
        print(f"{modified_expression} = {eval(modified_expression)}")
        quit()
    return unknown, modified_expression

def identify_coefficient_and_enclosed_expression(expression: str) -> set:
    # Storage
    coefficient_and_enclosed_expression = {} # coefficient: enclosed_term 
    coefficients = [] # Stores all the coefficients
    coefficient_ind = [] # Stores the index position of coefficients
    
    # Initialize left&right pointer
    left_pointer = 0 
    right_pointer = len(expression) - 1 

    print('-'*30)

    while left_pointer < len(expression):

        if expression[left_pointer] == '(':
            # parenthesis is found 
            coefficient = 1 # Default coefficient
            
            # Find the coefficient of the parenthesis 
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
            # Find the index of closing parenthesis to determine the enclosed expression 
            while right_pointer > left_pointer:
                if expression[right_pointer] == ')':
                    # The index position is found for close parenthesis 
                    enclosed_expression = expression[left_pointer:right_pointer + 1]
                    print(f"enclosed_expression: {enclosed_expression}")
                    coefficient_and_enclosed_expression[coefficient] = enclosed_expression
                    right_pointer -= 1 
                    break 
                right_pointer -= 1 
            print("-"*30)
                
        left_pointer += 1 
    print(f"coefficient_and_enclosed_expression: {coefficient_and_enclosed_expression}")
    print(f"coefficients: {coefficients}")
    print(f"coefficient_ind: {coefficient_ind}") 
    return coefficient_and_enclosed_expression, coefficients

def identify_enclosed_terms(enclosed_expression: str) -> list:
    # Collect all individual terms inside the enclosed expression
    # Handle operators and parentheses correctly, ensuring that '*' and '/' are stored by themselves,
    # while '+' and '-' are inclusive with the terms that follow them.
    operations = set('+-*')
    enclosed_terms = []
    operators = [] 
    term_start = 0
    print(f"enclosed_expression: {enclosed_expression}")
    if enclosed_expression[0] == '(' and enclosed_expression[-1] == ')':
        enclosed_expression = enclosed_expression[1:-1]
    
    if enclosed_expression[0] == '*' or enclosed_expression[-1] in '+-':
        raise Exception("Operators placed in incorrect position.")

    for char_ind, char in enumerate(enclosed_expression):
        if char in operations:
            if char_ind > 0 and enclosed_expression[char_ind-1] not in operations:
                # Cases where the operation should be included in the next term
                # Previous char is not an operation 
                if char in '+-':
                    enclosed_terms.append(enclosed_expression[term_start:char_ind].strip())
                    term_start = char_ind  # Start the new term from the operator
                elif char in '*':
                    enclosed_terms.append(enclosed_expression[term_start:char_ind].strip())
                    enclosed_terms.append(char) # Add the operator itself as a seperate term 
                    term_start = char_ind + 1  # Start new term after the operator
                operators.append(char)
            elif char_ind == 0 or enclosed_expression[char_ind-1] in operations:
                # Possibly a division/multiplication of a negative term 
                if char in '*':
                    enclosed_terms.append(char)
                    operators.append(char)
                    term_start = char_ind + 1

        elif char_ind == len(enclosed_expression) - 1: 
            # Add the last term 
            enclosed_terms.append(enclosed_expression[term_start:].strip())
    print(f"operators: {operators}")
    return enclosed_terms, operators
    
def finding_coefficients(unknown: str, terms: list, multiplication: bool) -> bool:
    coefficients = [] 
    unknown_found = False
    print(f"given terms: {terms}") 
    for term in terms:
        if unknown not in term:
            coefficients.append(term)
        else:
            coefficient = term[:term.index(unknown)] 
            if not isNumeric(coefficient):
                coefficient = coefficient + '1'
            coefficients.append(coefficient)
            unknown_found = True 
    
    if multiplication:
        coefficients.insert(1, '*') 
        print(f"coefficients: {coefficients}")
        coefficient = str(eval(''.join(coefficients)))
        if unknown_found:
            return coefficient + 'x'
        return coefficient
    else:
        return coefficients 
                    
def simplify_enclosed_expression(unknown: str, enclosed_expression: str, enclosed_terms: str) -> str:
    print(f"enclosed_expression: {enclosed_expression}")
    if unknown not in enclosed_expression:
        simplified_expression = eval(enclosed_expression)
        print(f"simplified_expression: {simplified_expression}")
        return str(simplified_expression)
    else:
        # Unknown values in enclosed expression
        print(f"Unknown values...\nexpression 14: {enclosed_expression}")
        multiplied_terms = [term_ind for term_ind in range(len(enclosed_terms)) if enclosed_terms[term_ind] == '*']
        print(f"multiplied_terms: {multiplied_terms}")
        
        if len(multiplied_terms) == 0:
            terms_with_unknown = [] 
            terms_with_numeric = [] 
            for term_ind, term in enumerate(enclosed_terms):
                if unknown in term:
                    terms_with_unknown.append(term)
                else:
                    terms_with_numeric.append(term) 

            coefficients_of_numeric = eval(''.join(terms_with_numeric))
            print(f"coefficients_of_numeric: {coefficients_of_numeric}")

            coefficients_of_unknown = finding_coefficients(unknown, terms_with_unknown, False)
            print(f"coefficients_of_unknown: {coefficients_of_unknown}")

            new_coefficients_of_unknown = eval(''.join(coefficients_of_unknown))
            print(f"new_coefficients_of_unknown: {new_coefficients_of_unknown}") 

            if coefficients_of_numeric < 0:
                enclosed_expression = str(new_coefficients_of_unknown) + unknown + str(coefficients_of_numeric)
            elif coefficients_of_numeric > 0:
                enclosed_expression = str(new_coefficients_of_unknown) + unknown + '+' + str(coefficients_of_numeric)
            else:
                enclosed_expression = str(new_coefficients_of_unknown) + unknown
            print(f"new enclosed_expression: {enclosed_expression}")
            return enclosed_expression
                
        
        # Combining coefficients for multiplication
        for term_ind, term in enumerate(enclosed_terms):
            if term == '*':
                prev_term, next_term = enclosed_terms[term_ind - 1], enclosed_terms[term_ind + 1] 
                combined_term = finding_coefficients(unknown, [prev_term, next_term], True)
                enclosed_terms = [combined_term] + enclosed_terms[term_ind+2:] 
                print(f"updated enclosed_terms: {enclosed_terms}")
                print("-"*40)
                return simplify_enclosed_expression(unknown, enclosed_expression, enclosed_terms)

    print("-"*40)      

def multiply_inside_out(unknown: str, coefficient: str, enclosed_terms: list, operators: list) -> str: 
    print(f" --- multiply_inside_out:\ncoefficient: {coefficient}\nenclosed_terms: {enclosed_terms} ")
    new_term = ''
    for term_ind, term in enumerate(enclosed_terms):
        if unknown in coefficient and unknown in term:
            raise Exception("Only linear relations are accepted.")
        if unknown in coefficient:
            term_coefficient = coefficient[:coefficient.index(unknown)] 
            new_coefficient = float(term_coefficient) * float(term)
            new_term += str(new_coefficient) + unknown 
        elif unknown in term:
            term_coefficient = term[:term.index(unknown)] 
            new_coefficient = float(coefficient) * float(term_coefficient)
            new_term += str(new_coefficient) + unknown 
        
        if term_ind <= len(operators) - 1:
            if enclosed_terms[term_ind + 1][0] != '-':
                new_term += operators[term_ind] 
            
        else:
            new_term += str(float(coefficient) * float(term))
    print(f"new_term: {new_term}")
    return new_term

def updating_expression(coefficient_and_enclosed_expression, update_expression, update_value):
    coefficients = list(coefficient_and_enclosed_expression.keys())
    coefficient_index = len(coefficient_and_enclosed_expression) - 1 

    while coefficient_index >= 0:
        coefficient = coefficients[coefficient_index - 1]
        print(f"---------- Replacing {update_expression} with {'(' + str(update_value) + ')'} ----------")
        new_expression = coefficient_and_enclosed_expression[coefficient].replace(update_expression, str(update_value))
        coefficient_and_enclosed_expression[coefficient] = new_expression
        coefficient_index -= 1
 
    print(coefficient_and_enclosed_expression)
    return coefficient_and_enclosed_expression

def distributive_property(input_expression: str) -> str:
    # Validating the parenthesis in given expression 
    if not valid_parenthesis(input_expression):
        raise Exception("parenthesis are invalid.") 
    
    # Reject rational expressions
    if '/' in input_expression:
        raise Exception("Rational expression will not be accepted.")
    
    # Initialize base conditions
    # Determining the unknown variable and break down brackets
    unknown_var, expression = modify_expression(input_expression)  
    coefficient_and_enclosed_expression, coefficients = identify_coefficient_and_enclosed_expression(expression)
    print(f"unknown_var: {unknown_var}\nexpressio 12: {expression}")
    print(f"coefficient_and_enclosed_expression: {coefficient_and_enclosed_expression}\ncoefficients: {coefficients}")

    coefficient_index = len(coefficient_and_enclosed_expression) - 1 
    while coefficient_index >= 0: 

        coefficient = coefficients[coefficient_index] # Enclosed expression coefficient
        enclosed_expression = coefficient_and_enclosed_expression[coefficient] # Enclosed expression

        print(f"coefficient: {coefficient} ------------- enclosed_expression: {enclosed_expression}")

        enclosed_terms, operators = identify_enclosed_terms(enclosed_expression)
        new_expression = simplify_enclosed_expression(unknown_var, enclosed_expression, enclosed_terms)
        terms, operators = identify_enclosed_terms(new_expression)

        updated_expression = multiply_inside_out(unknown_var, coefficient, terms, operators)
        updating_expression(coefficient_and_enclosed_expression, coefficient + "*" + enclosed_expression, updated_expression)

        print(coefficient_and_enclosed_expression)
        del coefficient_and_enclosed_expression[coefficient]

        coefficient_index -= 1 
        print("-"*100)
    final_expression = multiply_inside_out(unknown_var, coefficient, terms, operators)
    print("-"*100)
    print("Simplified Solution:")
    print(f"{input_expression} = {final_expression}")
    print("-"*100)
    return final_expression

clear()
input_expression = "13(22(3(-2*3) * x - 2) + x)"

distributive_property_questions = ['2(4 + 9w)', '10(12 - x)', '5(2 + 9x)', '25(4 - x)', '10(2(x+1))']
answers = []
for question in distributive_property_questions:
    answers.append(distributive_property(question))

distributive_property(input_expression)

print("\n\n--------- Testing ---------")
for question_id in range(len(distributive_property_questions)):
    print(f"{distributive_property_questions[question_id]} => {answers[question_id]}")
