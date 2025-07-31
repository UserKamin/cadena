from typing import List, Optional
from card import Card

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = []
    
    def add_card(self, card: Card):
        self.hand.append(card)
    
    def remove_card(self, card: Card):
        if card in self.hand:
            self.hand.remove(card)
    
    def sort_hand(self):
        """Sort hand by suit and rank"""
        self.hand.sort(key=lambda c: (c.suit.value if c.suit else "Z", c.get_value() if not c.is_joker else 0))
    
    def display_hand(self):
        self.sort_hand()
        return " ".join(str(card) for card in self.hand)