import random as rd

cards = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8',
         '9': '9', '10': 'X', '11': 'J', '12': 'Q', '13': 'K', '11': 'A'}
cards_keys = list(cards.keys())
game_status = True
winner = None

def print_card_user(display_card_arr):
    total_cards = len(display_card_arr)
    for idx in range(total_cards):
        print('______________', end = '   ')
    print('\n')
    for idx in range(total_cards):
        print('|%s           |' % cards[display_card_arr[idx]], end = '   ') 
    print('\n')
    for idx in range(total_cards):
        print('|            |', end = '   ')
    print('\n')
    for idx in range(total_cards):
        print('|            |', end = '   ')
    print('\n')
    for idx in range(total_cards):
        print('|           %s|' % cards[display_card_arr[idx]], end = '   ')
    print('\n')
    for idx in range(total_cards):
        print('--------------', end = '   ')
    print('\n')
    
def win_determine(player_cards_list, computer_cards_list):
    global winner
    player_cards_list = [int(i) for i in player_cards_list]
    computer_cards_list = [int(i) for i in computer_cards_list]
    if sum(player_cards_list) == 21:
        winner = 'Player'
    if sum(computer_cards_list) == 21:
        winner = 'Computer'
    if sum(player_cards_list) > 21:
        winner = 'Computer'
    if sum(computer_cards_list) > 21:
        winner = 'Player'
    if sum(player_cards_list) == sum(computer_cards_list):
        winner = 'Drew'
    if sum(player_cards_list) > 21:
        if sum(computer_cards_list) > 21:
            winner = 'None'
    if sum(player_cards_list) < 21:
        if sum(computer_cards_list) < 21:
            if sum(player_cards_list) > sum(computer_cards_list):
                winner = 'Player'
            if sum(player_cards_list) < sum(computer_cards_list):
                winner = 'Computer'

def reshuffle(player_cards, computer_cards):
    player_cards = [int(i) for i in player_cards]
    computer_cards = [int(i) for i in computer_cards]
    if sum(player_cards) > 21:
        play()
    if sum(computer_cards) > 21:
        play()
    if sum(player_cards) == 21:
        print('Player Wins - Blackjack')
    if sum(computer_cards) == 21:
        print('Computer Wins - Blackjack')

def computer_move(computer_cards):
    cards = [int(i) for i in computer_cards]
    if 21 - sum(cards) <= 4:
        print('\nComputer Chose to Stand')
    else:
        computer_cards.append(cards_keys[rd.randint(0, 12)])

def play():
    global game_status, winner
    player_cards = []
    computer_cards = []
    for _ in range(2):
        player_cards.append(cards_keys[rd.randint(0, 12)])
        computer_cards.append(cards_keys[rd.randint(0, 12)])
    reshuffle(player_cards, computer_cards)
    print("Player Current Cards:\n")
    print_card_user(player_cards)
    while game_status == True:
        if winner == None:
            computer_move(computer_cards)
            player_decision = input("""Hit or Stand?""")
            if player_decision.lower() == 'hit':
                player_cards.append(cards_keys[rd.randint(0, 12)])
                print_card_user(player_cards)
            if player_decision.lower() == 'stand':
                win_determine(player_cards, computer_cards)
                print("Game result: Player: %d - Computer: %d" % (sum([int(i) for i in player_cards]), sum([int(i) for i in computer_cards])))
                print("\nThe Winner is: %s" % winner)
                print("Computer's Cards:")
                print_card_user(computer_cards)
                quit()
play()
