import random
from typing import List, Optional
from card import Card, Suit

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()
        self.shuffle()
    
    def create_deck(self):
        """Create a standard 52-card deck plus 2 jokers"""
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        suits = [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]
        
        # Add regular cards
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank, suit))
        
        # Add 2 jokers
        self.cards.append(Card("JOKER", is_joker=True))
        self.cards.append(Card("JOKER", is_joker=True))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self) -> Optional[Card]:
        return self.cards.pop() if self.cards else None
    
    def is_empty(self) -> bool:
        return len(self.cards) == 0