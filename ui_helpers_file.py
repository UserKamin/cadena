import os


class UIHelpers:
    """Helper functions for the user interface"""

    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_header(title: str):
        """Print a formatted header"""
        print("=" * 60)
        print(f" {title.center(58)} ")
        print("=" * 60)

    @staticmethod
    def print_separator():
        """Print a separator line"""
        print("-" * 60)

    @staticmethod
    def get_int_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
        """Get integer input with validation"""
        while True:
            try:
                value = int(input(prompt))
                if min_val is not None and value < min_val:
                    print(f"Value must be at least {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Value must be at most {max_val}")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number.")

    @staticmethod
    def get_string_input(prompt: str, allow_empty: bool = False) -> str:
        """Get string input with validation"""
        while True:
            value = input(prompt).strip()
            if not allow_empty and not value:
                print("Input cannot be empty.")
                continue
            return value


class CharacterTemplates:
    """Predefined character templates"""

    TEMPLATES = {
        "1": {"name": "Warrior", "str": 16, "dex": 12, "int": 8, "wis": 10, "agi": 11, "con": 15, "level": 3},
        "2": {"name": "Rogue", "str": 10, "dex": 18, "int": 12, "wis": 13, "agi": 16, "con": 11, "level": 3},
        "3": {"name": "Mage", "str": 8, "dex": 10, "int": 18, "wis": 16, "agi": 12, "con": 10, "level": 3},
        "4": {"name": "Cleric", "str": 12, "dex": 10, "int": 14, "wis": 18, "agi": 11, "con": 13, "level": 3},
        "5": {"name": "Goblin", "str": 8, "dex": 14, "int": 6, "wis": 8, "agi": 15, "con": 10, "level": 1},
        "6": {"name": "Orc", "str": 16, "dex": 10, "int": 6, "wis": 8, "agi": 9, "con": 14, "level": 2},
        "7": {"name": "Dragon", "str": 20, "dex": 12, "int": 16, "wis": 15, "agi": 14, "con": 20, "level": 10},
        "8": {"name": "Skeleton", "str": 12, "dex": 13, "int": 4, "wis": 6, "agi": 12, "con": 8, "level": 2},
        "9": {"name": "Troll", "str": 18, "dex": 8, "int": 4, "wis": 7, "agi": 6, "con": 18, "level": 4},
    }

    @classmethod
    def get_template(cls, template_id: str) -> dict:
        """Get template by ID"""
        return cls.TEMPLATES.get(template_id)

    @classmethod
    def list_templates(cls):
        """Print all available templates"""
        print("Available templates:")
        for key, template in cls.TEMPLATES.items():
            t = template
            print(f"{key}. {t['name']} - STR:{t['str']} DEX:{t['dex']} INT:{t['int']} "
                  f"WIS:{t['wis']} AGI:{t['agi']} CON:{t['con']} Level:{t['level']}")
