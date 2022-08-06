import random as rd

word_bank = {'Person name': ['william', 'peter', 'wallage'],
             'car': ['bmw', 'mercades', 'toyota']}
word_bank_category = ['Person name', 'car']

category_name = word_bank_category[rd.randint(0, 1)] # display the category name
item_index = rd.randint(0, 2) # display the selection item in each category
correct_word = str(word_bank[category_name][item_index])

'''
The correct_word_list will replace the correct alphabet that the
user have inputed with a dash(-), which will eventually eliminate the possibility 
of a duplicate alphabet not being able to be processed by the program
'''
correct_word_list = list(correct_word) # check up with user's input
display_list = [char.replace(char, '_') for char in correct_word] # displaying to the users
print('%s: %s(%d alphabets)' % (category_name, display_list, len(display_list)))

wrong_guesses = []
limit_guesses = 0
count = 0

def result():
    if '_' not in display_list:
        print('win!'), quit()

def hangman_drawer():
    global limit_guesses
    if limit_guesses == 1:
        print("   _____ \n"
              "  |      \n"
              "  |      \n"
              "  |      \n"
              "  |      \n"
              "  |      \n"
              "  |      \n"
              "__|__\n")
        print("Wrong guess. " + str(limit_guesses) + " guesses remaining\n")
    elif limit_guesses == 2:
        print("   _____ \n"
              "  |     | \n"
              "  |     |\n"
              "  |     | \n"
              "  |     O \n"
              "  |      \n"
              "  |      \n"
              "__|__\n")
        print("Wrong guess. " + str(limit_guesses) + " guesses remaining\n")
    elif limit_guesses == 3:
        print("   _____ \n"
              "  |     | \n"
              "  |     |\n"
              "  |     | \n"
              "  |     O \n"
              "  |    / \ \n"
              "  |      \n"
              "__|__\n")
        print("Wrong guess. " + str(limit_guesses) + " guesses remaining\n")
    elif limit_guesses == 4:
        print("   _____ \n"
              "  |     | \n"
              "  |     |\n"
              "  |     | \n"
              "  |     O \n"
              "  |    /|\ \n"
              "  |      \n"
              "__|__\n")
        print("Wrong guess. " + str(limit_guesses) + " last guess remaining\n")
    elif limit_guesses == 5:
        print("   _____ \n"
              "  |     | \n"
              "  |     |\n"
              "  |     | \n"
              "  |     O \n"
              "  |    /|\ \n"
              "  |    / \ \n"
              "__|__\n")
        print("Wrong guess. You are hanged!!!\n")
        print('The word was: "%s"' % correct_word)

def user_input():
    global limit_guesses, count
    while True:
        print('wrong guesses:',wrong_guesses)
        player_guess = input('Please enter your guess(alphabet): ')
        if player_guess in correct_word_list:
            count += 1
            guess_index = correct_word_list.index(player_guess) # finding the index of the correct alphabet
            correct_word_list[guess_index] = '-'
            display_list[guess_index] = player_guess # replace the dash with the correct alphabet user had input
            print('%s: %s(%d alphabets left)' % (category_name, display_list, len(display_list) - count))
            result()
        else:
            wrong_guesses.append(player_guess)
            limit_guesses += 1
            hangman_drawer()
            result()

user_input()
