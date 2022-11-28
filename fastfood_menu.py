# Python 3.9.6 64-bit
command = {1: 'Appetizers', 2: 'Mains', 3: 'Drinks', 4: 'Desserts', 5: 'View Order', 6: 'Exit'}

menu = {'Appetizers': {'French Fries': 3.40, 'Shrip Scampi': 4.30, 'Four Chesse Garlic Bread': 4.9}, 
        'Mains': {'Chessburger Combo': 7.99, 'Spicy Sandwhich': 9.89, 'Noodle': 8.99}, 
        'Drinks': {'Coca Cola': 2.00, 'Pepsi': 2.00, 'Sprite': 2.00}, 
        'Desserts': {'Ice cream': 3.99, 'Chessecake': 4.99, 'Putin': 3.99}}

sub_main = {'Chessburger Combo': {'Extra Cheese': 0.50, 'Extra Fries': 1.00},
            'Spicy Sandwhich': {'Extra Spice': 0.30, 'Extra Fries': 1.00},
            'Noodle': {'Extra Noodle': 1.50, 'Extra Beef': 3.00}}

order = {}

def view_order(): 
    total = 0
    for food in order.keys():
        total += float(order[food]) 
        print(food, order[food])
    print('Total:','{0:.2f}'.format(total*1.13))

def sub_main_func(food):
    print(sub_main[food]) 
    for _ in range(5):      
        sub_main_add = input("What sub choices do you want to make for your main?: ") 
        try:
            food_name = sub_main[food] 
            order[sub_main_add] = food_name[sub_main_add]
            exit = input("Have you finished adding sub mains?: ") 
        except KeyError:
            print("Please input a valid option")
            return sub_main_func(food)
        if exit in ['ye', 'yes', 'Yes', 'ofc']: 
            return customer_input()
        elif exit in ['no', 'nah']: 
            continue 
        else:
            print("Please input a valid option")
            return sub_main_func(food)

def customer_order(category, food):
    main = menu[category] 
    order[food] = main[food]
    print("Order Added")
    if category == 'Mains':
        sub_choice = input("Do you want to add any sub-choices?: ") 
        if sub_choice in ['ye', 'yes', 'Yes', 'ofc', 'True']:
            return sub_main_func(food)
        if sub_choice in ['no', 'nah', 'false']: 
            return customer_input()
    return customer_input()

def customer_input():
    while True:
        Number = input("\nPlease Select What You Would Like To Order (Type Number Between 1-6)")
        try:
            if int(Number) in [1,2,3,4,5,6]:
                return action(int(Number)) 
        except ValueError: 
            return customer_input()
    
def action(input_command):
    if input_command == 5:
       return view_order()
    if input_command == 6: 
       exit()
    else:
       category = command[input_command] 
       food_arr = menu[category]
       print(food_arr) 
       food_choice = input("What would you like to have?: ")
       return customer_order(category, food_choice)

def action_display():
    print("Welcome to McQuan's\n")
    for options in command.keys():
        print(options, command[options])
    return customer_input()
action_display()
