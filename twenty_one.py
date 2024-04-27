# Python 3.9.6 64-bit
# 2024/4/26
# Ericsson Cui

# This program calculates the median and average percentage of the dealer 
# drawing a safe card (sum of hand <= 21) in a deck of 52 cards. The number
# of players can be customized and will have impact on the result percentage.
# The object "Dealer" includes the function of a typical dealer's actions, 
# including: shuffling, drawing, dealing cards, and more. The main code covers
# the process on retrieving the simulation result based on the testrun_amount
# and will store the final result in a seperate Json file named "Blackjack_Testrun_Results.json". 

from collections import defaultdict
from timeit import default_timer as timer
import random
import json 

class Game:
    def __init__(self):
        self.num_players = 2
        self.game_status = True 
        self.winner = None 
        self.winner_hand = None

    def rules(self, player_sum, dealer_sum):
        if player_sum > 21:
            game.winner = "Dealer"
            print("You busted! Dealer win!")

        if dealer_sum > 21:
            game.winner = "Player"
            print("The Dealer has busted. You win!")

        if player_sum == 21:
            print("You got 21! Blackjack! So you win!")
            if dealer_sum == 21:
                game.winner = "Tie" 
                print("The Dealer also got 21. Tough Break.")
            else:
                game.winner = "Player"
            return
        
        elif dealer_sum == 21:
            game.winner = "Dealer"
            print("The Dealer got 21! Tough Break, you lose!")
            return
        
        if player_sum < 21 and dealer_sum < 21:
            if player_sum > dealer_sum:
                game.winner = "Player"
                print("You beat the Dealer! You got lucky punk.")
            elif player_sum == dealer_sum:
                game.winner = "Tie"
                print("It is a push, no one wins!")
            elif player_sum < dealer_sum:
                game.winner = "Dealer"
                print("Dealer wins! Better luck next time.")
        return

class Player:
    def __init__(self):
        self.playerID = 1
        self.currency = 100
        self.hit_status = True 
        self.stand_status = False 

    def player_stand(self):
        self.hit_status = False
        self.stand_status = True 

class Dealer:
    def __init__(self, num_players):
        self.num_players = num_players
        self.playerID = 0
        self.hands = [] # Store the hands of each player
        self.deck = []
        self.special_values = {'A': '[1, 11]', 
                               'J': '10', 
                               'Q': '10', 
                               'K': '10'}
        
    def shuffle(self) -> list:
        self.hands = [[] for _ in range(game.num_players)]
        suits = ['♠', '♥', '♦', '♣']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = [{'value': value, 'suit': suit} for value in values for suit in suits]
        random.shuffle(self.deck)
        return self.deck 
    
    def draw(self) -> list:
        # Every Player (Including the Dealer)
        # Recieves 2 cards at start
        for _ in range(2):
            for playerID in range(self.num_players):
                card = self.deck.pop() # {'value': '2', 'suit': '♠'}
                self.hands[playerID].append(card)
        
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
        if val <= 21:
            winning_difference = 21 - val if 21 - val <= 11 else 21 - 11
            deck = [card['value'] for card in self.deck]
            safe_cards_count = 0 # Cards the dealer can have without getting busted

            safe_cards_count += deck.count('A')
            for card_val in range(2, winning_difference+1):
                if card_val == 10:
                    for card in ['10', 'J', 'Q', 'K']: # J, Q, K are also valued at 10
                        safe_cards_count += deck.count(card)
                else:
                    safe_cards_count += deck.count(str(card_val))

            # print(f"safe_cards_count: {safe_cards_count}, deck: {len(deck)}")        
            
            return (hand, val, round((safe_cards_count/len(deck))*100, 2))
        else: # Busted
            return (hand, val, 0.00)
    
    def hand_sum(self, playerID):
        return dealer.hand_evaluation(playerID)[1]
    
    def win_probability(self):
        # Player has taken all the cards and choose to stand
        # Calculate the difference between player_hand_sum and dealer_hand_sum
        # For example: player_hand_sum = 19[K, 6, 3], dealer_hand_sum = 14[J, 4], Deck: 47 cards remaining
        # Difference = 19 - 14 = 5 -> Min = 5, Max = 21 - 14 = 7, Range = 5 - 7
        # Calculate the chance to recieve a card with value in the range from 5 - 7
        #   -> This chance is equivelent to winning/tie chance 
        # If winning chance is greater than the average/media percentage of the card_val
        # Take another card from the deck
        
        player_hand, player_sum, player_safe_card_chance = dealer.hand_evaluation(player.playerID)
        dealer_hand, dealer_sum, dealer_safe_card_chance = dealer.hand_evaluation(0)

        if player_sum > 21:
            return (100.00, 0.00, 100.00)

        elif dealer_sum <= player_sum:
            
            deck = [card['value'] for card in self.deck]
            potential_win_card = defaultdict(dict) # Cards the dealer can have without getting busted

            player_max_difference = 21 - player_sum 
            dealer_win_hand = [player_sum + difference for difference in range(1, player_max_difference + 1)]

            dealer_win_card = [str(diff) for card_val in dealer_win_hand if (diff := card_val - dealer_sum) <= 11]
            print(f"dealer win hand: {dealer_win_hand}\ndealer win card: {dealer_win_card}")

            if '1' in dealer_win_card or '11' in dealer_win_card:
                potential_win_card['A'] = deck.count('A')
                try:
                    dealer_win_card.remove('1')
                except ValueError:
                    dealer_win_card.remove('11')

            for card_val in dealer_win_card:
                if card_val == '10':
                    for card in ['10', 'J', 'Q', 'K']:
                        potential_win_card[card] = deck.count(card)
                else:
                    potential_win_card[card_val] = deck.count(str(card_val))

            winning_possibility = sum([potential_win_card[card_val] for card_val in potential_win_card.keys()])
            print(f"winning possibility: {(winning_possibility/len(deck)) * 100:.2f}%")
            print(f"player hand: {player_hand} - player sum: {player_sum} - safe card chance: {player_safe_card_chance}")
            print(f"dealer hand: {dealer_hand} - dealer sum: {dealer_sum} - safe card chance: {dealer_safe_card_chance}")
            print(f"potential winning cards: {potential_win_card}")

            draw_level = False 

            # Calculate draw possibility -> Dealer must also have a hand with sum of 21
            draw_difference = player_sum - dealer_sum
            if draw_difference == 0:
                draw_difference == len(deck)
            elif draw_difference == 1:
                draw_difference_count = deck.count("A")
            else:
                draw_difference_count = deck.count(str(draw_difference))
            draw_percentage = (draw_difference_count/len(deck)) * 100

            if winning_possibility == 0:
                draw_level = True
            
            if draw_level: 
                # Dealer is required to take minimum of 2 card to surpass/level player sum or bust
                # Assumption is player sum is <= 21
                return (0.00, round(draw_percentage, 2), dealer_safe_card_chance)
            
            else:
                # Return winning possibility value 
                winning_possibility = (winning_possibility/len(deck)) * 100
                return (round(winning_possibility, 2), round(draw_percentage, 2), dealer_safe_card_chance)
        else:
            print(f"dealer sum: {dealer_sum}, player sum: {player_sum}")
            return (100.00, 0.00, 100.00)
            
game = Game()
dealer = Dealer(game.num_players) 
player = Player()
onGoingGame = True

dealer.shuffle()
dealer.draw()

while onGoingGame:
    print(dealer.hands)
    userDecision = input("Do you want a card: ")
    if userDecision == 'y':
        dealer.deal_cards(1)
        print(dealer.hands[1])
    elif userDecision == 'n':
        player.player_stand()
        winning_chance, draw_percentage, safe_chance = dealer.win_probability()
        if (winning_chance, draw_percentage, safe_chance) != (None, None, None):
            print(f"winning chance: {winning_chance}%, draw percentage: {draw_percentage}%, safe chance: {safe_chance}%")
            player_sum = dealer.hand_sum(player.playerID)
            dealer_sum = dealer.hand_sum(dealer.playerID)
            game.rules(player_sum, dealer_sum)
            print(game.winner)
        break

    
"""
Terminal Output:
[[{'value': '6', 'suit': '♥'}, {'value': '6', 'suit': '♠'}], [{'value': 'J', 'suit': '♠'}, {'value': '9', 'suit': '♠'}]]
Do you want a card: n
dealer win hand: [20, 21]
dealer win card: ['8', '9']
winning possibility: 14.58%
player hand: ['10', '9'] - player sum: 19 - safe card chance: 16.67
dealer hand: ['6', '6'] - dealer sum: 12 - safe card chance: 68.75
potential winning cards: defaultdict(<class 'dict'>, {'8': 4, '9': 3})
winning chance: 14.58%, draw percentage: 8.33%, safe chance: 68.75%
You beat the Dealer! You got lucky punk.
Game winner: Player
"""
