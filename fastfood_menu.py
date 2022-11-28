command = {1: 'Appetizers', 2: 'Mains', 3: 'Drinks', 4: 'Desserts', 5: 'View Order', 6: 'Exit'}

menu = {'Appetizers': {'French Fries': 3.40, 'Shrip Scampi': 4.30, 'Four Chesse Garlic Bread': 4.9}, 
        'Mains': {'Chessburger Combo': 7.99, 'Spicy Sandwhich': 9.89, 'Noodle': 8.99}, 
        'Drinks': {'Coca Cola': 2.00, 'Pepsi': 2.00, 'Sprite': 2.00}, 
        'Desserts': {'Ice cream': 3.99, 'Chessecake': 4.99, 'Putin': 3.99}}

sub_main = {'Chessburger Combo': {'Extra Cheese': 0.50, 'Extra Fries': 1.00},
            'Spicy Sandwhich': {'Extra Spice': 0.30, 'Extra Fries': 1.00},
            'Noodle': {'Extra Noodle': 1.50, 'Extra Beef': 3.00}}

order = {} # food: price

def view_order(): # customer view order
    total = 0
    for food in order.keys():
        total += float(order[food]) 
        print(food, order[food])
    print('Total:','{0:.2f}'.format(total*1.13))

def sub_main_func(food):
    print(sub_main[food]) # go into sub_main dictionary and find the extra options for food
    for _ in range(5): # loop for a few extra times if a person require extras            
        sub_main_add = input("What sub choices do you want to make for your main?: ") 
        try:
            food_name = sub_main[food] # 'Extra Fries': 1.00
            order[sub_main_add] = food_name[sub_main_add] # 'Extra Cheese': 0.50 (same as above)
            exit = input("Have you finished adding sub mains?: ") 
        except KeyError:
            print("Please input a valid option")
            return sub_main_func(food)
        if exit in ['ye', 'yes', 'Yes', 'ofc']: # possible user inputs(true)
            return customer_input()
        elif exit in ['no', 'nah']: # possible user inputs(false)
            continue # leave this loop
        else:
            print("Please input a valid option")
            return sub_main_func(food)

def customer_order(category, food):
    main = menu[category] # find the category inside dictionary named "menu", the value category could be 'Appetizers', 'Mains', 'Drinks', 'Desserts'
    order[food] = main[food] # # add the exact food inside the menu, so menu['Appetizers']['French Fries'] to find it's price
    print("Order Added")
    if category == 'Mains':
        sub_choice = input("Do you want to add any sub-choices?: ") # asks user if they want sub-choices
        if sub_choice in ['ye', 'yes', 'Yes', 'ofc', 'True']: # possible user inputs(true)
            return sub_main_func(food)
        if sub_choice in ['no', 'nah', 'false']: # possible user inputs(false)
            return customer_input()
    return customer_input()

def customer_input(): # customer input action
    while True:
        Number = input("\nPlease Select What You Would Like To Order (Type Number Between 1-6)")
        try:
            if int(Number) in [1,2,3,4,5,6]: # if customer input is valid
                return action(int(Number)) # return to action function for further interact
        except ValueError: # You cannot address numeral value into a alphabet
            return customer_input()
    
def action(input_command):
    if input_command == 5: # view order
       return view_order()
    if input_command == 6: # exit
       exit()
    else: # if customer perfer to order
       category = command[input_command] # appetizers, mains, drinks or desserts
       food_arr = menu[category] # appetizers, mains, drinks etc
       print(food_arr) # {'French Fries': 3.4, 'Shrip Scampi': 4.3, 'Four Chesse Garlic Bread': 4.9}
       food_choice = input("What would you like to have?: ")
       return customer_order(category, food_choice)

def action_display(): # display options
    print("Welcome to McQuan's\n")
    for options in command.keys(): # command.keys() will display all the keys in the dictionary command, keys are 1, 2, 3, 4 etc
        print(options, command[options]) # ex. 1, Appetizers 
    return customer_input()
action_display()
