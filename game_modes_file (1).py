import random
from typing import List
from models import Character, CombatResult
from combat_simulation import CombatSimulation
from character_manager import CharacterManager
from ui_helpers import UIHelpers


class GameModes:
    """Special game modes like quick battle and tournament"""

    def __init__(self, char_manager: CharacterManager, combat_sim: CombatSimulation):
        self.char_manager = char_manager
        self.combat_sim = combat_sim
        self.ui = UIHelpers()
