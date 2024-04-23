
from collections import defaultdict
import random
from timeit import default_timer as timer
random.seed()

num_players = 4

class Dealer:
    def __init__(self, num_players):
        self.num_players = num_players
        self.hands = [] # Store the hands of each player
        self.deck = []
        self.special_values = {'A': '[1, 11]', 
                               'J': '10', 
                               'Q': '10', 
                               'K': '10'}

    def shuffle(self):
        self.hands = [[] for _ in range(num_players)]
        suits = ['♠', '♥', '♦', '♣']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = [{'value': value, 'suit': suit} for value in values for suit in suits]

        random.shuffle(self.deck)
        return self.deck 

    def draw(self):
        # Every Player (Including the Dealer)
        # Recieves 2 cards at start

        for _ in range(2):
            for player in range(self.num_players):
                card = self.deck.pop() # {'value': '2', 'suit': '♠'}
                self.hands[player].append(card)
        
        return self.hands 
    
    def deal_cards(self, playerID): 
        card = self.deck.pop()
        self.hands[playerID].append(card)
    
    def decision(self):
        dealer_hand = [card['value'] for card in self.hands[0]] # ['9', 'A']
        dealer_hand_val = [self.special_values[card] if card in ['A', 'J', 'Q', 'K'] else card for card in dealer_hand]  # [9, [1, 11]]
        #print(dealer_hand_val)

        ace_present = False 

        handA = []   # First hand
        handA_sum = 0

        handB = None # Second hand if Ace is present
        handB_sum = None

        # Check win statement right here

        if "A" in dealer_hand: # 2 Possible Scenario
            ace_present = True 

            handA = list(map(lambda x: x.replace('[1, 11]', '1'), dealer_hand_val))  # ['1', '8']
            handB = list(map(lambda x: x.replace('[1, 11]', '11'), dealer_hand_val)) # ['11', '8']

            handA_sum = sum([int(i) for i in handA])
            handB_sum = sum([int(i) for i in handB]) 
        
        else:
            handA = dealer_hand_val
            handA_sum = sum([int(i) for i in handA])

        #print(f"handA: {handA}\nhandA_sum: {handA_sum}\nhandB: {handB}\nhandB_sum: {handB_sum}")

        primary_hand = None 

        if ace_present:
            for i in range(2):
                hand = [handA, handB][i]
                val = [handA_sum, handB_sum][i]
                
                return dealer.card_counting((hand, val))
            # primary_hand = (handA, handA_sum) if handA_sum >= handB_sum else (handB, handB_sum)
        else:
            primary_hand = (handA, handA_sum)

        #print(f"primary_hand: {primary_hand}")
        return dealer.card_counting(primary_hand)

    def card_counting(self, primary_hand):
        hand, val = primary_hand
        winning_difference = 21 - val 
        deck = [card['value'] for card in self.deck]

        safe_cards_count = 0 # Cards the dealer can have without getting busted
        #print(f"winning_difference: {winning_difference}")
        safe_cards_count += deck.count('A')

        for card_val in range(2, winning_difference+1):
            safe_cards_count += deck.count(str(card_val))

        #print(f"safe_card_count: {safe_cards_count}, len(deck): {len(deck)}")

        #print(f"Chance of not busting: {(safe_cards_count/len(deck))*100:.2f}%")
        
        return (val, round((safe_cards_count/len(deck))*100, 2))

start = timer()

# Deal cards to players
dealer = Dealer(num_players)

testcase = defaultdict(list) 
testcase_avg = defaultdict(list)
count = 1 
while count <= 100:
    deck = dealer.shuffle()
    hands = dealer.draw()
    val, safe_percentage = dealer.decision()
    if val <= 21:
        print(f"Count: {count}")
        testcase[val].append(safe_percentage)
        count += 1
    
# Find median value of every sum of card combinations
for val in testcase.keys():
    tests = testcase[val] 
    tests = sorted(tests) 
    median = tests[len(tests)//2] 
    average = round((sum(tests) / len(tests)),2)
    testcase_avg[val] = (median, average) 
    
testcase_avg = [{i: testcase_avg[i]} for i in sorted(testcase.keys())]
end = timer() 

print(testcase_avg)
print(f"Run time: {end-start} seconds")    

"""
Terminal Output: Test Run
Cards Count: 44, Hands: [[{'value': '9', 'suit': '♠'}, {'value': '5', 'suit': '♥'}], [{'value': 'Q', 'suit': '♦'}, {'value': 'J', 'suit': '♣'}], [{'value': 'A', 'suit': '♦'}, {'value': '10', 'suit': '♥'}], [{'value': 'Q', 'suit': '♣'}, {'value': '6', 'suit': '♦'}]]
Cards Count: 43, Hands: [[{'value': '9', 'suit': '♠'}, {'value': '5', 'suit': '♥'}], [{'value': 'Q', 'suit': '♦'}, {'value': 'J', 'suit': '♣'}, {'value': '7', 'suit': '♥'}], [{'value': 'A', 'suit': '♦'}, {'value': '10', 'suit': '♥'}], [{'value': 'Q', 'suit': '♣'}, {'value': '6', 'suit': '♦'}]]
Cards Count: 42, Hands: [[{'value': '9', 'suit': '♠'}, {'value': '5', 'suit': '♥'}], [{'value': 'Q', 'suit': '♦'}, {'value': 'J', 'suit': '♣'}, {'value': '7', 'suit': '♥'}, {'value': 'J', 'suit': '♥'}], [{'value': 'A', 'suit': '♦'}, {'value': '10', 'suit': '♥'}], [{'value': 'Q', 'suit': '♣'}, {'value': '6', 'suit': '♦'}]]
['9', '[1, 11]']
handA: ['9', '1']
handA_sum: 10
handB: ['9', '11']
handB_sum: 20
primary_hand: (['9', '11'], 20)
winning_difference: 1
safe_card_count: 3, len(deck): 42
Chance of not busting: 7.14%
"""
