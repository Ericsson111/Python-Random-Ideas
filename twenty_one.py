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

    def decision(self) -> tuple: 
        dealer_hand = [card['value'] for card in self.hands[0]] # ['9', 'A']
        dealer_hand_val = [self.special_values[card] if card in ['A', 'J', 'Q', 'K'] else card for card in dealer_hand]  # [9, [1, 11]]

        if dealer_hand == ['A', 'A']:
            dealer_hand_val = 12 
            return dealer.card_counting((['A', 'A'], 12))

        ace_present = False 

        handA = []  
        handA_sum = 0
        handB = None # Second hand if Ace is present
        # Check win statement right here
        if "A" in dealer_hand: # 2 Possible Scenario
            ace_present = True 
            handA = list(map(lambda x: x.replace('[1, 11]', '1'), dealer_hand_val))  # ['1', '8']
            handB = list(map(lambda x: x.replace('[1, 11]', '11'), dealer_hand_val)) # ['11', '8']
        
        else:
            handA = dealer_hand_val
            handA_sum = sum([int(i) for i in handA])

        primary_hand = None 

        if ace_present:
            primary_hand = dealer.optimized_ace_hand((handA, handB))
        else:
            primary_hand = (handA, handA_sum)

        return dealer.card_counting(primary_hand)
    
    # Return the optimized ace inclusive hand that allow the dealer to not bust 
    def optimized_ace_hand(self, hands: tuple) -> tuple:
        print(f"hand: {hands}")
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
        
"""
The following code is used to record the repeating simulation of the process and results
of drawing the first two cards for the player and the dealer. The result is stored in a
json file including the average and median value of the percentage for the dealer to
recieve a safe cards when getting a certain value of cards to begin with.

# Testings
start = timer() # Begin timer
dealer = Dealer(num_players)

# Store testcase results
testcase = defaultdict(list) 
testcase_avg = defaultdict(list)

# Total simulation 
testrun_amount = input("Enter the total simulation amount: ")
testrun_amount = int(testrun_amount)
count = 1

while count <= testrun_amount:
    deck = dealer.shuffle()    
    hands = dealer.draw()     
    print(count)
    val, safe_percentage = dealer.decision() 

    if count == testrun_amount:
        break 

    # Check if the current count is a multiple of 10% of the total runs
    if count % (testrun_amount // 10) == 0:
        progress = (count * 100) // testrun_amount  # Calculate progress percentage
        print(f"Testrun: {progress}%  - {count} Runs Completed")
    
    if val <= 21:
        testcase[val].append(safe_percentage)
        count += 1
    
# Find median value of every sum of card combinations
for val in testcase.keys():
    tests = testcase[val] 
    tests = sorted(tests) 
    median = tests[len(tests)//2] 
    average = round((sum(tests) / len(tests)),2)
    testcase_avg[val] = (median, average) 
    
end = timer()

testcase_avg = [{i: {"Median": str(testcase_avg[i][0]) + "%" , "Average": str(testcase_avg[i][1]) + "%"}} for i in sorted(testcase.keys())] 
testcase_avg += {"Run time": f"{end-start:.3f} seconds"}, {"Test case": f"{count:,}"}

# Display test run result
print(json.dumps(
    testcase_avg,
    sort_keys = True,
    indent = 4
))

file_name = 'Blackjack_Testrun_Results.json'

# Save in Json file
with open(file_name, 'w') as file:
    json.dump(testcase_avg, file, indent=4, sort_keys=True)

print(f'Program run time: {end-start:.3f} seconds') 
print(f'{count:,} test case completed')   
print(f'All recorded data has been stored in: {file_name}.')
"""
