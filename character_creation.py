from typing import Optional
from models import Character
from character_manager import CharacterManager
from ui_helpers import UIHelpers, CharacterTemplates


class CharacterCreation:
    """Handles interactive character creation"""

    def __init__(self):
        self.ui = UIHelpers()
        self.templates = CharacterTemplates()

    def create_character_interactive(self, manager: CharacterManager, char_type: str = "character") -> Optional[Character]:
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

    def create_character_manual(self, manager: CharacterManager, name: str, char_type: str) -> Character:
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

    def create_character_random(self, manager: CharacterManager, name: str, char_type: str) -> Character:
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

    def create_character_template(self, manager: CharacterManager, name: str, char_type: str) -> Character:
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

    def create_enemy_group(self, manager: CharacterManager):
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
