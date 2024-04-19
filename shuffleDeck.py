import random
from collections import defaultdict

player_id = 1
num_players = 2

card_deck = {}

def create_deck():
    suits = ['♠', '♥', '♦', '♣']
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = [{'value': value, 'suit': suit} for value in values for suit in suits]
    return deck

def shuffle_deck(deck):
    random.shuffle(deck)

def deal_cards(deck, num_players):
    global card_deck
    if num_players * 5 > len(deck):
        raise ValueError("Not enough cards in the deck to deal to all players.")

    for player in range(num_players):
        deal = input("1. Hit\n2. Stay\nEnter: ")
        if deal == '1':
            card = deck.pop()
            if player in card_deck.keys():
                card_deck[player].append(card)
            else:
                card_deck[player] = []
                card_deck[player].append(card)
        elif deal == '2':
            print(f"Player {player} stayed.") 
        else:
            print("Invalid choice!") 
            return deal_cards(deck, num_players)
    print(card_deck)

def new_deck():
    # Create and shuffle the deck
    deck = create_deck()
    shuffle_deck(deck)
    return deck 

# Deal cards to players
deck = new_deck()

deal_cards(deck, num_players)

    
