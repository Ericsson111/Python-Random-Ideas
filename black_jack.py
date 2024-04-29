# Python 3.9.6 64-bit
# 2024/4/28
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
import time
import os 


class Game:
    def __init__(self):
        self.num_players = 2
        self.winner = None 
        self.tie_game_count = 0
        self.player_win_count = 0
        self.dealer_win_count = 0
        self.total_game_count = 0

    def clear_terminal(self):
        os.system("cls || clear")

    def display_hands(self):
        self.display_hand(dealer.playerID, dealer.hands[dealer.playerID], False)
        print("Dealer hand\n")
        self.display_hand(player.playerID, dealer.hands[player.playerID], True)
        print("Player hand\n") 

    def main_game(self):
        play_game = True
        print("\n------- Welcome to my Blackjack game! -------\n")
        while play_game:
            onGoingGame = True
            self.winner = None

            dealer.shuffle()
            dealer.draw()

            # Display hand
            self.display_hands() 

            player_sum = dealer.hand_sum(player.playerID)
            dealer_sum = dealer.hand_sum(dealer.playerID)

            if dealer_sum == 21 and dealer_sum == player_sum:
                self.winner = "Tie"
                self.rules(player_sum, dealer_sum)

            elif dealer_sum == 21:
                self.winner = "Dealer"
                self.rules(player_sum, dealer_sum)
            elif player_sum == 21:
                self.winner = "Player"
                self.rules(player_sum, dealer_sum)

            # Game begins
            if self.winner == None:

                while onGoingGame:

                    userDecision = input("Hit/Stand: ")
                    userDecision = userDecision.strip().lower()

                    self.clear_terminal() 

                    if userDecision in ['h', 'hit']:
                        dealer.deal_cards(player.playerID)
                        winning_chance, draw_percentage, safe_chance, dealer_bust_chance = dealer.win_probability()
                        self.display_hands()
                        print(f"Dealer Statistics: winning chance: {winning_chance:.2f}%, draw percentage: {draw_percentage:.2f}%, safe chance: {safe_chance:.2f}%, bust chance: {dealer_bust_chance:.2f}%")

                    elif userDecision in ['s', 'stand']:
                        player.player_stand()

                        while True:
                            decision = dealer.decision()
                            print(f"dealer decision (player: stand): {decision}")
                            winning_chance, draw_percentage, safe_chance, dealer_bust_chance = dealer.win_probability()
                            print(f"Dealer Statistics: winning chance: {winning_chance:.2f}%, draw percentage: {draw_percentage:.2f}%, safe chance: {safe_chance:.2f}%, bust chance: {dealer_bust_chance:.2f}%")
                            self.clear_terminal() 
                            if decision == "Hit":
                                dealer.deal_cards(dealer.playerID)
                                self.display_hands() 
                                time.sleep(1)
                            else:
                                self.display_hands()
                                break      
                        break

            self.clear_terminal()
            self.display_hand(dealer.playerID, dealer.hands[dealer.playerID], True)
            print("Dealer hand\n")
            self.display_hand(player.playerID, dealer.hands[player.playerID], True)
            print("Player hand\n") 
            player_sum = dealer.hand_sum(player.playerID)
            dealer_sum = dealer.hand_sum(dealer.playerID)
            print("_________________________________________")
            self.rules(player_sum, dealer_sum)
            print(f"Game winner: {self.winner}")

            if game.winner == "Dealer":
                self.dealer_win_count += 1
            elif game.winner == "Player":
                self.player_win_count += 1
            else:
                self.tie_game_count += 1
            
            self.total_game_count += 1

            print("-----------------------------------------")
            while True:
                rematchDecision = input("Do you want to play again?(y/n): ")
                rematchDecision = rematchDecision.strip().lower()
                if rematchDecision in ['n', 'no']:
                    play_game = False
                    self.display_statistics() 
                    break 
                elif rematchDecision in ['y', 'yes']:
                    self.clear_terminal() 
                    break 

    def display_statistics(self):
        self.clear_terminal()
        print("Player Statistics:")
        print("----------------------") 
        print(f"|Player win: {self.player_win_count:^5}   |")
        print(f"|Tie game:   {self.tie_game_count:^5}   |")
        print(f"|Total game: {self.total_game_count:^5}   |")
        print(f"|Win rate:   {(self.player_win_count/self.total_game_count)*100:^5.2f}%  |")
        print("----------------------") 
            
    def display_hand(self, playerID: int, cards: list, reveal):
        """
        This function takes a list of card dictionaries and prints them formatted as small poker cards, 
        hiding the dealer's second card unless 'reveal' is True.
        
        Args:
            playerID (int): The identifier for the player, where 0 is typically the dealer.
            cards (list of dict): The list of cards to display, where each card is a dictionary
                                with 'value' and 'suit' keys.
            reveal (bool): Flag to indicate whether to reveal the dealer's second card.
        """
        top = ' ___ '   # Top part of the card
        bottom = '|___|' # Bottom part of the card
        
        # Prepare lines for each part of the card display
        middle_top = []
        middle_bottom = []
        
        # Generate each card's display lines
        for card_ind, card in enumerate(cards):
            if playerID == 0 and card_ind == 1 and not reveal:
                val = '?'
                suit = '?'
                middle_top.append(f'|{val}{suit} |')
                middle_bottom.append(f'|__{suit}|')
            else:
                val = str(card['value'])
                suit = card['suit']
                # Handle special case for 10 (two characters)
                if val == '10':
                    middle_top.append(f'|{val}{suit}|')
                    middle_bottom.append(f'|__{suit}|')
                else:
                    middle_top.append(f'|{val}{suit} |')
                    middle_bottom.append(f'|__{suit}|')
        
        # Print the cards
        print('   '.join([top] * len(cards)))  # Print the top line for all cards
        print('   '.join(middle_top))          # Print the middle top part of each card
        print('   '.join(middle_bottom))       # Print the middle bottom part of each card
        print('   '.join([bottom] * len(cards)))  # Print the bottom line for all cards

    def rules(self, player_sum: int, dealer_sum: int):
        """
        This function takes the sum of player hand and the dealer hand and determine the winner,
        which will be modified in game.winner
        
        Args:
            player_sum (int): The sum value of the player's hand
            dealer_sum (int): The sum value of the dealer's hand
        """
        
        if player_sum > 21:
            self.winner = "Dealer"
            print("You busted! Dealer win!")

        if dealer_sum > 21:
            self.winner = "Player"
            print("The Dealer has busted. You win!")

        if player_sum == 21:
            print("You got 21! Blackjack! So you win!")
            if dealer_sum == 21:
                self.winner = "Tie" 
                print("The Dealer also got 21. Tough Break.")
            else:
                self.winner = "Player"
            return
        
        elif dealer_sum == 21:
            self.winner = "Dealer"
            print("The Dealer got 21! Tough Break, you lose!")
            return
        
        if player_sum < 21 and dealer_sum < 21:
            if player_sum > dealer_sum:
                self.winner = "Player"
                print("You beat the Dealer! You got lucky punk.")
            elif player_sum == dealer_sum:
                self.winner = "Tie"
                print("It is a push, no one wins!")
            elif player_sum < dealer_sum:
                self.winner = "Dealer"
                print("Dealer wins! Better luck next time.")
        return

class Player:
    def __init__(self):
        self.playerID = 1
        self.currency = 100
        self.hit_status = True 
        self.stand_status = False 

    def player_stand(self):
        """ This function modify player's status when making the decision to stand """
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
        """
        This function uses all the values and their corresponding suits to build a deck for the game
        and is shuffled using random.shuffle()
        """
        self.hands = [[] for _ in range(game.num_players)]
        suits = ['♠', '♥', '♦', '♣']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = [{'value': value, 'suit': suit} for value in values for suit in suits]
        random.shuffle(self.deck)
        return self.deck 
    
    def draw(self) -> list:
        # Every Player (Including the Dealer)
        # Recieves 2 cards at the start of the game
        for _ in range(2):
            for playerID in range(self.num_players):
                card = self.deck.pop() # {'value': '2', 'suit': '♠'}
                self.hands[playerID].append(card)
        
        return self.hands 
    
    def deal_cards(self, playerID: int): 
        # Deal cards to the player who requested it using playerID
        card = self.deck.pop()
        self.hands[playerID].append(card)
        
    def hand_evaluation(self, playerID) -> tuple: 
        # Evaluate the sum of the player's hand given playerID as identifier
        hand = [card['value'] for card in self.hands[playerID]] # ['9', 'A']
        hand_val = [self.special_values[card] if card in ['A', 'J', 'Q', 'K'] else card for card in hand]  # [9, [1, 11]]

        if hand == ['A', 'A']:
            hand_val = 12 
            return self.card_counting((['A', 'A'], 12))

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
            primary_hand = self.optimized_ace_hand(playerID, (handA, handB))
        else:
            primary_hand = (handA, handA_sum)
        
        return self.card_counting(primary_hand)
    
    # Return the optimized ace inclusive hand that allow the requested hand to not bust 
    def optimized_ace_hand(self, playerID, hands: tuple) -> tuple:
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
            game.winner = self.playerID if playerID == player.playerID else player.playerID
            primary_hand = (handA, handA_sum) if handA_sum <= handB_sum else (handB, handB_sum)

        return primary_hand
    
    # Calculate the chance of the dealer to draw a safe card 
    def card_counting(self, primary_hand: tuple) -> tuple:
        hand, val = primary_hand
        winning_difference = 21 - val if 21 - val <= 11 else 21 - 11
        deck = [card['value'] for card in self.deck]
        safe_cards_count = 0 # Cards the dealer can have without getting busted
        bust_cards_count = 0

        safe_cards_count += deck.count('A')
        for card_val in range(2, winning_difference+1):
            if card_val == 10:
                for card in ['10', 'J', 'Q', 'K']: # J, Q, K are also valued at 10
                    safe_cards_count += deck.count(card)
            else:
                safe_cards_count += deck.count(str(card_val))
        bust_cards_count = len(deck) - safe_cards_count     
        
        return (bust_cards_count, hand, val, round((safe_cards_count/len(deck))*100, 2))
    
    def hand_sum(self, playerID):
        return self.hand_evaluation(playerID)[2]
    
    def win_probability(self):
        # Player has taken all the cards and choose to stand
        # Calculate the difference between player_hand_sum and dealer_hand_sum
        # For example: player_hand_sum = 19[K, 6, 3], dealer_hand_sum = 14[J, 4], Deck: 47 cards remaining
        # Difference = 19 - 14 = 5 -> Min = 5, Max = 21 - 14 = 7, Range = 5 - 7
        # Calculate the chance to recieve a card with value in the range from 5 - 7
        #   -> This chance is equivelent to winning/tie chance 
        # If winning chance is greater than the average/media percentage of the card_val
        # Take another card from the deck
        player_sum = self.hand_evaluation(player.playerID)[2]
        dealer_bust_cards_count, _, dealer_sum, dealer_safe_card_chance = self.hand_evaluation(0)

        if player_sum > 21:
            return (100.00, 0.00, 100.00, 0.00)
        
        if dealer_sum > 21:
            return (0.00, 0.00, 0.00, 100.00)

        elif dealer_sum <= player_sum:
            deck = [card['value'] for card in self.deck]
            dealer_bust_chance = round((dealer_bust_cards_count/len(deck)) * 100, 2)
            potential_win_card = defaultdict(dict) # Cards the dealer can have without getting busted

            player_max_difference = 21 - player_sum 
            dealer_win_hand = [player_sum + difference for difference in range(1, player_max_difference + 1)]

            dealer_win_card = [str(diff) for card_val in dealer_win_hand if (diff := card_val - dealer_sum) <= 11]
            # print(f"dealer win hand: {dealer_win_hand}\ndealer win card: {dealer_win_card}")

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
            draw_level = False 

            # Calculate draw possibility -> Dealer must also have a hand with sum of 21
            draw_difference = player_sum - dealer_sum
            draw_difference_count = 0
            if draw_difference == 0:
                return ((winning_possibility/len(deck)) * 100, 100.00, dealer_safe_card_chance, dealer_bust_chance)
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
                return (0.00, round(draw_percentage, 2), dealer_safe_card_chance, dealer_bust_chance)
            
            else:
                # Return winning possibility value 
                winning_possibility = (winning_possibility/len(deck)) * 100
                return (round(winning_possibility, 2), round(draw_percentage, 2), dealer_safe_card_chance, dealer_bust_chance)
        else:
            return (100.00, 0.00, 100.00, 0.00)
            
    def decision(self):
        # Primary evaluation
        #   -> No risk for dealer for busting on the next card(If choose to his)
        # Player Chance of  
        #   -> Dealer's chance of busting
        # Dealer Chance of Winning
        #   -> Dealer drawing a hand with sum greater than player
        winning_percentage, draw_percentage, safe_percentage, dealer_bust_chance = self.win_probability() 

        if winning_percentage == 100: # Leave it
            return "Stand"
        
        if winning_percentage > dealer_bust_chance: # More likely to win than bust
            return "Hit"
        
        elif winning_percentage < dealer_bust_chance: # More likely to bust
            # If draw
            if draw_percentage == 100: 
                if safe_percentage >= 66:
                    return "Hit"
                else:
                    return "stand"
            
            # Next draw is fairly safe
            if safe_percentage > dealer_bust_chance:
                return "Hit"
            
            if winning_percentage >= 30:
                return "Hit"

            # Impossible to win, 1/3 chance for safe card
            if winning_percentage == 0 and safe_percentage >= 33:
                return "Hit"
            
            else:
                return "Stand"
        else: # Equal
            if safe_percentage > dealer_bust_chance:
                return "Hit"
            else:
                return "Stand"

if __name__ == "__main__":
    game = Game()
    dealer = Dealer(game.num_players) 
    player = Player()
    game.main_game()

