from typing import List
from card import Card

class MeldValidator:
    @staticmethod
    def is_valid_sequence(cards: List[Card]) -> bool:
        """Check if cards form a valid sequence (same suit, consecutive)"""
        if len(cards) < 3:
            return False
        
        # Count jokers
        jokers = [c for c in cards if c.is_joker]
        non_jokers = [c for c in cards if not c.is_joker]
        
        if not non_jokers:  # All jokers - not valid
            return False
        
        # Check same suit (for non-jokers)
        suit = non_jokers[0].suit
        if not all(c.suit == suit for c in non_jokers):
            return False
        
        # Sort non-jokers by value
        non_jokers.sort(key=lambda c: c.get_value())
        
        # Check if we can form a sequence with jokers filling gaps
        values = [c.get_value() for c in non_jokers]
        
        # Check for consecutive sequence possibility
        min_val = min(values)
        max_val = max(values)
        
        # Total span should not exceed the number of cards
        if max_val - min_val + 1 > len(cards):
            return False
        
        # Check if jokers can fill the gaps
        expected_values = list(range(min_val, max_val + 1))
        missing_count = len(expected_values) - len(values)
        
        return missing_count <= len(jokers)
    
    @staticmethod
    def is_valid_set(cards: List[Card]) -> bool:
        """Check if cards form a valid set (same rank)"""
        if len(cards) < 3:
            return False
        
        # Count jokers
        jokers = [c for c in cards if c.is_joker]
        non_jokers = [c for c in cards if not c.is_joker]
        
        if not non_jokers:  # All jokers - not valid
            return False
        
        # Check same rank (for non-jokers)
        rank = non_jokers[0].rank
        return all(c.rank == rank for c in non_jokers)
    
    @staticmethod
    def is_valid_meld(cards: List[Card]) -> bool:
        """Check if cards form a valid meld (set or sequence)"""
        return MeldValidator.is_valid_set(cards) or MeldValidator.is_valid_sequence(cards)