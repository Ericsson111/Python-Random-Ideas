# Python 3.8.6 64-bit
import sys
priority = {0: ['(', ')'], 1: ['[', ']'], 2: ['*', '/'], 3: ['+', '-']}

class Calculator():
    def __init__(self, expression):
        self.expression = expression

    def find_priority_index(self, inp):
        index_arr = {}
        for index, char in enumerate(inp):
            if char == None:
                pass
            if char.isdigit():
                pass
            else:
                for key, value in priority.items():
                    if char in value:
                        if key in index_arr.keys():
                            index_arr[key].append(index)
                        else:
                            index_arr[key] = [index]
        return index_arr 
        
    def bracket_filter(self):
        bracket_arr = {}
        Q = self.expression
        sorted_arr = calculator.find_priority_index(Q)
        for key in [int(i) for i in sorted_arr.keys()]:
            if key == 1: # if there is square bracket
                if 0 in [int(i) for i in sorted_arr.keys()]: # if the rounde bracket is in the expression
                    if sorted_arr[0][0] > sorted_arr[key][0]: # if the round bracket is in the square bracket
                        bracket_arr[sorted_arr[key][0]] = (Q[sorted_arr[key][0] : sorted_arr[key][1]+1])
                        return calculator.evaluate_inside_bracket(bracket_arr[sorted_arr[key][0]])
                else:
                    bracket_arr[sorted_arr[key][0]] = (Q[sorted_arr[key][0] : sorted_arr[key][1]+1])
                    return calculator.evaluate_inside_bracket(bracket_arr[sorted_arr[key][0]])
            if key == 0:
                bracket_arr[sorted_arr[key][0]] = (Q[sorted_arr[key][0] : sorted_arr[key][1]+1])
                return calculator.evaluate_inside_bracket(bracket_arr[sorted_arr[key][0]])
            if '(' or '[' not in Q:
                return calculator.evaluate_outside_bracket(Q)
    
    def evaluate_inside_bracket(self, inp):
        question = self.expression
        for char_index in range(len(inp)):
            if '(' == inp[char_index]: 
                for i in range(len(inp)):
                    if inp[char_index+i] == ')':
                        result_round_bracket = eval(inp[char_index+1:char_index+i])
                        question = question.replace(str(inp[char_index:char_index+i+1]), str(result_round_bracket))
                        break
        if '[' in question:
            evaluation = str(eval(question[question.index('[')+1:question.index(']')]))
            question = question.replace(str(question[question.index('['):question.index(']')+1]), evaluation)
        return calculator.evaluate_outside_bracket(question)
        
    def evaluate_outside_bracket(self, inp):
        return eval(inp)

print("BEDMAS calculator")
print('Please type "q" if you want to end the session.')
while True:
    question = input("What is your question?: ")
    if question in ['q', 'Q', 'quit']:
        print('Session ended')
        sys.exit()
    calculator = Calculator(str(question.replace(' ', '')).replace('x' or 'X', '*'))
    print('For the question: %s\nThe answer will be: %s\n' % (question, calculator.bracket_filter()))
