import random
import json
from typing import Dict, List, Optional, Tuple
from models import Character


class CharacterManager:
    """Manages character creation, editing, and persistence"""

    def __init__(self):
        self.characters: Dict[str, Character] = {}

    def create_character(self, name: str, **kwargs) -> Character:
        """Create a new character with given stats"""
        char = Character(name=name, **kwargs)
        self.characters[name] = char
        return char

    def create_random_character(self, name: str, stat_range: Tuple[int, int] = (8, 15),
                                level_range: Tuple[int, int] = (1, 5)) -> Character:
        """Create a character with randomized stats within given ranges"""
        stats = {
            'strength': random.randint(*stat_range),
            'dexterity': random.randint(*stat_range),
            'intelligence': random.randint(*stat_range),
            'wisdom': random.randint(*stat_range),
            'agility': random.randint(*stat_range),
            'constitution': random.randint(*stat_range),
            'level': random.randint(*level_range)
        }
        return self.create_character(name, **stats)

    def edit_character(self, name: str, **kwargs) -> bool:
        """Edit existing character stats"""
        if name not in self.characters:
            return False

        char = self.characters[name]
        for attr, value in kwargs.items():
            if hasattr(char, attr):
                setattr(char, attr, value)

        # Recalculate HP/Mana if constitution/intelligence changed
        if 'constitution' in kwargs and char.current_hp > char.max_hp:
            char.current_hp = char.max_hp
        if 'intelligence' in kwargs and char.current_mana > char.max_mana:
            char.current_mana = char.max_mana

        return True

    def delete_character(self, name: str) -> bool:
        """Delete a character"""
        if name in self.characters:
            del self.characters[name]
            return True
        return False

    def get_character(self, name: str) -> Optional[Character]:
        """Get character by name"""
        return self.characters.get(name)

    def list_characters(self) -> List[str]:
        """Get list of all character names"""
        return list(self.characters.keys())

    def save_to_file(self, filename: str):
        """Save all characters to JSON file"""
        data = {name: char.to_dict() for name, char in self.characters.items()}
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filename: str):
        """Load characters from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.characters = {name: Character.from_dict(char_data)
                               for name, char_data in data.items()}
        except FileNotFoundError:
            print(
                f"File {filename} not found. Starting with empty character list.")
        except json.JSONDecodeError:
            print(f"Error reading {filename}. File may be corrupted.")
