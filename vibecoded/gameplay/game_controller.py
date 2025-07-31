import threading
import time
from tkinter import messagebox, simpledialog
from typing import List
from deck import Deck
from player import Player
from game_logic import GameLogic
from card import Card

class GameController:
    """Handles game logic and state management"""
    
    def __init__(self, ui_components):
        self.ui = ui_components
        
        # Game state
        self.players = []
        self.deck = None
        self.discard_pile = []
        self.current_player_index = 0
        self.game_over = False
        self.winner = None
        self.selected_cards = []
        self.turn_start_time = 0
        self.deck_draw_enabled = True
        self.must_discard_to_start = False
        
        # Bind UI events
        self.setup_ui_events()
    
    def setup_ui_events(self):
        """Setup UI event handlers"""
        self.ui.deck_button.config(command=self.draw_from_deck)
        self.ui.discard_button.config(command=self.take_discard)
        self.ui.win_button.config(command=self.declare_win)
        self.ui.sort_button.config(command=self.sort_hand)
    
    def setup_game(self):
        """Setup the game with players"""
        # Get number of players
        num_players = simpledialog.askinteger("Setup", "Number of players (2-6):", 
                                            minvalue=2, maxvalue=6)
        if not num_players:
            return False
        
        # Get player names
        player_names = []
        for i in range(num_players):
            name = simpledialog.askstring("Setup", f"Enter name for Player {i+1}:")
            if not name:
                name = f"Player {i+1}"
            player_names.append(name)
        
        # Initialize game
        self.players = [Player(name) for name in player_names]
        self.deck = Deck()
        self.discard_pile = []
        self.current_player_index = 0
        
        # Deal cards
        self.deal_cards()
        self.start_turn()
        
        self.ui.log_message("🎮 Game Started! Win by forming one 4-card meld and one 3-card meld!")
        self.ui.log_message("Melds: same rank (7♦ 7♣ 7♠) or consecutive same suit (4♠ 5♠ 6♠)")
        self.ui.log_message("Jokers 🃏 can substitute for any card!")
        self.ui.log_message("💡 Drag cards to rearrange your hand!")
        
        return True
    
    def deal_cards(self):
        """Deal cards to players"""
        # Deal 7 cards to each player
        for _ in range(7):
            for player in self.players:
                card = self.deck.deal_card()
                if card:
                    player.add_card(card)
        
        # Deal 1 extra card to starting player
        starting_player = self.players[self.current_player_index]
        card = self.deck.deal_card()
        if card:
            starting_player.add_card(card)
        
        self.ui.log_message(f"{starting_player.name} is the starting player (8 cards)")
        self.must_discard_to_start = True
    
    def start_turn(self):
        """Start a new turn with 1-second delay for deck drawing"""
        self.turn_start_time = time.time()
        self.deck_draw_enabled = False
        self.ui.deck_button.config(state='disabled', text="DECK\n🂠\n(Wait...)")
        
        # Enable deck drawing after 1 second
        def enable_deck_draw():
            time.sleep(1)
            if not self.game_over:
                self.deck_draw_enabled = True
                self.ui.deck_button.config(state='normal', text="DECK\n🂠")
        
        threading.Thread(target=enable_deck_draw, daemon=True).start()
        self.update_turn_timer()
    
    def update_turn_timer(self):
        """Update turn timer display"""
        if self.game_over:
            return
        
        elapsed = time.time() - self.turn_start_time
        if elapsed < 1:
            remaining = 1 - elapsed
            self.ui.turn_timer_label.config(text=f"Draw in: {remaining:.1f}s")
            self.ui.root.after(100, self.update_turn_timer)
        else:
            self.ui.turn_timer_label.config(text="")
    
    def draw_from_deck(self):
        """Draw a card from the deck"""
        if self.game_over or not self.deck_draw_enabled:
            return
        
        if self.must_discard_to_start:
            messagebox.showwarning("Warning", "Starting player must discard first!")
            return
        
        current_player = self.players[self.current_player_index]
        
        if len(current_player.hand) >= 8:
            messagebox.showwarning("Warning", "You must discard before drawing!")
            return
        
        if self.deck.is_empty():
            self.reshuffle_deck()
        
        card = self.deck.deal_card()
        if card:
            current_player.add_card(card)
            self.ui.log_message(f"{current_player.name} drew from deck")
            self.check_win_condition()
    
    def take_discard(self):
        """Take the top card from discard pile"""
        if self.game_over or not self.discard_pile:
            return
        
        if self.must_discard_to_start:
            messagebox.showwarning("Warning", "Starting player must discard first!")
            return
        
        current_player = self.players[self.current_player_index]
        
        if len(current_player.hand) >= 8:
            messagebox.showwarning("Warning", "You must discard before drawing!")
            return
        
        top_discard = self.discard_pile[-1]
        
        if GameLogic.can_take_discard(current_player, top_discard):
            card = self.discard_pile.pop()
            current_player.add_card(card)
            self.ui.log_message(f"{current_player.name} took {card} from discard")
            self.check_win_condition()
        else:
            messagebox.showwarning("Invalid Move", 
                                 "You can only take the discard if it immediately completes a meld!")
    
    def check_win_condition(self):
        """Check if current player can win"""
        current_player = self.players[self.current_player_index]
        if GameLogic.can_win(current_player):
            self.ui.win_button.config(state='normal')
            self.ui.log_message(f"🎉 {current_player.name} can win!")
        else:
            self.ui.win_button.config(state='disabled')
    
    def declare_win(self):
        """Declare victory"""
        if self.game_over:
            return
        
        current_player = self.players[self.current_player_index]
        
        if len(current_player.hand) != 7:
            messagebox.showwarning("Invalid Win", "You must have exactly 7 cards to win!")
            return
        
        winning_melds = GameLogic.find_winning_melds(current_player)
        if winning_melds:
            four_card_meld, three_card_meld = winning_melds
            
            meld_info = f"4-card meld: {' '.join(str(c) for c in four_card_meld)}\n"
            meld_info += f"3-card meld: {' '.join(str(c) for c in three_card_meld)}"
            
            messagebox.showinfo("🏆 WINNER! 🏆", 
                              f"{current_player.name} wins!\n\n{meld_info}")
            
            self.ui.log_message(f"🏆 {current_player.name} WINS! 🏆")
            self.ui.log_message(f"Winning melds: {meld_info}")
            
            self.game_over = True
            self.winner = current_player
            self.ui.win_button.config(state='disabled')
        else:
            messagebox.showwarning("Invalid Win", "You don't have valid winning melds!")
    
    def check_discard_winners(self, discarded_card: Card):
        """Check if any player can win with the discarded card"""
        winners = []
        
        for i, player in enumerate(self.players):
            if i != self.current_player_index:  # Skip current player
                if GameLogic.can_win_with_discard(player, discarded_card):
                    winners.append(player)
        
        if winners:
            winner_names = ", ".join(p.name for p in winners)
            self.ui.log_message(f"🚨 {winner_names} can win with {discarded_card}!")
            
            # Show popup for each winner
            for winner in winners:
                response = messagebox.askyesno("Winning Opportunity!", 
                                             f"{winner.name} can win with {discarded_card}!\n\nTake it and win?")
                if response:
                    # Player takes the card and wins
                    winner.add_card(discarded_card)
                    self.discard_pile.pop()
                    
                    winning_melds = GameLogic.find_winning_melds(winner)
                    if winning_melds:
                        four_card_meld, three_card_meld = winning_melds
                        
                        meld_info = f"4-card meld: {' '.join(str(c) for c in four_card_meld)}\n"
                        meld_info += f"3-card meld: {' '.join(str(c) for c in three_card_meld)}"
                        
                        messagebox.showinfo("🏆 WINNER! 🏆", 
                                          f"{winner.name} wins by taking the discard!\n\n{meld_info}")
                        
                        self.ui.log_message(f"🏆 {winner.name} WINS by taking {discarded_card}! 🏆")
                        self.ui.log_message(f"Winning melds: {meld_info}")
                        
                        self.game_over = True
                        self.winner = winner
                        return True
        
        return False
    
    def discard_card(self, card: Card):
        """Discard a card"""
        if self.game_over:
            return
        
        current_player = self.players[self.current_player_index]
        
        if card in current_player.hand:
            current_player.remove_card(card)
            self.discard_pile.append(card)
            self.selected_cards = []
            
            self.ui.log_message(f"{current_player.name} discarded {card}")
            
            # Check if any player can win with this discard
            if not self.check_discard_winners(card):
                self.next_turn()
    
    def next_turn(self):
        """Move to next player's turn"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.start_turn()
    
    def sort_hand(self):
        """Sort current player's hand"""
        if not self.game_over:
            current_player = self.players[self.current_player_index]
            current_player.sort_hand()
    
    def reshuffle_deck(self):
        """Reshuffle discard pile when deck runs out"""
        if len(self.discard_pile) <= 1:
            messagebox.showwarning("Game Over", "Not enough cards to continue!")
            return
        
        # Keep top discard, shuffle the rest back into deck
        top_discard = self.discard_pile.pop()
        self.deck.cards = self.discard_pile[:]
        self.deck.shuffle()
        self.discard_pile = [top_discard]
        self.ui.log_message("Deck reshuffled!")
    
    def card_clicked(self, card: Card):
        """Handle card selection"""
        current_player = self.players[self.current_player_index]
        
        if self.must_discard_to_start:
            # Starting player must discard
            if card in current_player.hand:
                self.discard_card(card)
                self.must_discard_to_start = False
                return
        
        # Normal card selection for discarding
        if card in self.selected_cards:
            self.selected_cards.remove(card)
        else:
            self.selected_cards = [card]  # Only one card can be selected for discard
    
    def discard_selected(self):
        """Discard the selected card"""
        if not self.selected_cards or self.game_over:
            return
        
        card_to_discard = self.selected_cards[0]
        self.discard_card(card_to_discard)
    
    def get_current_player(self):
        """Get the current player"""
        return self.players[self.current_player_index] if self.players else None