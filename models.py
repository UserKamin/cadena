from typing import Optional
from typing import Dict, List
import random
from typing import Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class CombatResult(Enum):
    VICTORY = "victory"
    DEFEAT = "defeat"
    ONGOING = "ongoing"


@dataclass
class Character:
    """Character class with all stats and combat properties"""
    name: str
    level: int = 1
    title: str = ""

    # Base stats
    strength: int = 10
    dexterity: int = 10
    intelligence: int = 10
    wisdom: int = 10
    agility: int = 10
    constitution: int = 10

    # Combat properties (calculated from base stats)
    current_hp: Optional[int] = None
    current_mana: Optional[int] = None

    def __post_init__(self):
        """Initialize calculated properties after object creation"""
        if self.current_hp is None:
            self.current_hp = self.max_hp
        if self.current_mana is None:
            self.current_mana = self.max_mana

    @property
    def max_hp(self) -> int:
        """HP = Constitution * 2"""
        return self.constitution * 2

    @property
    def max_mana(self) -> int:
        """Mana = Intelligence"""
        return self.intelligence

    @property
    def mana_regen(self) -> int:
        """Mana regeneration per turn = Wisdom"""
        return max(1, self.wisdom // 3)  # Fixed: prevent zero regen

    @property
    def is_alive(self) -> bool:
        """Check if character is still alive"""
        return self.current_hp > 0

    def heal(self, amount: int) -> int:
        """Heal character and return actual amount healed"""
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - old_hp

    def take_damage(self, damage: int) -> int:
        """Apply damage and return actual damage taken"""
        actual_damage = min(damage, self.current_hp)
        self.current_hp = max(0, self.current_hp - damage)
        return actual_damage

    def regenerate_mana(self) -> int:
        """Regenerate mana based on wisdom, return amount regenerated"""
        old_mana = self.current_mana
        self.current_mana = min(
            self.max_mana, self.current_mana + self.mana_regen)
        return self.current_mana - old_mana

    def spend_mana(self, amount: int) -> bool:
        """Try to spend mana, return True if successful"""
        if self.current_mana >= amount:
            self.current_mana -= amount
            return True
        return False

    def reset_to_full(self):
        """Reset HP and mana to maximum"""
        self.current_hp = self.max_hp
        self.current_mana = self.max_mana

    def get_display_name(self) -> str:
        """Get formatted display name with title and level"""
        title_part = f"{self.title} " if self.title else ""
        return f"{title_part}{self.name} (Lv.{self.level})"

    def to_dict(self) -> Dict:
        """Convert character to dictionary for saving"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Character':
        """Create character from dictionary"""
        return cls(**data)

    def __str__(self) -> str:
        return (f"{self.get_display_name()}\n"
                f"STR:{self.strength} DEX:{self.dexterity} INT:{self.intelligence} "
                f"WIS:{self.wisdom} AGI:{self.agility} CON:{self.constitution}\n"
                f"HP:{self.current_hp}/{self.max_hp} MP:{self.current_mana}/{self.max_mana}")


# combat_engine.py - Fixed version


class CombatEngine:
    """Handles turn-based combat simulation"""

    def __init__(self):
        self.combat_log: List[str] = []

    def calculate_hit_chance(self, attacker: Character, defender: Character) -> float:
        """Calculate hit chance based on attacker DEX vs defender DEX"""
        # Base 50% + (attacker_dex - defender_dex) * 3%
        # Clamped between 5% and 95%
        base_chance = 0.5
        dex_difference = attacker.dexterity - defender.dexterity
        hit_chance = base_chance + (dex_difference * 0.03)
        return max(0.05, min(0.95, hit_chance))

    def calculate_damage(self, attacker: Character) -> int:
        """Calculate base damage from STR with some randomization"""
        base_damage = attacker.strength
        # Add some variance: 80% to 120% of base damage
        variance = random.uniform(0.8, 1.2)
        return max(1, int(base_damage * variance))

    def attack(self, attacker: Character, defender: Character) -> Dict:
        """Perform an attack and return result details"""
        if not attacker.is_alive:
            return {"hit": False, "damage": 0, "message": f"{attacker.name} is defeated and cannot attack!"}

        hit_chance = self.calculate_hit_chance(attacker, defender)
        hit_roll = random.random()

        if hit_roll <= hit_chance:
            damage = self.calculate_damage(attacker)
            actual_damage = defender.take_damage(damage)

            message = f"{attacker.name} hits {defender.name} for {actual_damage} damage!"
            if not defender.is_alive:
                message += f" {defender.name} is defeated!"

            return {
                "hit": True,
                "damage": actual_damage,
                "message": message,
                "hit_chance": hit_chance
            }
        else:
            return {
                "hit": False,
                "damage": 0,
                "message": f"{attacker.name} misses {defender.name}!",
                "hit_chance": hit_chance
            }

    def determine_turn_order(self, participants: List[Character]) -> List[Character]:
        """Sort participants by AGI (highest first), with random tiebreaker"""
        return sorted(participants, key=lambda x: (x.agility, random.random()), reverse=True)

    def process_turn(self, character: Character):
        """Process end-of-turn effects (mana regeneration)"""
        if character.is_alive:
            mana_regen = character.regenerate_mana()
            if mana_regen > 0 and hasattr(self, '_detailed_log') and self._detailed_log:
                self.log(f"{character.name} regenerates {mana_regen} mana.")

    def log(self, message: str):
        """Add message to combat log"""
        self.combat_log.append(message)

    def clear_log(self):
        """Clear the combat log"""
        self.combat_log.clear()

    def get_combat_log(self) -> List[str]:
        """Get copy of combat log"""
        return self.combat_log.copy()


# character_creation.py - Fixed version


class CharacterCreation:
    """Handles interactive character creation"""

    def __init__(self):
        # Fixed: import here to avoid circular imports
        from ui_helpers import UIHelpers, CharacterTemplates
        self.ui = UIHelpers()
        self.templates = CharacterTemplates()

    def create_character_interactive(self, manager, char_type: str = "character") -> Optional[Character]:
        """Interactive character creation"""
        print(f"\n--- Create New {char_type.title()} ---")

        name = self.ui.get_string_input(f"Enter {char_type} name: ")

        # Check if name already exists
        if manager.get_character(name):
            print(f"A {char_type} with that name already exists!")
            return None

        print("\nCharacter Creation Options:")
        print("1. Manual stat entry")
        print("2. Random stats")
        print("3. Preset templates")

        choice = self.ui.get_int_input("Choose creation method (1-3): ", 1, 3)

        if choice == 1:
            return self.create_character_manual(manager, name, char_type)
        elif choice == 2:
            return self.create_character_random(manager, name, char_type)
        else:
            return self.create_character_template(manager, name, char_type)

    def create_character_manual(self, manager, name: str, char_type: str) -> Character:
        """Manual character creation with stat entry"""
        print(f"\nEnter stats for {name}:")

        title = self.ui.get_string_input(
            "Title (optional): ", allow_empty=True)
        level = self.ui.get_int_input("Level (1-20): ", 1, 20)

        print("\nEnter base stats (1-20):")
        strength = self.ui.get_int_input("Strength: ", 1, 20)
        dexterity = self.ui.get_int_input("Dexterity: ", 1, 20)
        intelligence = self.ui.get_int_input("Intelligence: ", 1, 20)
        wisdom = self.ui.get_int_input("Wisdom: ", 1, 20)
        agility = self.ui.get_int_input("Agility: ", 1, 20)
        constitution = self.ui.get_int_input("Constitution: ", 1, 20)

        char = manager.create_character(
            name=name, title=title, level=level,
            strength=strength, dexterity=dexterity, intelligence=intelligence,
            wisdom=wisdom, agility=agility, constitution=constitution
        )

        print(f"\n{char_type.title()} created successfully!")
        print(char)
        return char

    def create_character_random(self, manager, name: str, char_type: str) -> Character:
        """Random character creation"""
        print(f"\nRandom {char_type} generation:")
        print("1. Weak (stats 6-12, level 1-3)")
        print("2. Average (stats 8-15, level 2-5)")
        print("3. Strong (stats 12-18, level 4-8)")
        print("4. Custom ranges")

        choice = self.ui.get_int_input("Choose power level (1-4): ", 1, 4)

        if choice == 1:
            stat_range = (6, 12)
            level_range = (1, 3)
        elif choice == 2:
            stat_range = (8, 15)
            level_range = (2, 5)
        elif choice == 3:
            stat_range = (12, 18)
            level_range = (4, 8)
        else:
            print("Enter custom ranges:")
            stat_min = self.ui.get_int_input("Minimum stat value: ", 1, 20)
            stat_max = self.ui.get_int_input(
                "Maximum stat value: ", stat_min, 20)
            level_min = self.ui.get_int_input("Minimum level: ", 1, 20)
            level_max = self.ui.get_int_input("Maximum level: ", level_min, 20)
            stat_range = (stat_min, stat_max)
            level_range = (level_min, level_max)

        char = manager.create_random_character(name, stat_range, level_range)

        # Add optional title
        title = self.ui.get_string_input(
            "Title (optional): ", allow_empty=True)
        if title:
            char.title = title

        print(f"\n{char_type.title()} created successfully!")
        print(char)
        return char

    # Fixed: return type
    def create_character_template(self, manager, name: str, char_type: str) -> Optional[Character]:
        """Create character from templates"""
        print(f"\n{self.templates.list_templates()}")

        choice = input("Choose template (1-9): ")
        template = self.templates.get_template(choice)

        if not template:
            print("Invalid choice!")
            return None

        char = manager.create_character(
            name=name,
            title=template["name"],
            level=template["level"],
            strength=template["str"],
            dexterity=template["dex"],
            intelligence=template["int"],
            wisdom=template["wis"],
            agility=template["agi"],
            constitution=template["con"]
        )

        print(f"\n{char_type.title()} created successfully!")
        print(char)
        return char

    def create_enemy_group(self, manager):
        """Create multiple enemies at once"""
        print("\n--- Create Enemy Group ---")

        base_name = self.ui.get_string_input(
            "Base name for enemies (e.g., 'Goblin'): ")
        count = self.ui.get_int_input("How many enemies to create: ", 1, 20)

        print("\nEnemy creation method:")
        print("1. All identical (use template)")
        print("2. Random variations")

        method = self.ui.get_int_input("Choose method (1-2): ", 1, 2)

        if method == 1:
            # Create one template enemy
            print(f"\nCreate template for {base_name}:")
            template = self.create_character_interactive(manager, "enemy")
            if not template:
                return

            # Create copies
            for i in range(2, count + 1):
                enemy_name = f"{base_name}_{i}"
                template_data = template.to_dict()
                template_data['name'] = enemy_name
                manager.characters[enemy_name] = Character.from_dict(
                    template_data)

            print(f"\nCreated {count} {base_name} enemies!")

        else:
            # Random variations
            print("Enter stat ranges for random generation:")
            stat_min = self.ui.get_int_input("Minimum stat value: ", 1, 20)
            stat_max = self.ui.get_int_input(
                "Maximum stat value: ", stat_min, 20)
            level_min = self.ui.get_int_input("Minimum level: ", 1, 20)
            level_max = self.ui.get_int_input("Maximum level: ", level_min, 20)

            for i in range(1, count + 1):
                enemy_name = f"{base_name}_{i}"
                manager.create_random_character(
                    enemy_name, (stat_min, stat_max), (level_min, level_max)
                )

            print(f"\nCreated {count} random {base_name} enemies!")
