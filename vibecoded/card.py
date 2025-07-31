from enum import Enum
from typing import Optional
from dataclasses import dataclass

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

@dataclass
class Card:
    rank: str
    suit: Optional[Suit] = None
    is_joker: bool = False
    
    def __str__(self):
        if self.is_joker:
            return "🃏"
        return f"{self.rank}{self.suit.value if self.suit else ''}"
    
    def __repr__(self):
        return str(self)
    
    def get_value(self):
        """Get numeric value for sequence checking"""
        if self.is_joker:
            return -1  # Special value for jokers
        if self.rank == "A":
            return 1
        elif self.rank == "J":
            return 11
        elif self.rank == "Q":
            return 12
        elif self.rank == "K":
            return 13
        else:
            return int(self.rank)
    
    def get_color(self):
        """Get card color for display"""
        if self.is_joker:
            return "purple"
        if self.suit in [Suit.HEARTS, Suit.DIAMONDS]:
            return "red"
        return "black"