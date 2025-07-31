import tkinter as tk
from typing import List
from card import Card
from .ui_components import UIComponents
from .game_controller import GameController
from .drag_drop_card import DragDropCard

class CardGameGUI:
    """Main GUI class for the card game"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Two Sequence Card Game")
        self.root.geometry("1400x900")
        self.root.configure(bg='darkgreen')
        
        # Initialize UI components
        self.ui = UIComponents(self.root)
        
        # Initialize game controller
        self.controller = GameController(self.ui)
        
        # Drag and drop cards list
        self.drag_cards = []
        
        # Setup and start game
        if self.controller.setup_game():
            self.update_display()
        else:
            self.root.quit()
    
    def create_card_button(self, card: Card, row: int, col: int) -> tk.Button:
        """Create a clickable and draggable card button"""
        def card_click():
            if not self.controller.must_discard_to_start or not self.controller.must_discard_to_start:
                self.controller.card_clicked(card)
                self.update_display()
        
        card_text = str(card)
        card_color = card.get_color()
        
        button = tk.Button(self.ui.hand_frame, text=card_text, 
                          font=('Arial', 12, 'bold'), width=4, height=2,
                          bg='white', fg=card_color, 
                          relief=tk.RAISED, bd=2,
                          command=card_click)
        
        button.grid(row=row, column=col, padx=2, pady=2)
        
        # Create drag-drop handler
        drag_card = DragDropCard(card, button, self)
        self.drag_cards.append(drag_card)
        
        return button
    
    def update_display(self):
        """Update the game display"""
        if self.controller.game_over:
            winner_name = self.controller.winner.name if self.controller.winner else 'Unknown'
            self.ui.current_player_label.config(text=f"🏆 Winner: {winner_name} 🏆")
            self.ui.deck_button.config(state='disabled')
            self.ui.discard_button.config(state='disabled')
            return
        
        # Clear hand frame
        for widget in self.ui.hand_frame.winfo_children():
            widget.destroy()
        
        self.drag_cards = []
        
        # Update current player info
        current_player = self.controller.get_current_player()
        if not current_player:
            return
        
        self.ui.current_player_label.config(text=f"Current Player: {current_player.name}")
        
        # Display current player's hand
        hand_label = tk.Label(self.ui.hand_frame, text=f"{current_player.name}'s Hand:", 
                             font=('Arial', 14, 'bold'), bg='darkgreen', fg='white')
        hand_label.grid(row=0, column=0, columnspan=10, pady=5)
        
        # Create card buttons
        for i, card in enumerate(current_player.hand):
            row = 1 + i // 8
            col = i % 8
            
            button = self.create_card_button(card, row, col)
            
            # Highlight selected cards
            if card in self.controller.selected_cards:
                button.config(bg='yellow', relief=tk.SUNKEN)
        
        # Add discard button if cards are selected
        if self.controller.selected_cards and len(current_player.hand) >= 8:
            discard_btn = tk.Button(self.ui.hand_frame, text="DISCARD\nSELECTED", 
                                   font=('Arial', 12, 'bold'), bg='red', fg='white',
                                   command=self.controller.discard_selected)
            discard_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Update discard pile display
        if self.controller.discard_pile:
            top_card = self.controller.discard_pile[-1]
            self.ui.discard_button.config(text=f"DISCARD\n{top_card}", 
                                        bg='orange', fg='black')
        else:
            self.ui.discard_button.config(text="DISCARD\n(Empty)", 
                                        bg='gray', fg='white')
        
        # Update cards remaining
        deck_cards = len(self.controller.deck.cards) if self.controller.deck else 0
        self.ui.cards_remaining_label.config(text=f"Cards: {deck_cards}")
        
        # Update win button state
        self.controller.check_win_condition()
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()