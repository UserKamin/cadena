from typing import List
from models import Character
from character_manager import CharacterManager
from combat_simulation import CombatSimulation
from character_creation import CharacterCreation
from game_modes import GameModes
from ui_helpers import UIHelpers


class UserInterface:
    """Interactive command-line interface for the combat simulator"""

    def __init__(self):
        self.char_manager = CharacterManager()
        self.enemy_manager = CharacterManager()  # Separate manager for enemies
        self.combat_sim = CombatSimulation(self.char_manager)
        self.char_creator = CharacterCreation()
        self.game_modes = GameModes(self.char_manager, self.combat_sim)
        self.ui = UIHelpers()

        self.save_file_chars = "characters.json"
        self.save_file_enemies = "enemies.json"

        # Try to load existing data
        self.load_data()

    def list_characters(self, manager: CharacterManager, char_type: str):
        """List all characters"""
        chars = manager.list_characters()
        if not chars:
            print(f"No {char_type}s found.")
            return

        print(f"\n--- {char_type.title()}s ---")
        for i, char_name in enumerate(chars, 1):
            char = manager.get_character(char_name)
            print(f"{i}. {char}")
            self.ui.print_separator()

    def edit_character(self, manager: CharacterManager, char_type: str):
        """Edit an existing character"""
        chars = manager.list_characters()
        if not chars:
            print(f"No {char_type}s to edit.")
            return

        print(f"\nSelect {char_type} to edit:")
        for i, name in enumerate(chars, 1):
            print(f"{i}. {name}")

        try:
            choice = self.ui.get_int_input("Enter number: ", 1, len(chars))
            char_name = chars[choice - 1]
            char = manager.get_character(char_name)

            print(f"\nEditing {char}")
            print("\nWhat would you like to edit?")
            print("1. Name")
            print("2. Title")
            print("3. Level")
            print("4. Individual stat")
            print("5. All stats")

            edit_choice = self.ui.get_int_input("Choose option (1-5): ", 1, 5)

            if edit_choice == 1:
                new_name = self.ui.get_string_input("New name: ")
                # Remove old character and add with new name
                char_data = char.to_dict()
                char_data['name'] = new_name
                manager.delete_character(char_name)
                manager.characters[new_name] = Character.from_dict(char_data)
                print("Name updated!")

            elif edit_choice == 2:
                new_title = self.ui.get_string_input(
                    "New title: ", allow_empty=True)
                manager.edit_character(char_name, title=new_title)
                print("Title updated!")

            elif edit_choice == 3:
                new_level = self.ui.get_int_input("New level (1-20): ", 1, 20)
                manager.edit_character(char_name, level=new_level)
                print("Level updated!")

            elif edit_choice == 4:
                print("Which stat to edit?")
                print("1. Strength")
                print("2. Dexterity")
                print("3. Intelligence")
                print("4. Wisdom")
                print("5. Agility")
                print("6. Constitution")

                stat_choice = self.ui.get_int_input(
                    "Choose stat (1-6): ", 1, 6)
                stats = ['strength', 'dexterity', 'intelligence',
                         'wisdom', 'agility', 'constitution']
                stat_name = stats[stat_choice - 1]

                new_value = self.ui.get_int_input(
                    f"New {stat_name} value (1-20): ", 1, 20)
                manager.edit_character(char_name, **{stat_name: new_value})
                print(f"{stat_name.title()} updated!")

            elif edit_choice == 5:
                print("Enter new stats:")
                new_stats = {}
                new_stats['strength'] = self.ui.get_int_input(
                    "Strength: ", 1, 20)
                new_stats['dexterity'] = self.ui.get_int_input(
                    "Dexterity: ", 1, 20)
                new_stats['intelligence'] = self.ui.get_int_input(
                    "Intelligence: ", 1, 20)
                new_stats['wisdom'] = self.ui.get_int_input("Wisdom: ", 1, 20)
                new_stats['agility'] = self.ui.get_int_input(
                    "Agility: ", 1, 20)
                new_stats['constitution'] = self.ui.get_int_input(
                    "Constitution: ", 1, 20)

                manager.edit_character(char_name, **new_stats)
                print("All stats updated!")

            print(f"\nUpdated {char_type}:")
            print(manager.get_character(char_name))

        except (ValueError, IndexError):
            print("Invalid selection!")

    def delete_character(self, manager: CharacterManager, char_type: str):
        """Delete a character"""
        chars = manager.list_characters()
        if not chars:
            print(f"No {char_type}s to delete.")
            return

        print(f"\nSelect {char_type} to delete:")
        for i, name in enumerate(chars, 1):
            print(f"{i}. {name}")

        try:
            choice = self.ui.get_int_input("Enter number: ", 1, len(chars))
            char_name = chars[choice - 1]

            confirm = input(
                f"Are you sure you want to delete {char_name}? (y/N): ")
            if confirm.lower() == 'y':
                manager.delete_character(char_name)
                print(f"{char_type.title()} deleted!")
            else:
                print("Deletion cancelled.")

        except (ValueError, IndexError):
            print("Invalid selection!")

    def run_combat(self):
        """Run combat simulation"""
        players = self.char_manager.list_characters()
        enemies = self.enemy_manager.list_characters()

        if not players:
            print("No player characters found! Create a character first.")
            return

        if not enemies:
            print("No enemies found! Create enemies first.")
            return

        print("\n--- Combat Setup ---")

        # Select player
        print("Select player character:")
        for i, name in enumerate(players, 1):
            char = self.char_manager.get_character(name)
            print(f"{i}. {char.get_display_name()}")

        player_choice = self.ui.get_int_input(
            "Choose player (number): ", 1, len(players))
        player_name = players[player_choice - 1]

        # Select enemies
        print("\nSelect enemies (you can choose multiple):")
        for i, name in enumerate(enemies, 1):
            char = self.enemy_manager.get_character(name)
            print(f"{i}. {char.get_display_name()}")

        selected_enemies = []
        while True:
            enemy_input = input("\nEnter enemy number (or 'done' to finish): ")
            if enemy_input.lower() == 'done':
                break

            try:
                enemy_choice = int(enemy_input)
                if 1 <= enemy_choice <= len(enemies):
                    enemy_name = enemies[enemy_choice - 1]
                    enemy = self.enemy_manager.get_character(enemy_name)
                    selected_enemies.append(enemy)
                    print(f"Added {enemy.get_display_name()}")
                else:
                    print("Invalid enemy number!")
            except ValueError:
                print("Please enter a valid number or 'done'!")

        if not selected_enemies:
            print("No enemies selected for combat!")
            return

        print(f"\nCombat: {player_name} vs {len(selected_enemies)} enemies")

        # Combat options
        print("\nCombat Options:")
        print("1. Quick combat (summary only)")
        print("2. Detailed combat (full log)")

        detail_choice = self.ui.get_int_input("Choose option (1-2): ", 1, 2)
        detailed_log = (detail_choice == 2)

        # Run combat
        print("\n" + "="*60)
        print("STARTING COMBAT!")
        print("="*60)

        result = self.combat_sim.simulate_combat(
            player_name, selected_enemies,
            max_rounds=100, detailed_log=detailed_log
        )

        # Display results
        if detailed_log:
            print("\n--- COMBAT LOG ---")
            for line in result['combat_log']:
                print(line)
        else:
            print(f"\nCombat Result: {result['result'].value.upper()}")
            print(f"Rounds: {result['rounds']}")
            print(
                f"Player HP: {result['player_final_hp']}/{result['player_max_hp']}")
            print(
                f"Enemies defeated: {result['enemies_defeated']}/{result['total_enemies']}")

        input("\nPress Enter to continue...")

    def save_data(self):
        """Save characters and enemies to files"""
        try:
            self.char_manager.save_to_file(self.save_file_chars)
            self.enemy_manager.save_to_file(self.save_file_enemies)
            print("Data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        """Load characters and enemies from files"""
        try:
            self.char_manager.load_from_file(self.save_file_chars)
            self.enemy_manager.load_from_file(self.save_file_enemies)
        except Exception as e:
            pass  # Silently handle missing files on first run

    def character_menu(self):
        """Character management menu"""
        while True:
            self.ui.clear_screen()
            self.ui.print_header("Character Management")
            print("1. Create new character")
            print("2. List all characters")
            print("3. Edit character")
            print("4. Delete character")
            print("5. Back to main menu")

            choice = input("\nEnter your choice (1-5): ")

            if choice == '1':
                self.char_creator.create_character_interactive(
                    self.char_manager, "character")
                input("\nPress Enter to continue...")
            elif choice == '2':
                self.list_characters(self.char_manager, "character")
                input("\nPress Enter to continue...")
            elif choice == '3':
                self.edit_character(self.char_manager, "character")
                input("\nPress Enter to continue...")
            elif choice == '4':
                self.delete_character(self.char_manager, "character")
                input("\nPress Enter to continue...")
            elif choice == '5':
                break
            else:
                print("Invalid choice! Please try again.")
                input("\nPress Enter to continue...")

    def enemy_menu(self):
        """Enemy management menu"""
        while True:
            self.ui.clear_screen()
            self.ui.print_header("Enemy Management")
            print("1. Create new enemy")
            print("2. List all enemies")
            print("3. Edit enemy")
            print("4. Delete enemy")
            print("5. Create enemy group (multiple)")
            print("6. Back to main menu")

            choice = input("\nEnter your choice (1-6): ")

            if choice == '1':
                self.char_creator.create_character_interactive(
                    self.enemy_manager, "enemy")
                input("\nPress Enter to continue...")
            elif choice == '2':
                self.list_characters(self.enemy_manager, "enemy")
                input("\nPress Enter to continue...")
            elif choice == '3':
                self.edit_character(self.enemy_manager, "enemy")
                input("\nPress Enter to continue...")
            elif choice == '4':
                self.delete_character(self.enemy_manager, "enemy")
                input("\nPress Enter to continue...")
            elif choice == '5':
                self.char_creator.create_enemy_group(self.enemy_manager)
                input("\nPress Enter to continue...")
            elif choice == '6':
                break
            else:
                print("Invalid choice! Please try again.")
                input("\nPress Enter to continue...")

    def combat_menu(self):
        """Combat simulation menu"""
        while True:
            self.ui.clear_screen()
            self.ui.print_header("Combat Simulation")
            print("1. Start combat")
            print("2. Quick battle (random opponents)")
            print("3. Tournament mode (player vs multiple enemy groups)")
            print("4. Back to main menu")

            choice = input("\nEnter your choice (1-4): ")

            if choice == '1':
                self.run_combat()
            elif choice == '2':
                self.game_modes.quick_battle()
            elif choice == '3':
                self.game_modes.tournament_mode()
            elif choice == '4':
                break
            else:
                print("Invalid choice! Please try again.")
                input("\nPress Enter to continue...")

    def main_menu(self):
        """Main application menu"""
        while True:
            self.ui.clear_screen()
            self.ui.print_header("Combat Simulator")
            print("Welcome to the Character Combat Simulator!")
            print()

            # Show quick stats
            char_count = len(self.char_manager.list_characters())
            enemy_count = len(self.enemy_manager.list_characters())
            print(f"Characters: {char_count} | Enemies: {enemy_count}")
            print()

            print("1. Character Management")
            print("2. Enemy Management")
            print("3. Combat Simulation")
            print("4. Save Data")
            print("5. Load Data")
            print("6. Exit")

            choice = input("\nEnter your choice (1-6): ")

            if choice == '1':
                self.character_menu()
            elif choice == '2':
                self.enemy_menu()
            elif choice == '3':
                self.combat_menu()
            elif choice == '4':
                self.save_data()
                input("\nPress Enter to continue...")
            elif choice == '5':
                self.load_data()
                print("Data loaded!")
                input("\nPress Enter to continue...")
            elif choice == '6':
                print("\nSaving data before exit...")
                self.save_data()
                print("Thank you for using Combat Simulator!")
                break
            else:
                print("Invalid choice! Please try again.")
                input("\nPress Enter to continue...")
