from typing import List, Optional
from itertools import combinations
from card import Card
from player import Player
from meld_validator import MeldValidator

class GameLogic:
    @staticmethod
    def can_win(player: Player) -> bool:
        """Check if player can win with current hand"""
        if len(player.hand) != 7:  # Must have exactly 7 cards to win
            return False
        
        # Try all possible combinations of 4 and 3 cards
        for four_card_combo in combinations(player.hand, 4):
            remaining_cards = [c for c in player.hand if c not in four_card_combo]
            
            if (MeldValidator.is_valid_meld(list(four_card_combo)) and 
                MeldValidator.is_valid_meld(remaining_cards)):
                return True
        
        return False
    
    @staticmethod
    def can_take_discard(player: Player, discard_card: Card) -> bool:
        """Check if player can take the discard card (must immediately complete a meld)"""
        # Try adding the discard card to the hand temporarily
        test_hand = player.hand + [discard_card]
        
        # Check if it immediately forms a valid meld
        for r in range(3, len(test_hand) + 1):
            for combo in combinations(test_hand, r):
                if discard_card in combo and MeldValidator.is_valid_meld(list(combo)):
                    return True
        
        return False
    
    @staticmethod
    def find_winning_melds(player: Player) -> Optional[tuple]:
        """Find the winning combination of 4-card and 3-card melds"""
        if len(player.hand) != 7:
            return None
        
        for four_card_combo in combinations(player.hand, 4):
            remaining_cards = [c for c in player.hand if c not in four_card_combo]
            
            if (MeldValidator.is_valid_meld(list(four_card_combo)) and 
                MeldValidator.is_valid_meld(remaining_cards)):
                return (list(four_card_combo), remaining_cards)
        
        return None