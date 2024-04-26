# Python 3.9.6 64-bit
# 2024/4/24
# Ericsson Cui

# This program calculates the median and average percentage of the dealer 
# drawing a safe card (sum of hand <= 21) in a deck of 52 cards. The number
# of players can be customized and will have impact on the result percentage.
# The object "Dealer" includes the function of a typical dealer's actions, 
# including: shuffling, drawing, dealing cards, and more. The main code covers
# the process on retrieving the simulation result based on the testrun_amount
# and will store the final result in a seperate Json file named "Blackjack_Testrun_Results.json". 

from collections import defaultdict
import random
import json 
from timeit import default_timer as timer

num_players = 2

class Dealer:
    def __init__(self, num_players):
        self.num_players = num_players
        self.hands = [] # Store the hands of each player
        self.deck = []
        self.special_values = {'A': '[1, 11]', 
                               'J': '10', 
                               'Q': '10', 
                               'K': '10'}
        
    def shuffle(self) -> list:
        self.hands = [[] for _ in range(num_players)]
        suits = ['♠', '♥', '♦', '♣']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = [{'value': value, 'suit': suit} for value in values for suit in suits]
        random.shuffle(self.deck)
        return self.deck 
    
    def draw(self) -> list:
        # Every Player (Including the Dealer)
        # Recieves 2 cards at start
        for _ in range(2):
            for player in range(self.num_players):
                card = self.deck.pop() # {'value': '2', 'suit': '♠'}
                self.hands[player].append(card)
        
        return self.hands 
    
    def deal_cards(self, playerID: int): 
        card = self.deck.pop()
        self.hands[playerID].append(card)
        

    def hand_evaluation(self, playerID) -> tuple: 
        hand = [card['value'] for card in self.hands[playerID]] # ['9', 'A']
        hand_val = [self.special_values[card] if card in ['A', 'J', 'Q', 'K'] else card for card in hand]  # [9, [1, 11]]

        if hand == ['A', 'A']:
            hand_val = 12 
            return dealer.card_counting((['A', 'A'], 12))

        ace_present = False 

        handA = []  
        handA_sum = 0
        handB = None # Second hand if Ace is present
        # Check win statement right here
        if "A" in hand: # 2 Possible Scenario
            ace_present = True 
            handA = list(map(lambda x: x.replace('[1, 11]', '1'), hand_val))  # ['1', '8']
            handB = list(map(lambda x: x.replace('[1, 11]', '11'), hand_val)) # ['11', '8']
        
        else:
            handA = hand_val
            handA_sum = sum([int(i) for i in handA])

        primary_hand = None 

        if ace_present:
            primary_hand = dealer.optimized_ace_hand(playerID, hand, (handA, handB))
        else:
            primary_hand = (handA, handA_sum)
        
        return dealer.card_counting(primary_hand)
    
    # Return the optimized ace inclusive hand that allow the dealer to not bust 
    def optimized_ace_hand(self, playerID, hand, hands: tuple) -> tuple:
        print(f"Player {playerID} - hand: {hands}")
        handA, handB = hands

        handA_sum = sum([int(card_val) for card_val in handA]) 
        handB_sum = sum([int(card_val) for card_val in handB])

        primary_hand = None

        # If either scenario goes bust and alternative is safe -> return the safe hand
        if handA_sum > 21 and handB_sum <= 21:
            primary_hand = (handB, handB_sum)
        elif handB_sum > 21 and handA_sum <= 21:
            primary_hand = (handA, handA_sum) 
        
        # If both scenarios are safe <= 21
        if handA_sum <= 21 and handB_sum <= 21:
            primary_hand = (handA, handA_sum) if handA_sum >= handB_sum else (handB, handB_sum)
            
        # If both scenarios are bust > 21
        if handA_sum > 21 and handB_sum > 21:
            return f"Player {playerID} busted with the hand: {hand}"

        print(f"optimized ace hand: {primary_hand}")
        return primary_hand
    
    # Calculate the chance of the dealer to draw a safe card 
    def card_counting(self, primary_hand: tuple) -> tuple:
        hand, val = primary_hand
        winning_difference = 21 - val 
        deck = [card['value'] for card in self.deck]
        safe_cards_count = 0 # Cards the dealer can have without getting busted

        safe_cards_count += deck.count('A')
        for card_val in range(2, winning_difference+1):
            safe_cards_count += deck.count(str(card_val))
        
        return (hand, val, round((safe_cards_count/len(deck))*100, 2))
    
    def win_probability(self, playerID):
        # Player has taken all the cards and choose to stand
        # Calculate the difference between player_hand_sum and dealer_hand_sum
        # For example: player_hand_sum = 19[K, 6, 3], dealer_hand_sum = 14[J, 4], Deck: 47 cards remaining
        # Difference = 19 - 14 = 5 -> Min = 5, Max = 21 - 14 = 7, Range = 5 - 7
        # Calculate the chance to recieve a card with value in the range from 5 - 7
        #   -> This chance is equivelent to winning/tie chance 
        # If winning chance is greater than the average/media percentage of the card_val
        # Take another card from the deck
        player_hand, player_sum, player_chance = dealer.hand_evaluation(playerID)
        dealer_hand, dealer_sum, dealer_chance = dealer.hand_evaluation(0)
        
        min_tie_difference = player_sum - dealer_sum 
        max_win_difference = 21 - dealer_sum 
        
        deck = [card['value'] for card in self.deck]
        win_cards_count = 0 # Cards the dealer can have without getting busted

        for card_val in range(max_win_difference - min_tie_difference):
            win_cards_count += deck.count(str(card_val))
            
        print(f"player hand: {player_hand} - {player_sum}")
        print(f"dealer hand: {dealer_hand} - {dealer_sum}")
        print(f"win cards: {win_cards_count}")
    
    
dealer = Dealer(num_players) 

onGoingGame = True

dealer.shuffle()
dealer.draw()
dealer.deal_cards(1)
dealer.deal_cards(0)
print("player",dealer.hand_evaluation(1))
print("dealer",dealer.hand_evaluation(0))
print("--------------------------------------------")
dealer.win_probability(1)
"""
while onGoingGame:
    print(dealer.hands)
    userDecision = input("Do you want a card: ")
    if userDecision == 'y':
        dealer.deal_cards(1)
    elif userDecision == 'n':
        print(dealer.hands)
        print(dealer.decision()) 
        break
"""    
