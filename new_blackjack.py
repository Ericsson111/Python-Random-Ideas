import random

num_players = 4

class Dealer:
    def __init__(self, num_players):
        self.num_players = num_players
        self.hands = [[] for _ in range(num_players)] # Store the hands of each player
        self.deck = []

    def shuffle_deck(self):
        suits = ['♠', '♥', '♦', '♣']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = [{'value': value, 'suit': suit} for value in values for suit in suits]

        random.shuffle(self.deck)
        print(self.deck)
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
    
    def decision():
        pass

# Deal cards to players
dealer = Dealer(num_players)
deck = dealer.shuffle_deck()

hands = dealer.draw()
print(f"Cards Count: {len(dealer.deck)}, Hands: {dealer.hands}")

dealer.deal_cards(1) # 1 is player id
print(f"Cards Count: {len(dealer.deck)}, Hands: {dealer.hands}")

dealer.deal_cards(1)
print(f"Cards Count: {len(dealer.deck)}, Hands: {dealer.hands}")

