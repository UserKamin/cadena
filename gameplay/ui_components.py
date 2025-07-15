import tkinter as tk
from tkinter import ttk

class UIComponents:
    """Handles UI component creation and management"""
    
    def __init__(self, root):
        self.root = root
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI components"""
        # Title
        title_label = tk.Label(self.root, text="Two Sequence Card Game", 
                              font=('Arial', 24, 'bold'), bg='darkgreen', fg='white')
        title_label.pack(pady=10)
        
        # Game info frame
        self.info_frame = tk.Frame(self.root, bg='darkgreen')
        self.info_frame.pack(pady=10)
        
        self.current_player_label = tk.Label(self.info_frame, text="", 
                                           font=('Arial', 16), bg='darkgreen', fg='yellow')
        self.current_player_label.pack()
        
        # Deck and discard area
        self.deck_frame = tk.Frame(self.root, bg='darkgreen')
        self.deck_frame.pack(pady=10)
        
        # Deck button
        self.deck_button = tk.Button(self.deck_frame, text="DECK\n🂠", 
                                    font=('Arial', 14), width=8, height=4,
                                    bg='blue', fg='white')
        self.deck_button.pack(side=tk.LEFT, padx=10)
        
        # Discard pile
        self.discard_button = tk.Button(self.deck_frame, text="DISCARD\n(Empty)", 
                                       font=('Arial', 14), width=8, height=4,
                                       bg='gray', fg='white')
        self.discard_button.pack(side=tk.LEFT, padx=10)
        
        # Cards remaining label
        self.cards_remaining_label = tk.Label(self.deck_frame, text="Cards: 54", 
                                             font=('Arial', 12), bg='darkgreen', fg='white')
        self.cards_remaining_label.pack(side=tk.LEFT, padx=10)
        
        # Turn timer label
        self.turn_timer_label = tk.Label(self.deck_frame, text="", 
                                        font=('Arial', 12), bg='darkgreen', fg='yellow')
        self.turn_timer_label.pack(side=tk.LEFT, padx=10)
        
        # Player hand frame
        self.hand_frame = tk.Frame(self.root, bg='darkgreen', height=200)
        self.hand_frame.pack(pady=20, fill=tk.X)
        self.hand_frame.pack_propagate(False)
        
        # Action buttons
        self.action_frame = tk.Frame(self.root, bg='darkgreen')
        self.action_frame.pack(pady=10)
        
        self.win_button = tk.Button(self.action_frame, text="Declare Win", 
                                   font=('Arial', 14), bg='gold', fg='black',
                                   state=tk.DISABLED)
        self.win_button.pack(side=tk.LEFT, padx=10)
        
        self.sort_button = tk.Button(self.action_frame, text="Sort Hand", 
                                    font=('Arial', 14), bg='lightblue', fg='black')
        self.sort_button.pack(side=tk.LEFT, padx=10)
        
        # Game log
        self.log_frame = tk.Frame(self.root, bg='darkgreen')
        self.log_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        log_label = tk.Label(self.log_frame, text="Game Log:", 
                           font=('Arial', 12, 'bold'), bg='darkgreen', fg='white')
        log_label.pack(anchor=tk.W)
        
        self.log_text = tk.Text(self.log_frame, height=8, width=80, 
                               font=('Arial', 10), bg='black', fg='white')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for log
        scrollbar = tk.Scrollbar(self.log_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
    
    def log_message(self, message: str):
        """Add a message to the game log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)