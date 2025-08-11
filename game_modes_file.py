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

    def quick_battle(self):
        """Quick random battle"""
        players = self.char_manager.list_characters()
        if not players:
            print("No player characters found! Create a character first.")
            input("\nPress Enter to continue...")
            return

        print("\n--- Quick Battle ---")
        print("Select player character:")
        for i, name in enumerate(players, 1):
            char = self.char_manager.get_character(name)
            print(f"{i}. {char.get_display_name()}")

        player_choice = self.ui.get_int_input(
            "Choose player: ", 1, len(players))
        player_name = players[player_choice - 1]

        # Generate random enemies
        enemy_count = random.randint(1, 4)
        random_enemies = []

        enemy_templates = ["Goblin", "Orc", "Skeleton", "Wolf", "Bandit"]

        for i in range(enemy_count):
            enemy_type = random.choice(enemy_templates)
            enemy = Character(
                name=f"{enemy_type}_{i+1}",
                title=enemy_type,
                level=random.randint(1, 5),
                strength=random.randint(6, 15),
                dexterity=random.randint(6, 15),
                intelligence=random.randint(4, 12),
                wisdom=random.randint(4, 12),
                agility=random.randint(6, 15),
                constitution=random.randint(6, 15)
            )
            random_enemies.append(enemy)

        print(f"\nRandom encounter: {enemy_count} enemies!")
        for enemy in random_enemies:
            print(f"  {enemy.get_display_name()}")

        result = self.combat_sim.simulate_combat(
            player_name, random_enemies, detailed_log=False)

        print(f"\nBattle Result: {result['result'].value.upper()}")
        print(f"Rounds: {result['rounds']}")
        print(
            f"Enemies defeated: {result['enemies_defeated']}/{result['total_enemies']}")

        input("\nPress Enter to continue...")

    def tournament_mode(self):
        """Tournament mode - fight multiple groups"""
        players = self.char_manager.list_characters()
        if not players:
            print("No player characters found! Create a character first.")
            input("\nPress Enter to continue...")
            return

        print("\n--- Tournament Mode ---")
        print("Select player character:")
        for i, name in enumerate(players, 1):
            char = self.char_manager.get_character(name)
            print(f"{i}. {char.get_display_name()}")

        player_choice = self.ui.get_int_input(
            "Choose player: ", 1, len(players))
        player_name = players[player_choice - 1]
        player = self.char_manager.get_character(player_name)

        rounds = self.ui.get_int_input("Number of tournament rounds: ", 1, 10)

        wins = 0
        losses = 0

        for round_num in range(1, rounds + 1):
            print(f"\n{'='*40}")
            print(f"TOURNAMENT ROUND {round_num}")
            print(f"{'='*40}")

            # Generate enemies for this round
            enemy_count = random.randint(1, 3)
            difficulty = min(round_num, 5)  # Difficulty scales with rounds

            enemies = []
            for i in range(enemy_count):
                enemy_name = f"Round{round_num}_Enemy{i+1}"
                stat_min = 6 + difficulty
                stat_max = 12 + difficulty
                level_range = (1, 2 + difficulty)

                enemy = Character(
                    name=enemy_name,
                    level=random.randint(*level_range),
                    strength=random.randint(stat_min, stat_max),
                    dexterity=random.randint(stat_min, stat_max),
                    intelligence=random.randint(stat_min-2, stat_max-2),
                    wisdom=random.randint(stat_min-2, stat_max-2),
                    agility=random.randint(stat_min, stat_max),
                    constitution=random.randint(stat_min, stat_max)
                )
                enemies.append(enemy)

            print(f"Facing {enemy_count} enemies:")
            for enemy in enemies:
                print(f"  {enemy}")

            # Run combat
            result = self.combat_sim.simulate_combat(
                player_name, enemies, detailed_log=False)

            if result['result'] == CombatResult.VICTORY:
                wins += 1
                print(f"🎉 ROUND {round_num} - VICTORY!")
            else:
                losses += 1
                print(f"💀 ROUND {round_num} - DEFEAT!")
                break  # Tournament ends on first loss

            print(
                f"Player HP after round: {result['player_final_hp']}/{result['player_max_hp']}")

            if round_num < rounds:
                # Heal player partially between rounds
                heal_amount = player.max_hp // 4  # Heal 25%
                player.heal(heal_amount)
                print(f"Player heals {heal_amount} HP between rounds")

        print(f"\n{'='*40}")
        print("TOURNAMENT RESULTS")
        print(f"{'='*40}")
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        if wins + losses > 0:
            print(f"Win Rate: {wins/(wins+losses)*100:.1f}%")

        if wins == rounds:
            print("🏆 TOURNAMENT CHAMPION!")
        elif wins >= rounds // 2:
            print("🥈 Good performance!")
        else:
            print("Better luck next time!")

        input("\nPress Enter to continue...")
